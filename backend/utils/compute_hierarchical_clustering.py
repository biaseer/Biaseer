
import pandas as pd
import os
from sklearn.cluster import AgglomerativeClustering
from collections import Counter
import json
from utils.helpers import create_date_range

import utils.config as config

TOPIC = config.TOPIC
# media_statistic = "../../preprocess/media_statistic/renewprocess/source_url_domain_dict.json"
media_statistic = "../../preprocess/media_statistic/mention/" + TOPIC + "/source_url_domain_dict.json"

datestr = None

if TOPIC == "RUS_UKR":
    datestr=['2021-06-01','2022-08-31']
elif TOPIC == "GBR_EUR":
    datestr=['2019-10-01','2020-02-01']
elif TOPIC == "JPN_JPN":
    datestr=['2020-01-01','2023-03-20']

def readJson(filepath):
    with open(filepath, 'r') as fp:
        ans = json.load(fp)
    return ans

def dimension_reduction_cluster(dimension_reduction_file, root_path, nc=10, datestr=datestr):

    savepath = dimension_reduction_file.split(".")[0].strip() +"/csv"
    if not os.path.exists(savepath):
        os.makedirs(savepath)

    dimension_reduction_df = pd.read_csv(root_path + dimension_reduction_file)
    dimension_reduction_df["media_id"] = [i for i in range(len(dimension_reduction_df))]

    ac = AgglomerativeClustering(n_clusters=nc, affinity="euclidean", linkage="ward")
    data = dimension_reduction_df[["x1", "x2"]].values
    labels = ac.fit_predict(data)
    dimension_reduction_df["cluster_"+str(nc)] = labels
    dimension_reduction_df["media_name"] = readJson(media_statistic).keys()

    
    if '2021-06-01' in datestr and '2022-08-31' in datestr:
        dimension_reduction_df["event_num"] = readJson(media_statistic).values()
    else:
        event_root_path = '../../preprocess/media_embedding/pearson/' + TOPIC + '/'
        EventRootCode = pd.read_csv(event_root_path + "1EventRootCode_pearson.csv").fillna(0)
        timescope = create_date_range(inp=[ele.replace("-","") for ele in datestr], isint=True)
        EventRootCode = EventRootCode[(EventRootCode["timescope"] >= timescope[0]) & (EventRootCode["timescope"] <= timescope[-1])]
        # 循环计算每个媒体在当前时间段内的报道事件的个数
        media_event_num = []
        for domain in readJson(media_statistic).keys():
            media_event_num.append(sum(EventRootCode[domain]))
        dimension_reduction_df["event_num"] = media_event_num


    # resave
    dimension_reduction_df.to_csv(root_path + dimension_reduction_file, index=False)
    print(dict(Counter(labels)))

    for i in range(nc):
        tmp = dimension_reduction_df[dimension_reduction_df["cluster_"+str(nc)] == i]
        tmp.to_csv(savepath + "/cluster_" + str(i) + ".csv", index=False)

def hierarchicalTree(dimension_method_csv, level=6):
    savepath = dimension_method_csv.split("/")[0] + "/json"
    if not os.path.exists(savepath):
        os.mkdir(savepath)

    clusters = os.listdir(dimension_method_csv)
    for i, cluster in enumerate(clusters):
        tmp = pd.read_csv(dimension_method_csv + "/" + cluster)
        tree = {"left":None,
                "right":None,
                "level":0,
                "name":tmp["media_id"].tolist(),
                "len": len(tmp["media_id"].tolist())
                }
        computeHierarchicalTree(tree, tmp, level)
        # print(tree)
        json.dump(tree, open(savepath + "/cluster_" + str(i) + ".json", "w"), sort_keys=True, indent=4)


def computeHierarchicalTree(tree:dict, df, level=6)->dict:
    if len(tree["name"]) <= 20:
        return

    if tree["level"] >= level:
        return

    ac = AgglomerativeClustering(n_clusters=2, affinity="euclidean", linkage="ward")
    data = df[["x1", "x2"]].values
    labels = ac.fit_predict(data)
    df["labels"] = labels

    left_df = df[df["labels"] == 0]
    right_df = df[df["labels"] == 1]

    left_tree = {"left":None,
                 "right":None,
                 "level":tree["level"] + 1,
                 "name":left_df["media_id"].tolist(),
                 "len": len(left_df["media_id"].tolist())
                 }

    right_tree = {"left":None,
                  "right":None,
                  "level":tree["level"] + 1,
                  "name":right_df["media_id"].tolist(),
                  "len": len(right_df["media_id"].tolist())
                  }

    tree["left"] = left_tree
    tree["right"] = right_tree

    computeHierarchicalTree(tree["left"], left_df, level)
    computeHierarchicalTree(tree["right"], right_df, level)


def hierarchicalRepresentativeness(dimension_method_json):
    print(dimension_method_json)
    savepath = dimension_method_json.split("/")[0] + "/representive"
    if not os.path.exists(savepath):
        os.makedirs(savepath)

    hierarchicaltreeList = os.listdir(dimension_method_json)
    for element in hierarchicaltreeList:
        filepath = dimension_method_json + "/" + element
        element_id = int(element.split(".")[0].split("_")[-1])
        with open(filepath, 'r') as fp:
            hierarchicaltree = json.load(fp)

        cluster_df = pd.read_csv(filepath.replace("json", "csv"))

        computeHierarchicalRepresentativeness(hierarchicaltree, cluster_df)

        json.dump(hierarchicaltree, open(savepath +"/hierarchicaltree_"+ str(element_id) +".json", "w"), sort_keys=True, indent=4)

def computeHierarchicalRepresentativeness(tree:dict, cluster_df, num=10):
    if tree["left"] == None:
        tree["representive"] = tree["name"]
        return tree["representive"]

    left_Representativeness = computeHierarchicalRepresentativeness(tree["left"], cluster_df, num)
    right_Representativeness = computeHierarchicalRepresentativeness(tree["right"], cluster_df, num)

    left_nums = int(num * len(left_Representativeness) / len((left_Representativeness + right_Representativeness)))
    right_nums = int(num * len(right_Representativeness) / len((left_Representativeness + right_Representativeness)))

    if left_nums + right_nums == num - 1:
        right_nums += 1

    # print("left_nums + right_nums: ", left_nums + right_nums)

    left_df = cluster_df[cluster_df["media_id"].isin(left_Representativeness)]
    # left_center = [left_df["x1"].mean(), left_df["x2"].mean()]

    right_df = cluster_df[cluster_df["media_id"].isin(right_Representativeness)]
    # right_center = [right_df["x1"].mean(), right_df["x2"].mean()]

    # left_df['center_distance'] = left_df.apply(lambda x: (x['x1'] - left_center[0]) ** 2 +
    #                                                      (x['x2'] - left_center[1]) ** 2, axis=1)

    # right_df['center_distance'] = right_df.apply(lambda x: (x['x1'] - right_center[0]) ** 2 +
    #                                                        (x['x2'] - right_center[1]) ** 2, axis=1)

    # left_df = left_df.sort_values(by="center_distance", axis=0, ascending=True)
    # right_df = right_df.sort_values(by="center_distance", axis=0, ascending=True)

    left_df = left_df.sort_values(by="event_num", axis=0, ascending=False)
    right_df = right_df.sort_values(by="event_num", axis=0, ascending=False)

    left_Representativeness = left_df["media_id"].tolist()[:left_nums]
    right_Representativeness = right_df["media_id"].tolist()[:right_nums]

    tree["representive"] = left_Representativeness + right_Representativeness

    return tree["representive"]


def hierarchicalRepresentativeCsv(csvpath, dimension_method_representive, level=6):

    dimension_reduction_df = pd.read_csv(csvpath)
    for ilevel in range(0,level+1):
        dimension_reduction_df['zoom_' + str(ilevel)] = dimension_reduction_df.apply(lambda x: 0, axis=1)

    representiveList = os.listdir(dimension_method_representive)

    for ilevel in range(0, level+1):
        ans = []
        for representive in representiveList:
            filepath = dimension_method_representive + "/" + representive
            with open(filepath, 'r') as fp:
                representivehierarchicaltree = json.load(fp)
            computeRepresentiveLevel(representivehierarchicaltree, ans, ilevel=ilevel)

        # if ilevel > 0:
        #     dimension_reduction_df['zoom_' + str(ilevel)] = dimension_reduction_df['zoom_' + str(ilevel - 1)]
        # dimension_reduction_df['zoom_' + str(ilevel)] = dimension_reduction_df.apply(lambda x: 1 if x['media_id'] in ans else x['zoom_' + str(ilevel)], axis=1)

        dimension_reduction_df['zoom_' + str(ilevel)] = dimension_reduction_df.apply(lambda x: 1 if x['media_id'] in ans else 0, axis=1)
    
    dimension_reduction_df.to_csv("dimension_reduction_df.csv", index=False)
    return dimension_reduction_df



def computeRepresentiveLevel(tree, ans, ilevel=0):

    if ilevel == 0:
        ans += tree["representive"]
        return tree["representive"]

    if tree["left"] == None:
        computeRepresentiveLevel(tree, ans, ilevel - 1)
    else:
        computeRepresentiveLevel(tree["left"], ans, ilevel - 1)
        computeRepresentiveLevel(tree["right"], ans, ilevel - 1)


# if __name__ == "__main__":
    
#     # 先读取媒体降维结果
#     root_path = "../"
#     save_path = "../../GDELTEventKG/FrontEnd/public/helpers/"
#     dimension_reduction_file = "Pearson_tSNE_embedding_0.05.csv"
    
#     dimension_method_csv = dimension_reduction_file.split(".")[0].strip() +"/csv"
#     dimension_method_json = dimension_reduction_file.split(".")[0].strip() +"/json"
#     dimension_method_representive = dimension_reduction_file.split(".")[0].strip() +"/representive"

#     treelevel = 16
#     dimension_reduction_cluster(dimension_reduction_file, root_path, nc=10)
#     hierarchicalTree(dimension_method_csv, level=treelevel)
#     hierarchicalRepresentativeness(dimension_method_json)
#     hierarchicalRepresentativeCsv(root_path+dimension_reduction_file, dimension_method_representive, level=treelevel)

from treelib import Tree,Node
import json
class NodeData:
    def __init__(self, val,num=0,tone=0.0):
        self.label = None  # 节点标记
        self.val = val
        self.num = num  # 媒体报道数量
        self.tone = tone  # 媒体报道该事件情绪
    def __str__(self):
    #     return {'val':self.val, 'num':self.num ,'tone':self.tone}
        return str(self.val)+"+"+str(self.num)+"+"+str(self.tone)

def buildTree(json_data):
    ori_json=json.loads(json.dumps(json_data))
    pass # null tree?
    mSrc_list=ori_json["children"][0]["mSrc_list"]
    tree_list=[]
    id=0
    for mSrc in mSrc_list:
        tree=Tree()
        tree.create_node(str(id),str(id),data=NodeData(True))  #data=none
        tree_list.append(tree)
        # print(tree)
    # print(tree_list[0])
    json_node_list=ori_json["children"]
    json_fatherId_list=[0]*len(json_node_list)
    while len(json_node_list)!=0:
        json_node=json_node_list.pop(0)
        fatherId=json_fatherId_list.pop(0)
        id=id+1
        if len(json_node['children'])!=0:
            json_node_list.extend(json_node['children'])
            json_fatherId_list.extend([id]*len(json_node['children']))
        # tree_mSrcName_list=json_node['tree_mSrcName']

        for i in range(len(mSrc_list)):
            tree=tree_list[i]
            new_num=json_node['totalresource_n'][i]
            new_num=float(new_num)
            if new_num==0.0:
                node_data=NodeData(True)

                tree_node=Node(str(id),str(id),data=node_data)

            else:
                new_tone=float(json_node['avg_avgTone'][i])
                node_data=NodeData(False,num=new_num,tone=new_tone)
                tree_node=Node(str(id),str(id),data=node_data)

            tree.add_node(tree_node, parent=str(fatherId))

    return tree_list

def  find_co_contiunity_sub_path(tree):
    path_list=tree.paths_to_leaves()
    co_path_list=[]
    for path in path_list:
        temp_list=[]
        for node_id in path:
            node=tree.get_node(node_id)

            node_val=node.data.val
            if node_val==False:
                temp_list.append(node_id)
            else:
                if len(temp_list)>=2:
                    co_path_list.append(temp_list)
                temp_list=[]
        if len(temp_list)>=2: #the last con path
            co_path_list.append(temp_list)
    return co_path_list

def find_subpath_maxLen(path,tree):
    sub_path_list=[]
    temp_list=[]
    for node_id in path:
        node=tree.get_node(node_id)
        if node.data.val==False:
            temp_list.append(node_id)
        else:
            if len(temp_list)>=2:
                sub_path_list.append(temp_list)
            temp_list=[]
    if len(temp_list)>=2:
        sub_path_list.append(temp_list)
    #find maxLen
    maxL=0
    for sub_path in sub_path_list:
        if len(sub_path)>maxL:
            maxL=len(sub_path)
    return maxL
def biasTED(tree1,tree2):
    pass #归一化
    w1=1
    w3=1
    co_path_list=[]
    co_path_list.extend(find_co_contiunity_sub_path(tree1))
    co_path_list.extend(find_co_contiunity_sub_path(tree2))
    continuity_cost=0
    for co_path in co_path_list:
        node_diff=0
        if len(co_path)==0:
            continue

        for node_id in co_path:

            node1=tree1.get_node(node_id)
            node2=tree2.get_node(node_id)
            node_diff=node_diff+w1*abs(node1.data.num*node1.data.tone-node2.data.num*node2.data.tone)
        maxL1=find_subpath_maxLen(co_path,tree1)
        maxL2 = find_subpath_maxLen(co_path, tree2)
        continuity_cost=continuity_cost+w3*(abs(maxL2-maxL1))*node_diff
        # continuity_cost = continuity_cost + w3 * node_diff

    return continuity_cost

def get_tree(mSrc,mSrc_list,tree_list):
    index_i=mSrc_list.index(mSrc)
    return tree_list[index_i]
def gen_diff(mSrc_list,mSrc1):
    print("mSrc_list, mSrc ",mSrc_list,mSrc1)
    json_path = "tree_pro.json"
    f = open(json_path, 'r')
    json_data = json.load(f)
    f.close()
    # mSrc_list = json_data["children"][0]["mSrc_list"] #null tree?

    tree_list=buildTree(json_data)
    index_i=mSrc_list.index(mSrc1)
    return_dict={}
    return_dict["media"]=mSrc1
    diff_list=[]
    for i in range(len(tree_list)):
        if index_i==i:
            continue
        temp_dict={}
        temp_dict["value"]=biasTED(tree_list[index_i],tree_list[i])
        temp_dict["name"]=mSrc_list[i]
        diff_list.append(temp_dict)

    return_dict["diffArray"]=sorted(diff_list,key=lambda x:x['value'],reverse=True)
    return_mSrcList=[]
    return_mSrcList.append({"domain":mSrc1,"value":999})
    for mSrc_dict in return_dict["diffArray"]:
        return_mSrcList.append({"domain":mSrc_dict["name"],"value":mSrc_dict["value"]})
    print("tree diff: ",return_dict)
    print("return msrclist",return_mSrcList)
    return return_mSrcList








if __name__=="__main__":
    # json_path="tree_pro.json"
    # f=open(json_path,'r')
    # json_data=json.load(f)
    # f.close()
    # tree_list=buildTree(json_data)
    # # print(json_data)
    # for tree in tree_list:
    #     print(tree)
    #     # print(tree.get_node('2'))
    #     temp1=tree.expand_tree(mode=Tree.DEPTH, sorting=False) #nodelist
    #     for node in temp1:
    #         print(tree.get_node(node))
    mSrclist=['msn.com','menafn.com','yahoo.com']
    print(gen_diff(mSrclist,'msn.com'))
    # print(gen_diff(json_data, 'prokerala.com'))


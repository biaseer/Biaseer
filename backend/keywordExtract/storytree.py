import os
import shutil
import sys
from keywordExtract import geninputbypath
from keywordExtract import geninputbypathMulti
from keywordExtract import treeVisual
from keywordExtract import test_jar

def getStoryTreedata(time_scope,mSrc_list,classnum,country_list):
    if classnum=="0":
        print("classnum 0!!!!!!!!!!!!!")
        return "will not change"
    print(time_scope)
    # geninputbypath.genStoryForestInput(time_scope,mSrc_list,classnum,country_list)
    geninputbypathMulti.genStoryForestInputMulti(time_scope,mSrc_list,classnum,country_list)
    test_jar.javaMain()
    treeVisual.GenJsonByTree()
    return treeVisual.GenJsonByTree()

def genMetricTreedata(time_scope,mSrc_list,classnum,country_list,goalpath):
    if classnum=="0":
        print("classnum 0!!!!!!!!!!!!!")
        return "will not change"
    print(time_scope)
    docn=geninputbypath.genStoryForestInput(time_scope,mSrc_list,classnum,country_list)
    test_jar.testJavaMain()


    goalpath=goalpath+"/"
    fname="genconf.csv"
    f=open(goalpath+fname,'w')
    lines=[]
    lines.append("time_scope,mSrc_list,country_list,testId,docn\n")
    temp_line=str(time_scope)+","+str(mSrc_list)+","+str(country_list)+","+goalpath+","+str(docn)+"\n"
    lines.append(temp_line)
    f.writelines(lines)
    f.close()
    shutil.copy('conf/EnglishNewsParameters_cluster.txt',goalpath+"Parameter_pro.txt")
    shutil.copy('conf/EnglishNewsParameters_cluster_ori.txt', goalpath + "Parameter_ori.txt")




    treeVisual.GenJsonByTree("test_data50","tree_pro.json",goalpath)
    treeVisual.GenJsonByTree("test_data_ori", "tree_ori.json",goalpath)

    # return treeVisual.GenJsonByTree()



if __name__=='__main__':
    mSrc_list = '["interfax.com","dailytimes.com.pk","www.thehindu.com","apnews.com"]'
    time_scope = '["2022-04-01","2022-08-01"]'
    country_list = '["ALL"]'
    classnum = '11'  # 选择类
    getStoryTreedata(time_scope,mSrc_list,classnum,country_list)

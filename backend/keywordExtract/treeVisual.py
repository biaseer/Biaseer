# coding=utf8
from typing import Dict, List, Set, Tuple
import json
import  os
# from chatgpt import summarize_documents



def transfer_json(obj: Dict[str, Dict]):
    if not obj:
        return {}
    new_obj = []
    print(obj)
    for v in obj["children"].values():
        new_obj.append(transfer_json(v))

    return {"name": obj["name"], "children": new_obj}
def read_tree():
    print("read tree!!!!!!!")
    #tree_path="F:\\coding\\Event\\StoryForest\\test_data50\\stories.txt"
    tree_path = "test_data50/stories.txt"
    # tree_path = "storyteller/test_data50/stories.txt"
    # tree_path="test_data50/stories.txt"
    f=open(tree_path,'r',encoding='latin1')
    textAll=f.readlines()
    IsTree_f=0
    treeNodeList=[]  #Ԫ�أ�[treename,tree����]
    for line in textAll:
        #print(len(line))
        line = line.replace("\n", "")
        line = line.replace("\t", "")
        #print(len(line))
        if len(line)==0:#����
            if IsTree_f==1:
                IsTree_f = 0
                break
            IsTree_f=0
            continue
        if line[0]=='+': #��⵽����ʼ
            IsTree_f=1
            # ��ȡ�ӽڵ���
            index_l = line.index('(')
            index_r = line.index(')')
            tree_undernum = line[index_l + 1:index_r]

            treeNodeList.append(['ROOT',0,"time","time","url",tree_undernum,0,0,'null','null','null','null','null','null','null','null','null','null','null','null','null','null','null','null','null','null','null','null','null','null','null',[],[],[]]) #�ɸ�Ϊtree name��summaryɶ��
            continue
        if IsTree_f==1:
            tree_name = ""
            tree_h = 0
            tree_et="" #����ʱ��
            tree_lt = ""
            tree_url = ""
            tree_resouceN = ""
            f_hei=0
            #��ȡh
            for str_c in line:
                if str_c == '|':
                    tree_h = tree_h + 1
                elif str_c=='+':
                    break

            # ��ȡname
            index_l = line.index('(')
            index_r = line.index(')')
            tree_name = line[index_l + 1:index_r]
            line = line[index_r + 1:]
            # ��ȡʱ��
            index_l = line.index('(')
            index_r = line.index(')')
            tree_time = line[index_l + 1:index_r]
            tree_et = tree_time.split('to')[0]
            tree_lt = tree_time.split('to')[1]
            line = line[index_r + 1:]  # ȥ���Ѷ�ȡ��time

            tree_titlename=''
            tree_url=''
            tree_eventcode=''
            tree_eventbasecode=''
            tree_titlekeyword=''
            tree_keyword=''
            tree_resouceN=''
            tree_mSrcName=''
            tree_DocEventSim=''
            tree_corpusText=[]
            tree_docDate=[]
            tree_filePath=[]

            while(True):
                index_l = line.find('#')
                if index_l==-1:
                    break

                index_l = line.index('(')
                index_r = line.index(')')
                tree_titlename =tree_titlename+ '&'+line[index_l + 1:index_r]
                line = line[index_r + 1:]

                #��ȡurl
                index_l = line.index('@')
                index_r = line.index('[')
                tree_url = tree_url+'&'+line[index_l+2:index_r]

                #��ȡeventbasecode
                index_l = line.index('[')
                index_r = line.index(']')
                tree_eventbasecode = tree_eventbasecode+'&'+line[index_l + 1:index_r]
                line = line[index_r + 1:]

                #��ȡeventcode
                index_l = line.index('[')
                index_r = line.index(']')
                tree_eventcode = tree_eventcode+'&&&&&'+line[index_l + 1:index_r]
                line = line[index_r + 1:]
                # print(tree_eventbasecode)

                #titlekeyword
                index_l = line.index('(')
                index_r = line.index(')')
                tree_titlekeyword = tree_titlekeyword+'&'+line[index_l + 1:index_r]
                line = line[index_r + 1:]

                #keyword
                index_l = line.index('(')
                index_r = line.index(')')
                tree_keyword =tree_keyword+'&'+ line[index_l + 1:index_r]
                line = line[index_r + 1:]

                #mSrcName
                index_l = line.index('(')
                index_r = line.index(')')
                tree_mSrcName = tree_mSrcName+'&'+line[index_l + 1:index_r]
                line = line[index_r + 1:]

                #similarity
                index_l = line.index('(')
                index_r = line.index(')')
                tree_DocEventSim = tree_DocEventSim+'&'+ line[index_l + 1:index_r]
                line = line[index_r + 1:]

                #publishTime aggregation date!!!
                index_l = line.index('(')
                index_r = line.index(')')
                tree_docDate.append(line[index_l + 1:index_r])
                line = line[index_r + 1:]

                #corpusText
                index_l = line.index('(')
                index_r = line.index(')')
                tree_corpusText.append(line[index_l + 1:index_r])
                # tree_corpusText = tree_corpusText + '&' + line[index_l + 1:index_r]
                line = line[index_r + 1:]

                #filePath
                index_l = line.index('(')
                index_r = line.index(')')
                tree_filePath.append(line[index_l + 1:index_r])
                # tree_corpusText = tree_corpusText + '&' + line[index_l + 1:index_r]
                line = line[index_r + 1:]


                # ��ȡ������Դ��
                # print(line)
                index_l = line.index('$')
                index_r = line.index('|')
                tree_resouceN = tree_resouceN+'&'+line[index_l + 2:index_r] # $:

                line = line[index_r + 1:]



            #��ȡ������
            index_l = line.index('(')
            index_r = line.index(')')
            tree_maxCompatibility = line[index_l + 1:index_r]
            line = line[index_r + 1:]

            index_l = line.index('(')
            index_r = line.index(')')
            tree_totalresouceN = line[index_l + 1:index_r]
            line = line[index_r + 1:]

            # print('after totalresouceN',line)

            index_l = line.index('(')
            index_r = line.index(')')
            tree_avg_avgTone = line[index_l + 1:index_r]
            line = line[index_r + 1:]


            index_l = line.index('(')
            index_r = line.index(')')
            tree_avg_goldsteinscale = line[index_l + 1:index_r]
            line = line[index_r + 1:]

            index_l = line.index('(')
            index_r = line.index(')')
            tree_avg_nummentions = line[index_l + 1:index_r]
            line = line[index_r + 1:]

            index_l = line.index('(')
            index_r = line.index(')')
            tree_avg_numarticles = line[index_l + 1:index_r]
            line = line[index_r + 1:]

            index_l = line.index('(')
            index_r = line.index(')')
            tree_avg_numresources = line[index_l + 1:index_r]
            line = line[index_r + 1:]

            index_l = line.index('(')
            index_r = line.index(')')
            tree_totalbias = line[index_l + 1:index_r]
            line = line[index_r + 1:]
            # print('after bias',line)

            # get vari_avgTone
            index_l = line.index('(')
            index_r = line.index(')')
            tree_vari_avgtone = line[index_l + 1:index_r]
            line = line[index_r + 1:]

            # get vari_gold
            index_l = line.index('(')
            index_r = line.index(')')
            tree_vari_gold = line[index_l + 1:index_r]
            line = line[index_r + 1:]
            # get vari_nummention
            index_l = line.index('(')
            index_r = line.index(')')
            tree_vari_nummention = line[index_l + 1:index_r]
            line = line[index_r + 1:]
            # get vari_numarticle
            index_l = line.index('(')
            index_r = line.index(')')
            tree_vari_numarticle = line[index_l + 1:index_r]
            line = line[index_r + 1:]
            # get vari_numresouce
            index_l = line.index('(')
            index_r = line.index(')')
            tree_vari_numresouce = line[index_l + 1:index_r]
            line = line[index_r + 1:]
            # get vari_mSrN
            index_l = line.index('(')
            index_r = line.index(')')
            tree_vari_mSrN = line[index_l + 1:index_r]
            line = line[index_r + 1:]

            #get mSrc_list
            index_l = line.index('(')
            index_r = line.index(')')
            tree_mSrclist = line[index_l + 1:index_r]
            line = line[index_r + 1:]

            #get SrcN in storynode
            index_l = line.index('(')
            index_r = line.index(')')
            tree_nodeSrcN = line[index_l + 1:index_r]
            line = line[index_r + 1:]

            # get topickey
            index_l = line.index('(')
            index_r = line.index(')')
            tree_topickey = line[index_l + 1:index_r]
            line = line[index_r + 1:]


            # print(line)
            #��ȡ�ӽڵ���
            index_l = line.index('(')
            index_r = line.index(')')
            tree_undernum = line[index_l + 1:index_r]
            line = line[index_r + 1:]
            #print(tree_undernum)

            temp_list=[tree_name,tree_h,tree_et,tree_lt,tree_url,tree_undernum,tree_eventbasecode,
                       tree_eventcode,tree_resouceN,tree_totalresouceN,tree_avg_avgTone,tree_avg_goldsteinscale,
                       tree_avg_nummentions,tree_avg_numarticles,tree_avg_numresources,tree_totalbias,tree_mSrclist,
                       tree_titlename,tree_titlekeyword,tree_keyword,tree_maxCompatibility,tree_nodeSrcN,tree_topickey,
                       tree_mSrcName,tree_DocEventSim,tree_docDate,tree_corpusText,tree_filePath,tree_vari_avgtone,tree_vari_gold,
                       tree_vari_nummention,tree_vari_numarticle,tree_vari_numresouce,tree_vari_mSrN]
            # print('len', len(temp_list))

            treeNodeList.append(temp_list)

            # print(tree_resouceN)
    return treeNodeList



def read_tree_pro(filedir="test_data50"):
    print("read tree!!!!!!!")
    # tree_path="F:\\coding\\Event\\StoryForest\\test_data50\\stories.txt"
    tree_path=filedir+"/stories.txt"
    # tree_path = "test_data50/stories.txt"
    # tree_path = "storyteller/test_data50/stories.txt"
    # tree_path="test_data50/stories.txt"
    f = open(tree_path, 'r', encoding='latin1')
    textAll = f.readlines()
    IsTree_f = 0
    treeNodeList = []  # Ԫ�أ�[treename,tree����]
    for line in textAll:
        # print(len(line))
        line = line.replace("\n", "")
        line = line.replace("\t", "")
        # print(len(line))
        if len(line) == 0:  # ����
            if IsTree_f == 1:
                IsTree_f = 0
                break
            IsTree_f = 0
            continue
        if line[0] == '+':  # ��⵽����ʼ
            IsTree_f = 1
            # ��ȡ�ӽڵ���
            index_l = line.index('(')
            index_r = line.index(')')
            tree_undernum = line[index_l + 1:index_r]

            treeNodeList.append(
                [['ROOT'], 0, "time", "time", [["url"]], tree_undernum, 0, 0, 'null', 'null', 'null', 'null', 'null', 'null',
                 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null',
                 'null', 'null', 'null', 'null', [], [], []])  # �ɸ�Ϊtree name��summaryɶ��
            continue
        if IsTree_f == 1:
            tree_name = ""
            tree_h = 0
            tree_et = ""  # ����ʱ��
            tree_lt = ""
            tree_url = ""
            tree_resouceN = ""
            f_hei = 0
            # ��ȡh
            for str_c in line:
                if str_c == '|':
                    tree_h = tree_h + 1
                elif str_c == '+':
                    break

            # ��ȡname
            index_l = line.index('(')
            index_r = line.index(')')
            tree_name = line[index_l + 1:index_r]
            line = line[index_r + 1:]
            # ��ȡʱ��
            index_l = line.index('(')
            index_r = line.index(')')
            tree_time = line[index_l + 1:index_r]
            tree_et = tree_time.split('to')[0]
            tree_lt = tree_time.split('to')[1]
            line = line[index_r + 1:]  # ȥ���Ѷ�ȡ��time

            tree_titlename = []
            tree_url = []
            tree_eventcode = []
            tree_eventbasecode = []
            tree_titlekeyword = []
            tree_keyword = []
            tree_resouceN = []
            tree_mSrcName = []
            tree_DocEventSim = []
            tree_corpusText = []
            tree_docDate = []
            tree_filePath = []

            sep_keywordlist=[]
            sep_titlekeylist=[]

            sep_avgTone=[]
            sep_goldsteinscale=[]
            sep_nummentions=[]
            sep_numarticles=[]
            sep_numsources=[]

            sep_date=[]

            while (True):
                index_l = line.find('#')
                if index_l == -1:
                    break

                index_l = line.index('(')
                index_r = line.index(')')
                titlenamelist=line[index_l + 1:index_r].split('+')

                tree_titlename.append(titlenamelist)
                # tree_titlename = tree_titlename + '&' + line[index_l + 1:index_r]
                line = line[index_r + 1:]

                # ��ȡurl
                index_l = line.index('@')
                index_r = line.index('[')
                url_temp_str=line[index_l + 2:index_r]
                url_temp_list=url_temp_str.split(',')
                tree_url.append(url_temp_list)

                # ��ȡeventbasecode
                index_l = line.index('[')
                index_r = line.index(']')
                tree_eventbasecode.append(line[index_l + 1:index_r])
                # tree_eventbasecode = tree_eventbasecode + '&' +
                line = line[index_r + 1:]

                # ��ȡeventcode
                index_l = line.index('[')
                index_r = line.index(']')
                tree_eventcode.append(line[index_l + 1:index_r])
                # tree_eventcode = tree_eventcode + '&&&&&' +
                line = line[index_r + 1:]
                # print(tree_eventbasecode)

                # titlekeyword
                index_l = line.index('(')
                index_r = line.index(')')
                tree_titlekey_list=line[index_l + 1:index_r].split(',')
                tree_titlekey_list=tree_titlekey_list[0:len(tree_titlekey_list)-1]
                tree_titlekeyword.append(tree_titlekey_list)
                # tree_titlekeyword = tree_titlekeyword + '&' + line[index_l + 1:index_r]
                line = line[index_r + 1:]

                # keyword
                index_l = line.index('(')
                index_r = line.index(')')
                tree_keyword_list=line[index_l + 1:index_r].split(',')
                tree_keyword_list=tree_keyword_list[0:len(tree_keyword_list)-1]
                # print("keyword: "+tree_keyword_list[-1])
                tree_keyword.append(tree_keyword_list)
                # tree_keyword = tree_keyword + '&' + line[index_l + 1:index_r]
                line = line[index_r + 1:]

                # mSrcName
                index_l = line.index('(')
                index_r = line.index(')')
                tree_mSrcName.append(line[index_l + 1:index_r])
                # tree_mSrcName = tree_mSrcName + '&' + line[index_l + 1:index_r]
                line = line[index_r + 1:]

                # similarity
                index_l = line.index('(')
                index_r = line.index(')')
                tree_DocEventSim.append(line[index_l + 1:index_r])
                # tree_DocEventSim = tree_DocEventSim + '&' + line[index_l + 1:index_r]
                line = line[index_r + 1:]

                # publishTime aggregation date!!!
                index_l = line.index('(')
                index_r = line.index(')')
                docDatelist=line[index_l + 1:index_r].split('+')
                tree_docDate.append(docDatelist)
                line = line[index_r + 1:]

                # corpusText
                index_l = line.index('(')
                index_r = line.index(')')
                corpustTextList=line[index_l + 1:index_r].split("+@+")
                tree_corpusText.append(corpustTextList)
                # tree_corpusText = tree_corpusText + '&' + line[index_l + 1:index_r]
                line = line[index_r + 1:]

                # filePath
                index_l = line.index('(')
                index_r = line.index(')')
                filepathlist=line[index_l + 1:index_r].split('+')
                tree_filePath.append(filepathlist)
                # tree_corpusText = tree_corpusText + '&' + line[index_l + 1:index_r]
                line = line[index_r + 1:]

                # ��ȡ������Դ��
                # print(line)
                index_l = line.index('$')
                index_r = line.index(')')
                tree_resouceN_list=line[index_l + 2:index_r].split(',')  # $:
                tree_resouceN.append(tree_resouceN_list)
                # tree_resouceN = tree_resouceN + '&' + line[index_l + 2:index_r]  # $:

                line = line[index_r + 1:]

                #sep_keyword
                index_l = line.index('(')
                index_r = line.index(')')
                sep_keywordStr=line[index_l + 1:index_r]
                temp_list=sep_keywordStr.split('#')
                temp_keyword_list=[]
                for keywordStr in temp_list:
                    keywordlist=keywordStr.split('+')
                    temp_keyword_list.append(keywordlist)
                sep_keywordlist.append(temp_keyword_list)

                line = line[index_r + 1:]

                # sep_titlekey
                index_l = line.index('(')
                index_r = line.index(')')
                sep_keywordStr = line[index_l + 1:index_r]
                temp_list = sep_keywordStr.split('#')
                temp_titlekey_list=[]
                for keywordStr in temp_list:
                    keywordlist = keywordStr.split('+')
                    temp_titlekey_list.append(keywordlist)

                sep_titlekeylist.append(temp_titlekey_list)

                line = line[index_r + 1:]

                # sep_avgTone
                index_l = line.index('(')
                index_r = line.index(')')
                sep_Str = line[index_l + 1:index_r]
                sep_avgTone.append(sep_Str.split('+'))

                line = line[index_r + 1:]

                # sep_goldsteinscale
                index_l = line.index('(')
                index_r = line.index(')')
                sep_Str = line[index_l + 1:index_r]
                sep_goldsteinscale.append(sep_Str.split('+'))

                line = line[index_r + 1:]

                # sep_nummentions
                index_l = line.index('(')
                index_r = line.index(')')
                sep_Str = line[index_l + 1:index_r]
                sep_nummentions.append(sep_Str.split('+'))

                line = line[index_r + 1:]

                # sep_numarticles
                index_l = line.index('(')
                index_r = line.index(')')
                sep_Str = line[index_l + 1:index_r]
                sep_numarticles.append(sep_Str.split('+'))

                line = line[index_r + 1:]

                # sep_numsources
                index_l = line.index('(')
                index_r = line.index(')')
                sep_Str = line[index_l + 1:index_r]
                sep_numsources.append(sep_Str.split('+'))

                line = line[index_r + 1:]

                # sep_date
                index_l = line.index('(')
                index_r = line.index(')')
                sep_Str = line[index_l + 1:index_r]
                sep_list=sep_Str.split('+')
                sep_after_list=[]
                for temp_str in sep_list:
                    after_str=temp_str[0:4]+'-'+temp_str[4:6]+'-'+temp_str[6:]
                    sep_after_list.append(after_str)
                sep_date.append(sep_after_list)

                line = line[index_r + 1:]



            # ��ȡ������
            index_l = line.index('(')
            index_r = line.index(')')
            tree_maxCompatibility = line[index_l + 1:index_r]
            line = line[index_r + 1:]

            index_l = line.index('(')
            index_r = line.index(')')

            tree_totalresouceN = line[index_l + 1:index_r].split(',')
            line = line[index_r + 1:]

            # print('after totalresouceN',line)

            index_l = line.index('(')
            index_r = line.index(')')
            tree_avg_avgTone = line[index_l + 1:index_r].split(',')
            line = line[index_r + 1:]

            index_l = line.index('(')
            index_r = line.index(')')
            tree_avg_goldsteinscale = line[index_l + 1:index_r].split(',')
            line = line[index_r + 1:]

            index_l = line.index('(')
            index_r = line.index(')')
            tree_avg_nummentions = line[index_l + 1:index_r].split(',')
            line = line[index_r + 1:]

            index_l = line.index('(')
            index_r = line.index(')')
            tree_avg_numarticles = line[index_l + 1:index_r].split(',')
            line = line[index_r + 1:]

            index_l = line.index('(')
            index_r = line.index(')')
            tree_avg_numresources = line[index_l + 1:index_r].split(',')
            line = line[index_r + 1:]

            index_l = line.index('(')
            index_r = line.index(')')
            tree_totalbias = line[index_l + 1:index_r]
            line = line[index_r + 1:]
            # print('after bias',line)

            # get vari_avgTone
            index_l = line.index('(')
            index_r = line.index(')')
            tree_vari_avgtone = line[index_l + 1:index_r]
            line = line[index_r + 1:]

            # get vari_gold
            index_l = line.index('(')
            index_r = line.index(')')
            tree_vari_gold = line[index_l + 1:index_r]
            line = line[index_r + 1:]
            # get vari_nummention
            index_l = line.index('(')
            index_r = line.index(')')
            tree_vari_nummention = line[index_l + 1:index_r]
            line = line[index_r + 1:]
            # get vari_numarticle
            index_l = line.index('(')
            index_r = line.index(')')
            tree_vari_numarticle = line[index_l + 1:index_r]
            line = line[index_r + 1:]
            # get vari_numresouce
            index_l = line.index('(')
            index_r = line.index(')')
            tree_vari_numresouce = line[index_l + 1:index_r]
            line = line[index_r + 1:]
            # get vari_mSrN
            index_l = line.index('(')
            index_r = line.index(')')
            tree_vari_mSrN = line[index_l + 1:index_r]
            line = line[index_r + 1:]

            # get mSrc_list
            index_l = line.index('(')
            index_r = line.index(')')
            tree_mSrclist = line[index_l + 1:index_r].split(',')
            line = line[index_r + 1:]

            # get SrcN in storynode
            index_l = line.index('(')
            index_r = line.index(')')
            tree_nodeSrcN = line[index_l + 1:index_r].split(',')
            line = line[index_r + 1:]

            # get topickey
            index_l = line.index('(')
            index_r = line.index(')')
            tree_topickey = line[index_l + 1:index_r].split('+')
            tree_topickey.pop(0)  # str start with +,remove first null
            line = line[index_r + 1:]

            # print(line)
            # ��ȡ�ӽڵ���
            index_l = line.index('(')
            index_r = line.index(')')
            tree_undernum = line[index_l + 1:index_r]
            line = line[index_r + 1:]
            # print("sep_titlekeylist")
            # print(sep_titlekeylist)
            # for keylist in tree_keyword:
            #
            #     print("keyword len: "+str(len(keylist)))
            #     print(keylist)
            # print(tree_undernum)
            # Root??????????????
            temp_list = [tree_name, tree_h, tree_et, tree_lt, tree_url, tree_undernum, tree_eventbasecode,
                         tree_eventcode, tree_resouceN, tree_totalresouceN, tree_avg_avgTone, tree_avg_goldsteinscale,
                         tree_avg_nummentions, tree_avg_numarticles, tree_avg_numresources, tree_totalbias,
                         tree_mSrclist,
                         tree_titlename, tree_titlekeyword, tree_keyword, tree_maxCompatibility, tree_nodeSrcN,
                         tree_topickey,
                         tree_mSrcName, tree_DocEventSim, tree_docDate, tree_corpusText, tree_filePath,
                         tree_vari_avgtone, tree_vari_gold,
                         tree_vari_nummention, tree_vari_numarticle, tree_vari_numresouce, tree_vari_mSrN,
                         sep_keywordlist,sep_titlekeylist,sep_avgTone,sep_goldsteinscale,sep_nummentions,
                         sep_numarticles,sep_numsources,sep_date]
            # print('len', len(temp_list))

            treeNodeList.append(temp_list)

            # print(tree_resouceN)
    return treeNodeList

def GenJsonByTree(filetxt="test_data50",filename_pro="tree_pro.json",goalpath=''):    #���ݶ�ȡ���������ɶ�Ӧ��Json��ʽ
    #����json��Ӧ��Dict
    # o_path='../FrontEnd/public/helpers/'
    if goalpath=='':
        o_path=''
    else:
        o_path=goalpath

    # treeNodeList = read_tree()
    treeNodeList_pro = read_tree_pro(filetxt)
    # print(treeNodeList)
    print(len(treeNodeList_pro))
    # jsonDict={}
    jsonDict_pro={}
    # jsonDict=GenDictself(0,0,treeNodeList)
    jsonDict_pro=GenDictselfPro(0,0,treeNodeList_pro)
    # print(jsonDict)

    # f=open(o_path+filename,"w")
    # json.dump(jsonDict,f)
    # f.close()
    # print("json")
    # print(jsonDict_pro)
    f = open(o_path + filename_pro, "w")
    json.dump(jsonDict_pro, f)
    f.close()
    return jsonDict_pro

def GenDictselfPro(treeNodeIndex,current_h,treeNodeList):
    jsonDictSelf={}
    if current_h==0:
        jsonDictSelf["name"]="ROOT"
        jsonDictSelf["time_e"] = "time"
        jsonDictSelf["time_l"] = "time"
        jsonDictSelf["url"] = []
        jsonDictSelf["tree_topickey"] =[]
        jsonDictSelf["undernum"] = "null"
        jsonDictSelf["totalbias"] = "null"
        jsonDictSelf["tree_vari_avgTone"] ="null"
        jsonDictSelf["tree_vari_gold"] = "null"
        jsonDictSelf["tree_vari_nummention"] ="null"
        jsonDictSelf["tree_vari_numarticle"] = "null"
        jsonDictSelf["tree_vari_numresouce"] = "null"
        jsonDictSelf["tree_vari_mSrcN"] ="null"

        jsonDictSelf["mSrc_list"] = []
        jsonDictSelf["totalresource_n"] =[]
        jsonDictSelf["avg_avgTone"] =[]
        jsonDictSelf["avg_goldsteinscale"] =[]
        jsonDictSelf["avg_nummentions"] = []
        jsonDictSelf["avg_numarticles"] = []
        jsonDictSelf["avg_numresources"] =[]
        jsonDictSelf["tree_nodeSrcN"] =[]
        #
        jsonDictSelf["tree_mSrcName"] = []
        jsonDictSelf["resource_n"] = []
        jsonDictSelf["eventbasecode"] =[]
        jsonDictSelf["eventcode"] = []
        jsonDictSelf["tree_DocEventSim"] =[]
        # print(jsonDictSelf["tree_DocEventSim"])
        jsonDictSelf["tree_keyword"] = []
        jsonDictSelf["tree_titlekeyword"] =[]
        jsonDictSelf["tree_titlename"] = []
        jsonDictSelf["tree_filePath"] = []
        jsonDictSelf["tree_maxCompatibility"] = "null"
        jsonDictSelf["node_detail_info"] = []

        jsonDictSelf["tree_allkeyword"]=[]

    else:
        # print("treeNodeIndex:",treeNodeIndex)
        jsonDictSelf["name"]=treeNodeList[treeNodeIndex][0]
        #if sonDictSelf["name"]=="ROOT"
        jsonDictSelf["time_e"]=treeNodeList[treeNodeIndex][2]
        jsonDictSelf["time_l"]=treeNodeList[treeNodeIndex][3]
        jsonDictSelf["url"]=treeNodeList[treeNodeIndex][4]
        jsonDictSelf["tree_topickey"] = treeNodeList[treeNodeIndex][22]
        jsonDictSelf["undernum"]=treeNodeList[treeNodeIndex][5]
        jsonDictSelf["totalbias"] = treeNodeList[treeNodeIndex][15]
        jsonDictSelf["tree_vari_avgTone"] = treeNodeList[treeNodeIndex][28]
        jsonDictSelf["tree_vari_gold"] = treeNodeList[treeNodeIndex][29]
        jsonDictSelf["tree_vari_nummention"] = treeNodeList[treeNodeIndex][30]
        jsonDictSelf["tree_vari_numarticle"] = treeNodeList[treeNodeIndex][31]
        jsonDictSelf["tree_vari_numresouce"] = treeNodeList[treeNodeIndex][32]
        jsonDictSelf["tree_vari_mSrcN"] = treeNodeList[treeNodeIndex][33]

        jsonDictSelf["mSrc_list"] = treeNodeList[treeNodeIndex][16]
        jsonDictSelf["totalresource_n"] = treeNodeList[treeNodeIndex][9]
        jsonDictSelf["avg_avgTone"] = treeNodeList[treeNodeIndex][10]
        jsonDictSelf["avg_goldsteinscale"] = treeNodeList[treeNodeIndex][11]
        jsonDictSelf["avg_nummentions"] = treeNodeList[treeNodeIndex][12]
        jsonDictSelf["avg_numarticles"] = treeNodeList[treeNodeIndex][13]
        jsonDictSelf["avg_numresources"] = treeNodeList[treeNodeIndex][14]
        jsonDictSelf["tree_nodeSrcN"] = treeNodeList[treeNodeIndex][21]
        #
        jsonDictSelf["tree_mSrcName"] = treeNodeList[treeNodeIndex][23]
        jsonDictSelf["resource_n"] = treeNodeList[treeNodeIndex][8]
        jsonDictSelf["eventbasecode"]=treeNodeList[treeNodeIndex][6]
        jsonDictSelf["eventcode"]=treeNodeList[treeNodeIndex][7]
        jsonDictSelf["tree_DocEventSim"] = treeNodeList[treeNodeIndex][24]
        # print(jsonDictSelf["tree_DocEventSim"])
        jsonDictSelf["tree_keyword"] = treeNodeList[treeNodeIndex][19]
        jsonDictSelf["tree_titlekeyword"] = treeNodeList[treeNodeIndex][18]
        jsonDictSelf["tree_titlename"] = treeNodeList[treeNodeIndex][17]
        jsonDictSelf["tree_filePath"] = treeNodeList[treeNodeIndex][27]
        jsonDictSelf["tree_maxCompatibility"] = treeNodeList[treeNodeIndex][20]

        jsonDictSelf["tree_allkeyword"]=treeNodeList[treeNodeIndex][34]

        docDateList= treeNodeList[treeNodeIndex][25]
        corpusTextList= treeNodeList[treeNodeIndex][26]

        sep_keyword=treeNodeList[treeNodeIndex][34]
        sep_titlekey=treeNodeList[treeNodeIndex][35]

        sep_avgTone=treeNodeList[treeNodeIndex][36]
        sep_goldsteinscale=treeNodeList[treeNodeIndex][37]
        sep_nummentions=treeNodeList[treeNodeIndex][38]
        sep_numarticles=treeNodeList[treeNodeIndex][39]
        sep_numsources=treeNodeList[treeNodeIndex][40]
        sep_date=treeNodeList[treeNodeIndex][41]


        print("sep_titlekey")
        print(sep_titlekey)
        #add in root!!!

        #node_detail_info-------------------------------------------------------------------------------
        jsonDictSelf["node_detail_info"]=[]
        mSrcName_list=jsonDictSelf["tree_mSrcName"]#aggregation doc list
        mSrcIndex_dict={}

        mSrcindex_list=jsonDictSelf["mSrc_list"]  #four mSrclist
        # print("mSrclist: ",mSrcindex_list)
        mSrcAllinfo_list=[]
        path_list = []
        for i in range(len(mSrcindex_list)):
            mSrcIndex_dict[mSrcindex_list[i]]=i
            mSrcAllinfo_list.append([])


        #get info for each aggregation doc and aggregate in mSrc
        for i in range(len(mSrcName_list)):
            mSrc=mSrcName_list[i]
            print("mSrc: "+mSrc)
            if len(sep_titlekey[i])==1:# doc not aggregate
                mSrc_dict = {}

                titlelist = jsonDictSelf["tree_titlename"][i][0]
                urllist = jsonDictSelf["url"][i][0]
                # print("urllist: " + urllist)
                timelist = sep_date[i][0]
                corpusList = corpusTextList[i][0]
                pathlist = jsonDictSelf["tree_filePath"][i][0]

                topickeylist = jsonDictSelf["tree_topickey"]
                docKeyword = sep_keyword[i][0]
                docTitlekey = sep_titlekey[i][0]
                docSim = 0
                print("dockeyword")
                print(docKeyword)
                print("topickeylist")
                print(topickeylist)
                for keyw in docKeyword:
                    if keyw in topickeylist:
                        docSim = docSim + 1

                docSim = docSim / len(topickeylist)

                print(docSim)

                docEventSim =docSim

                doc_avgTone = sep_avgTone[i][0]
                doc_goldsteinscale = sep_goldsteinscale[i][0]
                doc_nummentions = sep_nummentions[i][0]
                doc_numarticles = sep_numarticles[i][0]
                doc_numsources = sep_numsources[i][0]

                mSrc_dict["titlelist"] = titlelist
                mSrc_dict["urllist"] = urllist
                mSrc_dict['timelist'] = timelist
                mSrc_dict["corpuslist"] = corpusList
                mSrc_dict["docEventSim"] = docEventSim
                mSrc_dict["pathlist"] = pathlist
                mSrc_dict["doc_keyword"]= docKeyword
                mSrc_dict["doc_titlekey"]=docTitlekey

                mSrc_dict["doc_avgTone"] = doc_avgTone
                mSrc_dict["doc_goldsteinscale"] = doc_goldsteinscale
                mSrc_dict["doc_nummentions"] = doc_nummentions
                mSrc_dict["doc_numarticles"] = doc_numarticles
                mSrc_dict["doc_numsources"] = doc_numsources
                index_i = mSrcIndex_dict[mSrc]
                mSrcAllinfo_list[index_i].append(mSrc_dict)


            else: # multi doc in one aggregate doc
                for j in range(len(jsonDictSelf["tree_titlename"][i])):
                    print(jsonDictSelf["tree_titlename"][i][j])
                    mSrc_dict={}
                    # print("j: "+str(j))
                    # print("titlename len "+str(len(jsonDictSelf["tree_titlename"][i])))
                    titlelist=jsonDictSelf["tree_titlename"][i][j]
                    urllist=jsonDictSelf["url"][i][j]
                    # print("urllist: "+urllist)
                    # print(docDateList[i])
                    timelist=sep_date[i][j]
                    corpusList=corpusTextList[i][j]
                    pathlist=jsonDictSelf["tree_filePath"][i][j]

                    topickeylist=jsonDictSelf["tree_topickey"]
                    docKeyword=sep_keyword[i][j]
                    # print(sep_titlekey[i])
                    # print(j)
                    docTitlekey=sep_titlekey[i][j]
                    docSim=0

                    for keyw in docKeyword:
                        if keyw in topickeylist:
                            docSim=docSim+1

                    docSim=docSim/len(topickeylist)

                    docEventSim=docSim

                    # print("len avgTone: "+str(len(sep_avgTone[i])))
                    doc_avgTone=sep_avgTone[i][j]
                    doc_goldsteinscale=sep_goldsteinscale[i][j]
                    doc_nummentions=sep_nummentions[i][j]
                    doc_numarticles=sep_numarticles[i][j]
                    doc_numsources=sep_numsources[i][j]

                    mSrc_dict["titlelist"]=titlelist
                    mSrc_dict["urllist"] = urllist
                    mSrc_dict['timelist'] =timelist
                    mSrc_dict["corpuslist"] = corpusList
                    mSrc_dict["docEventSim"]= docEventSim
                    mSrc_dict["pathlist"]= pathlist

                    mSrc_dict["doc_keyword"] = docKeyword
                    mSrc_dict["doc_titlekey"] = docTitlekey

                    mSrc_dict["doc_avgTone"] = doc_avgTone
                    mSrc_dict["doc_goldsteinscale"] = doc_goldsteinscale
                    mSrc_dict["doc_nummentions"] = doc_nummentions
                    mSrc_dict["doc_numarticles"] = doc_numarticles
                    mSrc_dict["doc_numsources"] = doc_numsources
                    # mSrc_dict["doc_keyword"]

            # print('mSrcIndex_dict,',mSrcIndex_dict)
                    index_i= mSrcIndex_dict[mSrc]
                    mSrcAllinfo_list[index_i].append(mSrc_dict)




        #sorted by docEventSim
        for i in range(len(mSrcindex_list)):

            sorted_list=sorted(mSrcAllinfo_list[i],key=lambda x:x["docEventSim"],reverse=True)
            if len(sorted_list)==0:
                continue
            temp_dict={}
            temp_dict["title"]=sorted_list[0]["titlelist"]
            temp_dict["time"]=sorted_list[0]["timelist"]
            temp_dict["url"]=sorted_list[0]["urllist"]
            temp_dict["lines"]=sorted_list[0]["corpuslist"]

            temp_dict["docEventSim"]=sorted_list[0]["docEventSim"]
            temp_dict["features"]=[sorted_list[0]["doc_avgTone"],sorted_list[0]["doc_goldsteinscale"],sorted_list[0]["doc_nummentions"],sorted_list[0]["doc_numarticles"],sorted_list[0]["doc_numsources"]]
            temp_dict["doc_keyword"]=sorted_list[0]["doc_keyword"]
            temp_dict["doc_titlekey"]=sorted_list[0]["doc_titlekey"]
            temp_dict["related_infos"]=[]

            for j in range(len(sorted_list)-1):
                temp_index=j+1
                temp_relate_dict={}
                temp_relate_dict["title"] = sorted_list[temp_index]["titlelist"]
                temp_relate_dict["time"] = sorted_list[temp_index]["timelist"]
                temp_relate_dict["url"] = sorted_list[temp_index]["urllist"]
                temp_relate_dict["lines"] = sorted_list[temp_index]["corpuslist"]

                temp_relate_dict["docEventSim"] = sorted_list[temp_index]["docEventSim"]

                temp_relate_dict["features"]=[sorted_list[temp_index]["doc_avgTone"],sorted_list[temp_index]["doc_goldsteinscale"],sorted_list[temp_index]["doc_nummentions"],sorted_list[temp_index]["doc_numarticles"],sorted_list[temp_index]["doc_numsources"]]
                temp_relate_dict["doc_keyword"]=sorted_list[temp_index]["doc_keyword"]
                temp_relate_dict["doc_titlekey"]=sorted_list[temp_index]["doc_titlekey"]

                temp_dict["related_infos"].append(temp_relate_dict)

            path_list.append(sorted_list[0]["pathlist"])

            jsonDictSelf["node_detail_info"].append(temp_dict)

        #get summary------------------------------------------------------------------
        # print('path_lsit',path_list)
        final_pathlist=[]
        for i in range(len(path_list)):


            catpath=path_list[i]

            if len(path_list[i])==0:
                continue
            temp_list=catpath.split('+')[0]
            final_pathlist.append(temp_list)
            # for temp_path in temp_list:
            #     path_list.append(temp_path)
            #     print(temp_path)


        # print('final_pathlist: ',final_pathlist)
        # str_summary=summarize_documents(final_pathlist)

        # jsonDictSelf["summary"]=str_summary


    #get children recursion------------------------------------------------------------------
    jsonDictSelf["children"]=[]
    #1.��ʼ��dict
    #2.�����м���children
        #��ǰnodetreeindex ��ǰ����
    i=treeNodeIndex+1   #can't be root
    while i<len(treeNodeList):
        if treeNodeList[i][1]==(current_h+1):  #����children
            jsonDictSelf["children"].append(GenDictselfPro(i,treeNodeList[i][1],treeNodeList))
            i=i+1
        elif treeNodeList[i][1]>(current_h+1):
            i=i+1
        elif treeNodeList[i][1]<(current_h+1):
            break
    return jsonDictSelf
def GenDictself(treeNodeIndex,current_h,treeNodeList):
    jsonDictSelf={}
    # print("treeNodeIndex:",treeNodeIndex)
    jsonDictSelf["name"]=treeNodeList[treeNodeIndex][0]
    #if sonDictSelf["name"]=="ROOT"
    jsonDictSelf["time_e"]=treeNodeList[treeNodeIndex][2]
    jsonDictSelf["time_l"]=treeNodeList[treeNodeIndex][3]
    jsonDictSelf["url"]=treeNodeList[treeNodeIndex][4]
    jsonDictSelf["undernum"]=treeNodeList[treeNodeIndex][5]
    jsonDictSelf["eventbasecode"]=treeNodeList[treeNodeIndex][6]
    jsonDictSelf["eventcode"]=treeNodeList[treeNodeIndex][7]
    jsonDictSelf["resource_n"]=treeNodeList[treeNodeIndex][8]
    jsonDictSelf["totalresource_n"]=treeNodeList[treeNodeIndex][9]
    jsonDictSelf["avg_avgTone"] = treeNodeList[treeNodeIndex][10]
    jsonDictSelf["avg_goldsteinscale"] = treeNodeList[treeNodeIndex][11]
    jsonDictSelf["avg_nummentions"] = treeNodeList[treeNodeIndex][12]
    jsonDictSelf["avg_numarticles"] = treeNodeList[treeNodeIndex][13]
    jsonDictSelf["avg_numresources"] = treeNodeList[treeNodeIndex][14]
    jsonDictSelf["totalbias"] = treeNodeList[treeNodeIndex][15]
    jsonDictSelf["mSrc_list"] = treeNodeList[treeNodeIndex][16]
    jsonDictSelf["tree_titlename"] = treeNodeList[treeNodeIndex][17]
    jsonDictSelf["tree_titlekeyword"] = treeNodeList[treeNodeIndex][18]
    jsonDictSelf["tree_keyword"] = treeNodeList[treeNodeIndex][19]
    jsonDictSelf["tree_maxCompatibility"] = treeNodeList[treeNodeIndex][20]
    jsonDictSelf["tree_nodeSrcN"] = treeNodeList[treeNodeIndex][21]
    jsonDictSelf["tree_topickey"] = treeNodeList[treeNodeIndex][22]
    jsonDictSelf["tree_mSrcName"] = treeNodeList[treeNodeIndex][23]
    jsonDictSelf["tree_DocEventSim"] = treeNodeList[treeNodeIndex][24]


    docDateList= treeNodeList[treeNodeIndex][25]
    corpusTextList= treeNodeList[treeNodeIndex][26]
    jsonDictSelf["tree_filePath"] = treeNodeList[treeNodeIndex][27]

    jsonDictSelf["tree_vari_avgTone"]=treeNodeList[treeNodeIndex][28]
    jsonDictSelf["tree_vari_gold"]=treeNodeList[treeNodeIndex][29]
    jsonDictSelf["tree_vari_nummention"]=treeNodeList[treeNodeIndex][30]
    jsonDictSelf["tree_vari_numarticle"]=treeNodeList[treeNodeIndex][31]
    jsonDictSelf["tree_vari_numresouce"]=treeNodeList[treeNodeIndex][32]
    jsonDictSelf["tree_vari_mSrcN"]=treeNodeList[treeNodeIndex][33]
    #add in root!!!

    #node_detail_info-------------------------------------------------------------------------------
    jsonDictSelf["node_detail_info"]=[]
    mSrcName_list=jsonDictSelf["tree_mSrcName"].split('&')[1:]#aggregation doc list
    mSrcIndex_dict={}

    mSrcindex_list=jsonDictSelf["mSrc_list"].split(',')  #four mSrclist
    print("mSrclist: ",mSrcindex_list)
    mSrcAllinfo_list=[]
    path_list = []
    for i in range(len(mSrcindex_list)):
        mSrcIndex_dict[mSrcindex_list[i]]=i
        mSrcAllinfo_list.append([])


    #get info for each aggregation doc and aggregate in mSrc
    for i in range(len(mSrcName_list)):
        mSrc=mSrcName_list[i]
        print("mSrc: "+mSrc)
        mSrc_dict={}

        titlelist=jsonDictSelf["tree_titlename"].split('&')[i+1]
        urllist=jsonDictSelf["url"].split('&')[i+1]
        print("urllist: "+urllist)
        timelist=docDateList[i]
        corpusList=corpusTextList[i]
        pathlist=jsonDictSelf["tree_filePath"][i]
        docEventSim=jsonDictSelf["tree_DocEventSim"].split('&')[i+1]

        mSrc_dict["titlelist"]=titlelist
        mSrc_dict["urllist"] = urllist
        mSrc_dict['timelist'] =timelist
        mSrc_dict["corpuslist"] = corpusList
        mSrc_dict["docEventSim"]= docEventSim
        mSrc_dict["pathlist"]= pathlist

        # print('mSrcIndex_dict,',mSrcIndex_dict)
        index_i= mSrcIndex_dict[mSrc]
        mSrcAllinfo_list[index_i].append(mSrc_dict)



    #sorted by docEventSim
    for i in range(len(mSrcindex_list)):

        sorted_list=sorted(mSrcAllinfo_list[i],key=lambda x:x["docEventSim"],reverse=True)
        if len(sorted_list)==0:
            continue
        temp_dict={}
        temp_dict["title"]=sorted_list[0]["titlelist"]
        temp_dict["time"]=sorted_list[0]["timelist"]
        temp_dict["url"]=sorted_list[0]["urllist"]
        temp_dict["lines"]=sorted_list[0]["corpuslist"]
        temp_dict["urls"]=[]
        temp_dict["docEventSims"]=[]


        path_list.append(sorted_list[0]["pathlist"])

        for j in range(len(sorted_list)):
            temp_dict["urls"].append(sorted_list[j]["urllist"])
            temp_dict["docEventSims"].append(sorted_list[j]["docEventSim"])
        for strc in temp_dict["urls"]:
            print("temp_dict url_list: " + strc)

        jsonDictSelf["node_detail_info"].append(temp_dict)

    #get summary------------------------------------------------------------------
    # print('path_lsit',path_list)
    final_pathlist=[]
    for i in range(len(path_list)):


        catpath=path_list[i]

        if len(path_list[i])==0:
            continue
        temp_list=catpath.split('+')[0]
        final_pathlist.append(temp_list)
        # for temp_path in temp_list:
        #     path_list.append(temp_path)
        #     print(temp_path)


    # print('final_pathlist: ',final_pathlist)
    # str_summary=summarize_documents(final_pathlist)

    # jsonDictSelf["summary"]=str_summary


    #get children recursion------------------------------------------------------------------
    jsonDictSelf["children"]=[]
    #1.��ʼ��dict
    #2.�����м���children
        #��ǰnodetreeindex ��ǰ����
    i=treeNodeIndex+1
    while i<len(treeNodeList):
        if treeNodeList[i][1]==(current_h+1):  #����children
            jsonDictSelf["children"].append(GenDictself(i,treeNodeList[i][1],treeNodeList))
            i=i+1
        elif treeNodeList[i][1]>(current_h+1):
            i=i+1
        elif treeNodeList[i][1]<(current_h+1):
            break
    return jsonDictSelf

    #3.���children�ݹ����
    #4.��������dict������

strList=[]
strList.append("graph TB")
def GenTreeMD():
    GenMDstrself(0,0)
    for str1 in strList:
        print(str1)

def GenMDstrself(treeNodeIndex,current_h):
    jsonMDstrBase="A"+str(treeNodeIndex)+"("+"\""+treeNodeList[treeNodeIndex][0]+"\""+")"+"-->"

    #1.��ʼ��basestr
    #2.�����м���children
        #��ǰnodetreeindex ��ǰ����
    i=treeNodeIndex+1
    while i<len(treeNodeList):
        if treeNodeList[i][1]==(current_h+1):  #����children
            tempstr=jsonMDstrBase+"A"+str(i)+"("+"\""+treeNodeList[i][0]+"\""+")"
            strList.append(tempstr)
            GenMDstrself(i,treeNodeList[i][1])
            i=i+1
        elif treeNodeList[i][1]>(current_h+1):
            i=i+1
        elif treeNodeList[i][1]<(current_h+1):
            break

DotStrList=[]
DotStrList.append("digraph G {")
DotStrList.append("rankdir=\"LR\"")
DotNodeList=[]
DotbranchList=[]
def GenTreeDot():
    GenDotstrself(0,0)
    DotStrList.extend(DotNodeList)
    DotStrList.extend(DotbranchList)
    print(DotbranchList)
    DotStrList.append("}")
    for str1 in DotStrList:
        print(str1)


def GenDotstrself(treeNodeIndex, current_h):

    strnode = "node_" + str(treeNodeIndex) + " [label=" + "\"" + treeNodeList[treeNodeIndex][0] + "\"" + "]"
    DotNodeList.append(strnode)
    strBranchBase = "node_"+str(treeNodeIndex)+" -> "
    # 1.��ʼ��basestr
    # 2.�����м���children
    # ��ǰnodetreeindex ��ǰ����
    i = treeNodeIndex + 1
    while i < len(treeNodeList):
        if treeNodeList[i][1] == (current_h + 1):  # ����children
            tempstr = strBranchBase + "node_" + str(i) +";"
            DotbranchList.append(tempstr)
            GenDotstrself(i, treeNodeList[i][1])
            i = i + 1
        elif treeNodeList[i][1] > (current_h + 1):
            i = i + 1
        elif treeNodeList[i][1] < (current_h + 1):
            break


if __name__=="__main__":
    # obj_dict={}
    # obj_dict["name"]="A"
    # obj_dict["children"]={"name":"B","children":{"name":"C","children":{}}}
    #print(transfer_json(obj_dict))

    #print(tree)
    #print(treeNodeList)
    GenJsonByTree()

    #GenTreeMD()

    #GenTreeDot()
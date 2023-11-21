#encoding=utf8
import json
import sys
# print(sys.path)
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.wordnet import WordNetLemmatizer
import string
import pandas as pd
# import gensim
# from gensim import corpora
import os
import regex as re
from nltk import word_tokenize, sent_tokenize, pos_tag

import numpy as np
import datetime
import string
# import keybertExtract
import pandas as pd
import ast
import shutil



from typing import Dict, List, Set, Tuple

import utils.config as config


TOPIC = config.TOPIC

PUNCTUATION = string.punctuation.replace('\'', '').replace('-','')  # Do not use apostrophe as a delimiter
stop_words = pd.read_csv('./keywordExtract/stopwords-en.txt', index_col=False, quoting=3, sep="\t", names=['stopword'],encoding='utf-8')
stop_words = stop_words['stopword'].values
# import io
# import sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
def preprocess_text(text):
    # 1.������Ϊ��ĸ����
    text = remove_numbers(text)
    text = remove_http(text)
    text = remove_punctuation(text)
    text = convert_to_lower(text)
    text = remove_white_space(text)
    text = remove_short_words(text)
    tokens = toknizing(text)
    # 2.POS tagging
    pos_map = {'J': 'a', 'N': 'n', 'R': 'r', 'V': 'v'}
    pos_tags_list = pos_tag(tokens)
    # print(pos_tags)
    # 3.Сд�任�ʹ��λ�ԭ
    lemmatiser = WordNetLemmatizer()
    tokens = [lemmatiser.lemmatize(w.lower(),
                                   pos=pos_map.get(p[0], 'v'))
              for w, p in pos_tags_list]
    #for strs in tokens:
        #if len(strs)>14:
            #print(strs)
    return tokens


def convert_to_lower(text):
    # Сдת��
    return text.lower()


def remove_numbers(text):
    # ��ȥ����
    #text = re.sub(r'\d+', '', text)
    return text


def remove_http(text):
    # ��ȥ��ַ
    text = re.sub("https?:\/\/t.co\/[A-Za-z0-9]*", ' ', text)
    return text


def remove_short_words(text):
    # ȥ������������ĸ�ĵ���
    #text = re.sub(r'\b\w{1,2}\b', '', text)
    return text


def remove_punctuation(text):
    # ȥ�����źͱ�����
    punctuations = '''!()[]{};?��?:'"\,`<>./?@=#$-(%^)+&[*_]|~'''
    no_punct = ""

    for char in text:
        if char not in punctuations:
            no_punct = no_punct + char
    return no_punct


def remove_white_space(text):
    # ȥ���ո�
    text = text.strip()
    return text


def toknizing(text):
    #stp = my_stopwords
    # stops = set(stopwords.words('english'))
    # stop_words = set(stops)    #ͣ�ô�û��storyForest�࣡��
    stop_words = pd.read_csv('./keywordExtract/stopwords-en.txt', index_col=False, quoting=3, sep="\t", names=['stopword'],encoding='utf-8')
    stop_words = stop_words['stopword'].values
    #print("len:",len(stop_words))
    tokens = word_tokenize(text)
    ## ��tokens��ȥ��ͣ�ô�

    result = [i for i in tokens if not i in stop_words]
    return result



# import rake

def corpus_load(filepath):
    #20220209Whoops
    #filelist = os.listdir(filepath)
    wordlist = []
    # rootpath='D:/coding/Event'
    # # print('cur_path',os.getcwd())
    # # print(filepath)
    # temp_path=filepath.split('/',2)[-1]
    # abpath=rootpath+'/'+temp_path

    print('file_path in corpusload',filepath)
    try:
        f = open(filepath, 'r', encoding='latin1', errors="ignore")  # ע�⣡��������

        textlist=f.readlines()
        textlist.pop(0)
        textlist.pop(0)

        url=textlist[0][:-1]
        textlist.pop(0)

        # print("in file:",file)
        ori_text=' '.join(textlist)
        wordlist = preprocess_text(ori_text)

        wordstring = ' '.join(wordlist)
        #corpus.append(wordstring)
        #ori_text=ori_text.replace('\n','')
        #ori_corpus.append(ori_text)
        f.close()
        #print(corpus_index)
        return [url,wordstring]
        # quit(1)
    except:
        print("corpus load error!!")
        return ['error','error']

def corpus_loadText(filepath):
    try:
        f = open(filepath, 'r', encoding='latin1', errors="ignore")  # ע�⣡��������

        textlist=f.readlines()
        textlist=textlist[3:5]
        # line = line.replace("\n", "")
        # line = line.replace("\t", "")
        # print("in file:",file)
        ori_text='   '.join(textlist)  #3 blank
        ori_text=ori_text.replace("\n","")




        f.close
        return ori_text
    except:
        print("loadText error!")
        return 'error'

def getIndexByFile(filename):  #�����ļ�����������
    #print("getting")
    filename=filename.split('.')[0] #ȥ�� txt
    #filename=' '.join(preprocess_text(filename))
    #print('filename:',filename)
    for i in range(len(titlelist)):
        # print('#'+titlelist[i])
        # print(filename.lower())
        if titlelist[i]==filename:
            return i
    print("error!")
    return "error!"
    ##exit(111)

def csvRead():
    key_path = "D:\\coding\\Event\\articles_with_keywords_Lemmatization_eventrootcode\\articles_with_keywords_Lemmatization_eventrootcode.csv"
    titlekey_path= "D:\\coding\\Event\\articles_with_keywords_Lemmatization_eventrootcode\\titles_with_keywords_Lemmatization_eventrootcode.csv"
    keydata=pd.read_csv(key_path,usecols=['title','keywords'])
    titlekeydata=pd.read_csv(titlekey_path,usecols=['title','keywords'])
    return  [keydata,titlekeydata]

#[keydata,titlekeydata]=csvRead()


def getKeyCsv(filename):
    #csv ����û�о�������

    filename=filename.split('.')[0]  #  ȥtxt��׺
    #print('filename in csvread', filename)

    for i in range(len(keydata['title'])):

        if keydata.iloc[i]['title']==filename:
            #print(keydata.iloc[i]['keywords'])
            #list_list=json.loads(keydata.iloc[i]['keywords'])
            list_list=ast.literal_eval(keydata.iloc[i]['keywords'])
            return list_list
def getKeytitleCsv(filename):
    #csv ����û�о�������
    filename = filename.split('.')[0]
    for i in range(len(titlekeydata['title'])):
        if titlekeydata.iloc[i]['title']==filename:
            #list_list=json.loads(titlekeydata.iloc[i]['keywords'])
            list_list=ast.literal_eval(titlekeydata.iloc[i]['keywords'])
            return list_list

def groupFinalkey(keylist,keynum):
    keydict={}
    #print('keylist: ',keylist)
    #ת��Ϊ�ֵ䣬��ͬ�ؼ��ʵ���
    for wturple in keylist:
        key=wturple.split(':')[0]
        if key in keydict:
            keydict[key]=keydict[key]+float(wturple.split(':')[-1])
        else:
            #print('wturple ',wturple)
            #print(wturple.split(':')[-1])
            keydict[key] = float(wturple.split(':')[-1])

    key_sort=sorted(keydict.items(),key=lambda  x: x[0],reverse=True)
    keySortDict=dict(key_sort)
    #print('keysortdict:  ',keySortDict)
    keystr=""

    dictlen=len(keySortDict)
    if dictlen < keynum:
        keynum=dictlen
        print("dict not long! length: ",dictlen)
    for i in range(keynum):
        if i !=0:
            keystr=keystr+','+list(keySortDict.keys())[i]
        else:
            keystr = list(keySortDict.keys())[i]

    return keystr





def readJsonBasecode(jsonName_list,file_path,class_num):
    baseCode_dict={}
    # class_str = 'Class_' + str(class_num)
    class_str=str(class_num)
    print('class_str:',class_str)
    for jsonName in jsonName_list:
        # print(jsonName)
        #class filter


        if class_str in jsonName and 'WithCorpus' in jsonName:
            # print('JsonName: ',jsonName)
            # print('class_str_ori: ',class_str)
            # class_str=class_str.split('_')
            # class_str=class_str[1]
            # print('class_str: ', class_str)
            jsonStr = jsonName.split('_')
            jsonStr=jsonStr[1]
            if len(class_str)==2: #class 11-20
                if len(jsonStr)==2:
                    continue
                if jsonStr[0]!=class_str[0] or jsonStr[1]!=class_str[1]:
                    continue

            else:   #class 1-9
                if jsonStr[0] != class_str:
                    continue

                if class_num==1:

                    if len(jsonStr)>2:
                        continue
                elif class_num==2:
                    if len(jsonStr)>3:
                        continue
                    if jsonStr[1]==0 and len(jsonStr)>2:
                        continue

            print(jsonName)
            f = open(os.sep.join([file_path, jsonName]), 'r', encoding='utf-8')
            jsondict = json.load(f)
            f.close()
            baseCode_dict.update(jsondict)
    # f = open('testjson2.json', 'w', encoding='utf-8')
    # json.dump(baseCode_dict, f, indent=4)
    # f.close()
    return baseCode_dict

def gencorpus(mSrc_list,time_scope,country_list,totalSrcDict):
    septotallist=[]
    timedict_sep={}

    # time_scope=ast.literal_eval(time_scope)
    # country_list=ast.literal_eval(country_list)

    time_e = int(time_scope[0].replace('-', ''))
    time_l = int(time_scope[1].replace('-', ''))

    for key in totalSrcDict.keys():
        # print('key:  ',key)
        # country filter
        if country_list[0]!="ALL":
            # print("need country filter")
            # print(country_list)
            f_key=0
            key_list=key.split('+')
            for key_country in key_list:
                # print("key_country:" ,key_country)
                # print("coutnry list:",country_list)
                if key_country in country_list:
                    # print("country in it")
                    f_key=1
                    break
            if f_key==0:
                print('country filter!')
                continue


        event_list = totalSrcDict[key]
        for elist in event_list:
            if len(elist) != 0:  # ������ǿ�
                edict = {}
                etitlelist = []
                for pathstr in elist:
                    # print('pathstr',pathstr)
                    pathlist = pathstr.split('+')
                    # print(pathlist)

                    date = pathlist[0]
                    date_int=int(pathlist[0])
                    if date_int>time_l or date_int< time_e:
                        print('time filter: ',date_int )
                        # print(time_e)
                        # print(time_l)
                        continue

                    path_str = pathlist[1]
                    title = path_str.split('/')[-1]  # /�и�����һ����ֻȡtitle��

                    print(pathlist[0:9])
                    eventbasecode = pathlist[2]
                    eventcode = pathlist[3]

                    avgTone_str = pathlist[4]
                    temp_index=avgTone_str.find('0')
                    avgTone=avgTone_str[temp_index:]
                    # print('avgTone: ',avgTone)

                    goldsteinscale_str=pathlist[5]
                    temp_index=goldsteinscale_str.find('0')
                    goldsteinscale=goldsteinscale_str[temp_index:]

                    # if goldsteinscale==0:
                    #     print("gold0!!!!!!")

                    nummentions_str = pathlist[6]
                    temp_index = nummentions_str.find('0')
                    nummentions = nummentions_str[temp_index:]
                    # print('nummentions: ',nummentions)

                    numarticles_str = pathlist[7]
                    temp_index = numarticles_str.find('0')
                    numarticles = numarticles_str[temp_index:]
                    # print('nummarticles: ', numarticles)

                    numsources_str = pathlist[8]
                    temp_index = numsources_str.find('0')
                    numsources = numsources_str[temp_index:]
                    # print('numsouce',numsources)

                    keywordstr = pathlist[10]
                    # print("keywordstr: ",keywordstr)
                    key_list = ast.literal_eval(keywordstr)
                    print('keyread len : ',len(key_list))
                    print(key_list)

                    titlekeystr = pathlist[12]
                    titlekey_list = ast.literal_eval(titlekeystr)

                    resource_name=pathlist[-1]  #add in genArticleGroup
                    # print('resouce_n:',resource_name)
                    # if resource_name == 'menafn.com':
                    #     print('has men!!!!!!')


                    # #�޶�һ�·���debug
                    # if pathstr.split('/')[-2]!= "en-ae":
                    #     continue

                    # ·������
                    path_list = path_str.split('/')
                    path_list.pop(0)
                    path_finalstr = '/'.join(path_list)
                    path_finalstr='preprocess/'+path_finalstr
                    path_finalstr = '../../' + path_finalstr

                    etitlelist.append({'title': title, 'path_str': path_finalstr, 'titlekeylist': titlekey_list,
                                       'keywordlist': key_list, 'date': date, 'eventbasecode': eventbasecode,
                                       'eventcode': eventcode, 'resource_n': resource_name, 'avgTone':avgTone,
                                       'goldsteinscale': goldsteinscale,'nummentions': nummentions,'numarticles':numarticles,
                                       'numsources': numsources})
                # ֻ�轫����list�ϲ�һ�¼���
                if len(etitlelist) == 0:
                    continue

                print("title in grouping: ")
                #initial all with the first doc
                path_finalstr = etitlelist[0]['path_str']
                res_list = corpus_load(path_finalstr)
                corpus_text= corpus_loadText(path_finalstr)
                edict['date'] = etitlelist[0]['date']
                edict['corpus'] = res_list[1]
                edict['url'] = res_list[0]
                edict['title'] = etitlelist[0]['title']
                edict['eventbasecode'] = etitlelist[0]['eventbasecode']
                edict['eventcode'] = etitlelist[0]['eventcode']
                edict['corpusText']= corpus_text
                edict['resource_n'] = []
                edict["file_path"] = path_finalstr


                sep_keyword_list=etitlelist[0]["keywordlist"]
                sep_keyword_list_after=[]
                for wturple in sep_keyword_list:
                    keystr_temp=wturple.split(':')[0]
                    sep_keyword_list_after.append(keystr_temp)
                    edict["sep_keyword"]="+".join(sep_keyword_list_after)

                sep_titlekey_list=etitlelist[0]["titlekeylist"]
                sep_titlekey_list_after=[]
                for wturple in sep_titlekey_list:
                    keystr_temp=wturple.split(':')[0]
                    sep_titlekey_list_after.append(keystr_temp)
                    edict["sep_titlekey"]="+".join(sep_titlekey_list_after)

                for mSrc_n in mSrc_list:

                    if etitlelist[0]['resource_n']==mSrc_n:
                        edict['resource_n'].append(1)
                    else:
                        edict['resource_n'].append(0)

                # edict['resource_n'] = etitlelist[0]['resource_n']
                edict['avgTone']=[]
                for mSrc_n in mSrc_list:
                    if etitlelist[0]['resource_n'] == mSrc_n:
                        edict['avgTone'].append(float(etitlelist[0]['avgTone']))
                    else:
                        edict['avgTone'].append(0)

                edict['goldsteinscale'] = []
                for mSrc_n in mSrc_list:
                    if etitlelist[0]['resource_n'] == mSrc_n:
                        edict['goldsteinscale'].append(float(etitlelist[0]['goldsteinscale']))
                    else:
                        edict['goldsteinscale'].append(0)

                edict['nummentions'] = []
                for mSrc_n in mSrc_list:
                    if etitlelist[0]['resource_n'] == mSrc_n:
                        edict['nummentions'].append(float(etitlelist[0]['nummentions']))
                    else:
                        edict['nummentions'].append(0)

                edict['numarticles'] = []
                for mSrc_n in mSrc_list:
                    if etitlelist[0]['resource_n'] == mSrc_n:
                        # print(etitlelist[0])
                        edict['numarticles'].append(float(etitlelist[0]['numarticles']))
                    else:
                        edict['numarticles'].append(0)

                edict['numsources'] = []
                for mSrc_n in mSrc_list:
                    if etitlelist[0]['resource_n'] == mSrc_n:
                        edict['numsources'].append(float(etitlelist[0]['numsources']))
                    else:
                        edict['numsources'].append(0)

                edict["sep_avgTone"]=etitlelist[0]["avgTone"]
                edict["sep_goldsteinscale"]=etitlelist[0]["goldsteinscale"]
                edict["sep_nummentions"]=etitlelist[0]["nummentions"]
                edict["sep_numarticles"]=etitlelist[0]["numarticles"]
                edict["sep_numsources"]=etitlelist[0]["numsources"]






                # edict['avgTone'] = float(etitlelist[0]['avgTone'])/len(etitlelist) #�ӵĶ��ǳ��õģ�������Ϊƽ����
                # edict['goldsteinscale'] = float(etitlelist[0]['goldsteinscale'])/len(etitlelist)
                # edict['nummentions'] = float(etitlelist[0]['nummentions'])/len(etitlelist)
                # edict['numarticles'] = float(etitlelist[0]['numarticles'])/len(etitlelist)
                # edict['numsources'] = float(etitlelist[0]['numsources'])/len(etitlelist)

                # need add: doc_key doc_titlekey doc_avg...

                #Root����ʾ����Դlist
                #�����ĵ��Ĺؼ��ʺͱ���ؼ���
                #bias���������ⰴ����Դ�ۺϣ�ǰ�߱�Ϊavg�����߱�Ϊlist
                #��������Ҫ��һ����Ե�

                # print(edict)
                keyGroupList = []

                titlekeyGroupList = []
                # str תΪlist
                keyGroupList.extend(etitlelist[0]['keywordlist'])
                titlekeyGroupList.extend(etitlelist[0]['titlekeylist'])

                # print('keygrouplist: ',keyGroupList)

                # ��ȡcsv�ļ���key ��titile key����Ȩֵ��
                # һ���¼�����keyword��ȡ����ٸ���Ȩֵ��ȡ20��key��5��key

                # f_titlekey = titlekeylist[f_index]
                # f_key = keywordlist[f_index]
                # ��grouping������lda
                # f_lda = ldalist[f_index]

                # ����ʱ������
                f_time = etitlelist[0]['date']
                if f_time in timedict_sep:
                    timedict_sep[f_time].append(len(septotallist))  # ���ӵ�ǰ����
                else:
                    timedict_sep[f_time] = [len(septotallist)]

                for i in range(len(etitlelist) - 1):
                    # ������Ϣ
                    # print(edict)
                    temp_index = i + 1
                    # if temp_index =='error!':
                    #    #print("error!")
                    #     continue


                    [temp_url, temp_corpus] = corpus_load(etitlelist[temp_index]['path_str'])
                    temp_corpusText= corpus_loadText(etitlelist[temp_index]['path_str'])
                    if temp_url=='error':
                         continue
                    if temp_corpusText=='error':
                        continue
                    # no dif media aggregate anymore
                    edict['corpus'] = edict['corpus'] + " " + temp_corpus
                    edict['title'] = edict['title'] + "+" + etitlelist[temp_index]['title']
                    edict["date"]=edict["date"]+"+"+etitlelist[temp_index]["date"]
                    edict['url'] = edict['url'] + "," + temp_url
                    edict['corpusText']=edict['corpusText']+ " +@+ "+ temp_corpusText
                    edict["file_path"] = edict["file_path"] +"+"+etitlelist[temp_index]['path_str']



                    sep_keyword_list = etitlelist[temp_index]["keywordlist"]
                    sep_keyword_list_after=[]
                    for wturple in sep_keyword_list:
                        keystr_temp = wturple.split(':')[0]
                        sep_keyword_list_after.append(keystr_temp)

                    edict["sep_keyword"] = edict["sep_keyword"] + "#" + "+".join(sep_keyword_list_after)

                    sep_titlekey_list = etitlelist[0]["titlekeylist"]
                    sep_titlekey_list_after=[]
                    for wturple in sep_titlekey_list:
                        keystr_temp = wturple.split(':')[0]
                        sep_titlekey_list_after.append(keystr_temp)
                    edict["sep_titlekey"]=edict["sep_titlekey"]+"#"+"+".join(sep_titlekey_list_after)

                    edict["sep_avgTone"] =edict["sep_avgTone"]+"+"+ etitlelist[temp_index]["avgTone"]
                    edict["sep_goldsteinscale"] =edict["sep_goldsteinscale"]+"+"+ etitlelist[temp_index]["goldsteinscale"]
                    edict["sep_nummentions"] = edict["sep_nummentions"]+"+"+ etitlelist[temp_index]["nummentions"]
                    edict["sep_numarticles"] = edict["sep_numarticles"]+"+"+ etitlelist[temp_index]["numarticles"]
                    edict["sep_numsources"] = edict["sep_numsources"]+"+"+ etitlelist[temp_index]["numsources"]

                    for i in range(len(mSrc_list)):
                        mSrc_n=mSrc_list[i]
                        # if mSrc_n=="menafn":
                            # print("in menafn")
                        if etitlelist[temp_index]['resource_n'] == mSrc_n:
                            # print("count menafn")
                            edict['resource_n'][i]=1+edict['resource_n'][i]
                            edict['avgTone'][i]=float(etitlelist[temp_index]['avgTone'])+edict['avgTone'][i]
                            edict['goldsteinscale'][i] = float(etitlelist[temp_index]['goldsteinscale']) + edict['goldsteinscale'][i]
                            edict['nummentions'][i] = float(etitlelist[temp_index]['nummentions']) + edict['nummentions'][i]
                            edict['numarticles'][i] = float(etitlelist[temp_index]['numarticles']) + edict['numarticles'][i]
                            edict['numsources'][i] = float(etitlelist[temp_index]['numsources']) + edict['numsources'][i]





                    # src_n_list=edict['resource_n'].split(',')
                    # if etitlelist[temp_index]['resource_n'] not in src_n_list:
                    #     edict['resource_n']= edict['resource_n']+','+etitlelist[temp_index]['resource_n']




                    keyGroupList.extend(etitlelist[temp_index]['keywordlist'])
                    titlekeyGroupList.extend(etitlelist[temp_index]['titlekeylist'])

                edict['titlekey'] = groupFinalkey(titlekeyGroupList, 5)
                # edict['key']=f_key
                # edict['key'] = groupFinalkey(keyGroupList, 15)
                edict['key'] = groupFinalkey(keyGroupList, 20)

                for i in range(len(mSrc_list)):
                    mSrc_n = mSrc_list[i]
                    if edict['resource_n'][i]!=0:
                        edict['avgTone'][i]=edict['avgTone'][i]/edict['resource_n'][i]
                        edict['goldsteinscale'][i] = edict['goldsteinscale'][i] / edict['resource_n'][i]
                        edict['nummentions'][i] = edict['nummentions'][i] / edict['resource_n'][i]
                        edict['numarticles'][i] = edict['numarticles'][i] / edict['resource_n'][i]
                        edict['numsources'][i] = edict['numsources'][i] / edict['resource_n'][i]


                septotallist.append(edict)
    return [septotallist,timedict_sep]

def genArticleGroup(grouppath,mSrc_list,class_num,totalSrcDict):
    docn_list=[]
    for mSrc_n in mSrc_list:
        resource_name = mSrc_n
        print('in mSrc:',mSrc_n)
        groupjsonpath=os.sep.join([grouppath, mSrc_n])
        print(groupjsonpath,'!!!!!!')
        groupfiles=os.listdir(groupjsonpath)  #������Դ�ļ���
        baseCode_json = readJsonBasecode(groupfiles, groupjsonpath, class_num) #get all classnum spec json in one mSrc
    #groupfiles = os.listdir(os.sep.join([grouppath, file]))

    # for file_res in groupfiles:
        # resource_name=file_res
        # file_res_path=os.sep.join([grouppath, file_res])
        # file_dicts=os.listdir(file_res_path)
        #
        #
        #
        # baseCode_json= readJsonBasecode(file_dicts,file_res_path,class_num)


        # file_dict=file_dicts[0]  #�ݶ�ֻ��һ������
        # # print(file_dict)
        # # print(resource_name)
        # f = open(os.sep.join([file_res_path, file_dict]), 'r', encoding='utf-8')
        # jsondict = json.load(f)
        # f.close()
        jsondict=baseCode_json

        #cal the docnum of mSrc
        doc_num=0
        for key in jsondict.keys():
            for earray in jsondict[key]:
                for edoc in earray:
                    doc_num=1+doc_num
        docn_list.append(doc_num)

        for key in jsondict.keys():
            temp_array = []
            if key not in totalSrcDict.keys():
                for earray in jsondict[key]: #ÿ���¼�

                    if len(earray)==0:
                        continue
                    else:
                        for i in range(len(earray)):
                            earray[i]=earray[i]+'+'+resource_name #�ַ���
                            # if resource_name=='menafn.com':
                            #     print('has men!!')
                    temp_array.append(earray)
                totalSrcDict.update({key:temp_array})
                # if key=='UKR+RUS+18':
                #     print('UKR+RUS+18',temp_array)
            else:

                for earray in jsondict[key]:
                    match_f=0
                    if len(earray) == 0:
                        continue
                    else:
                        for i in range(len(earray)):
                            earray[i] = earray[i] + '+' + resource_name
                            # if resource_name=='menafn.com':
                            #     print('has men!!!!')
                        json_time = int(earray[0].split('+')[0])
                    for i in range(len(totalSrcDict[key])):
                        srcearray=totalSrcDict[key][i]
                        src_time = int(srcearray[0].split('+')[0])
                        abs_res = abs(json_time - src_time)
                        # if abs_res <= 7:  # �ۺ�
                        #     totalSrcDict[key][i].extend(earray)
                        #     match_f=1
                        #     break

                    if match_f==0:
                        temp_array.append(earray)


                    # temp_array.append(earray)
                    # if key == 'UKR+RUS+18':
                    #     print(temp_array)
                for srcearray in totalSrcDict[key]:
                    temp_array.append(srcearray)

                totalSrcDict[key]=temp_array
    return docn_list

def mergeTxt():
    dirpath="testinput_basecode"
    o_path=os.sep.join([dirpath,"class18"])

    if os.path.exists(o_path):
        shutil.rmtree(o_path)
    os.mkdir(o_path)
    classfile_list=os.listdir(dirpath)
    txt_dict={}
    print(classfile_list)
    # 1.get all the datetxtname list and merge it
    #2. accord to the datetxtname list to merge txt

    for classfile_name in classfile_list:
        if 'test' in classfile_name:#filter the wanted filedir
            filedir=os.sep.join([dirpath,classfile_name])
            txtname_list=os.listdir(filedir)
            for txt_name in txtname_list:
                txt_path=os.sep.join([filedir,txt_name])
                if txt_name not in txt_dict:
                    txt_dict[txt_name]=[txt_path]
                else:
                    txt_dict[txt_name].append(txt_path)

    dictname_sort = sorted(txt_dict.items(), key=lambda x: x[0], reverse=False)

    txt_dict_sort = dict(dictname_sort)
    print(txt_dict_sort)

    for txt_key in list(txt_dict_sort.keys()):
        ost_txt_path=os.sep.join([o_path,txt_key])
        o_f=open(ost_txt_path,'w')
        o_list=[]

        if len(txt_dict_sort[txt_key])>1:
            print(txt_dict_sort[txt_key])


        for src_path in txt_dict_sort[txt_key]:
            src_f=open(src_path,'r')
            templist=src_f.readlines()
            if len(o_list)!=0:
                templist.pop(0)
                o_list.extend(templist)
            else:
                o_list.extend(templist)
            src_f.close()
        o_f.writelines(o_list)
        o_f.close()







def genStoryForestInputMulti(time_scope,mSrc_list,classnum,country_list):
    # 遍历testinput_basecode文件夹下的子文件夹，删除.txt文件

    root_dir = "./testinput_basecode/"
    sub_dirs = os.listdir(root_dir)
    for ele in sub_dirs:
        shutil.rmtree(root_dir + ele)  
        os.mkdir(root_dir + ele)

    # class_list = ast.literal_eval(classnum)
    class_list = classnum
    for class_code in class_list:
        genStoryForestInput(time_scope,mSrc_list,class_code, country_list)
    mergeTxt()



def genStoryForestInput(time_scope,mSrc_list,classnum,country_list):
    totalGroupList = []
    totalTimeList = []
    totalSrcDict = {}
    o_path = "testinput_basecode"
    # o_path = "storyteller/testinput_basecode"

    # grouppath = "..//..//preprocess\\news_processing\\results\\same_events_class_EventCode"
    grouppath = "../../preprocess/news_processing/results2/" + TOPIC +"/same_events_class_EventCode"
    

    # mSrc_list=ast.literal_eval(mSrc_list)


    class_num = int(classnum)

    print('class:', class_num)

    print('country_list:',country_list)
    docn_list = genArticleGroup(grouppath, mSrc_list, class_num,totalSrcDict)

    print("docn_list",docn_list)
    temp_count=0
    for docn in docn_list:
        temp_count=temp_count+docn
    print(temp_count)


    print('lendict', len(totalSrcDict))
    event_num = 0
    for key in totalSrcDict:
        for event_list in totalSrcDict[key]:
            for event in event_list:
                event_num = event_num + 1
    # print(totalSrcDict)
    print(event_num)
    f = open('testjson1.json', 'w', encoding='utf-8')
    json.dump(totalSrcDict, f, indent=4)
    f.close()
    [septotallist, timedict_sep] = gencorpus(mSrc_list, time_scope, country_list,totalSrcDict)

    corpus = []
    print('len septotallist',len(septotallist))
    for edict in septotallist:
        # �����Ͻ���Ԥ����
        temp_corpus = edict['corpus']
        temp_token = preprocess_text(temp_corpus)
        corpus.append(' '.join(temp_token))
    print('lencorpus', len(corpus))



    print("begin lda")
    num_key = 20  # ǰ��λ
    corpus_lda=[ corpus_single.split() for corpus_single in corpus] #��list��ÿ��corpus stringת��Ϊ����list
    # dictionary = corpora.Dictionary(corpus_lda)

    # # ʹ������Ĵʵ䣬��ת���ĵ��б������ϣ���� DT ����
    # doc_term_matrix = [dictionary.doc2bow(doc) for doc in corpus_lda]
    #
    # # ʹ�� gensim ������ LDA ģ�Ͷ���
    # Lda = gensim.models.ldamodel.LdaModel

    # �� DT ���������к�ѵ�� LDA ģ��
    # num_topic=20
    # ldamodel = Lda(doc_term_matrix, num_topics=num_topic, id2word=dictionary, passes=1)   #������Ϊ1����debug



    # ���lda
    for i in range(len(corpus_lda)):
        # doc_bow = dictionary.doc2bow(corpus_lda[i])
        # doc_lda = ldamodel[doc_bow]
        templist=["0"]*20
        # for temptuple in doc_lda:
        #     templist[temptuple[0]]=str(temptuple[1])

        septotallist[i]['lda']=','.join(templist)






    print("begin writing")
    #print(len(corpus))
    #print(len(keywordlist))
    print("time num:",len(timedict_sep.keys()))
    print(timedict_sep)
    time_sort = sorted(timedict_sep.items(), key=lambda x: x[0], reverse=False)
    timedict_sort=dict(time_sort)
    class_n='testclass'+str(class_num)
    # class_n = 'class' + '18'
    o_path_sep=os.sep.join([o_path,class_n])
    if os.path.exists(o_path_sep):
        shutil.rmtree(o_path_sep)
    os.mkdir(o_path_sep)
    #print(timedict)
    #o_path="G:\\testinput_test"
    #o_path = "G:\\testinput_phra"
    #o_path="testinput"
    #�Ƿ�Ϊ���� (��ҪDF)
    for timename in timedict_sort.keys():

        index_list = timedict_sort[timename]
        if len(index_list)==0:
            continue

        #�ļ�������
        timestr='-'.join([timename[0:4],timename[4:6],timename[6:]])
        time_stamp=datetime.datetime(int(timename[0:4]),int(timename[4:6]),int(timename[6:]))
        time_stamp=str(time_stamp.timestamp())
        f=open(os.sep.join([o_path_sep,timestr+'.txt']),'w',encoding='utf-8')
        #f = open('testinput_1.txt', 'w')
        #f.write("id|segment_title|keywords|LDA|time|original\n")
        f.write("id|segment_title|titlekeys|keywords|LDA|time|original|url|eventbasecode|eventcode|resouce_n|avgTone|goldsteinscale|"
                "nummentions|numarticles|numsources|mSrc_list|docn_list|mSrcName|corpusText|filePath|sep_keyword|sep_titlekey|sep_avgTone|"
                "sep_goldsteinscale|sep_nummentions|sep_numarticles|sep_numsources|date\n")
        #f.write("id|segment_title|keywords|DF|LDA|time|original\n")

        for index_corpus in index_list:

            temp_id=index_corpus+1000*class_num# ��0����
            temp_original=septotallist[index_corpus]['corpus']
            temp_titlekeys=septotallist[index_corpus]['titlekey']
            temp_keywords=septotallist[index_corpus]['key']
            #�����һ��nlp������ȥtxt��׺

            #print("segtitle1: ",temp_segtitle)
            temp_segtitle = septotallist[index_corpus]['title'] #�������title
            temp_segtitle_list=septotallist[index_corpus]['title'].split('+') #ֻȡ��һ��
            #print("segtitle2: ", temp_segtitle)
            for i in range(len(temp_segtitle_list)):
                temp_segtitle_list[i]=temp_segtitle_list[i].split('.')[0]
            temp_segtitle='+'.join(temp_segtitle_list)

            # temp_segtitle=temp_segtitle.split('.')[0] #ȥtxt��׺
            #
            #ȥ����ֻʣ��һ��������
            # temp_segtitle_token=preprocess_text(temp_segtitle)
            # temp_segtitle=' '.join(temp_segtitle_token)   #��title����nlp����

            temp_lda = septotallist[index_corpus]['lda']
            #url�������
            temp_url = septotallist[index_corpus]['url']#.split(',')[0] #ֻȡ��һ��
            temp_eventbasecode = septotallist[index_corpus]['eventbasecode']
            temp_eventcode = septotallist[index_corpus]['eventcode']

            #���䣡��
            resouce_n=septotallist[index_corpus]['resource_n']
            temp_resouce=str(resouce_n[0])
            for i in range(len(resouce_n)-1):
                temp_resouce=temp_resouce+','+str(resouce_n[i+1])
            # print('resouce_n:',resouce_n)
            # print(temp_resouce)

            temp_avgTone_list = septotallist[index_corpus]['avgTone']
            temp_avgTone = str(temp_avgTone_list[0])
            for i in range(len(temp_avgTone_list) - 1):
                temp_avgTone = temp_avgTone + ',' + str(temp_avgTone_list[i + 1])

            temp_goldsteinscale_list = septotallist[index_corpus]['goldsteinscale']
            temp_goldsteinscale = str(temp_goldsteinscale_list[0])
            for i in range(len(temp_goldsteinscale_list) - 1):
                temp_goldsteinscale = temp_goldsteinscale + ',' + str(temp_goldsteinscale_list[i + 1])

            temp_nummentions_list = septotallist[index_corpus]['nummentions']
            temp_nummentions = str(temp_nummentions_list[0])
            for i in range(len(temp_nummentions_list) - 1):
                temp_nummentions = temp_nummentions + ',' + str(temp_nummentions_list[i + 1])

            temp_numarticles_list = septotallist[index_corpus]['numarticles']
            temp_numarticles = str(temp_numarticles_list[0])
            for i in range(len(temp_numarticles_list) - 1):
                temp_numarticles = temp_numarticles + ',' + str(temp_numarticles_list[i + 1])

            temp_numsources_list = septotallist[index_corpus]['numsources']
            temp_numsources = str(temp_numsources_list[0])
            for i in range(len(temp_numsources_list) - 1):
                temp_numsources = temp_numsources + ',' + str(temp_numsources_list[i + 1])

            # temp_avgTone = str(septotallist[index_corpus]['avgTone'])
            # temp_goldsteinscale = str(septotallist[index_corpus]['goldsteinscale'])
            # temp_nummentions = str(septotallist[index_corpus]['nummentions'])
            # temp_numarticles = str(septotallist[index_corpus]['numarticles'])
            # temp_numsources = str(septotallist[index_corpus]['numsources'])

            temp_mSrc_list=mSrc_list[0]
            for i in range(len(mSrc_list)-1):
                temp_mSrc_list=temp_mSrc_list+','+mSrc_list[i+1]
            temp_docn_list=str(docn_list[0])
            for i in range(len(docn_list)-1):
                temp_docn_list=temp_docn_list+','+str(docn_list[i+1])

            for i in range(len(resouce_n)):
                if resouce_n[i]!=0:
                    # print('in mSrcName:')
                    # print(resouce_n)
                    # print(mSrc_list[i])
                    temp_mSrcName=mSrc_list[i]
                    break
            # if temp_resouce =="tass.com":
            #     print("goal!!!!!!!!!!!!!!!!!")
            #temp_DF=DF_list[index_corpus]

            #add corpusText
            temp_corpusText=septotallist[index_corpus]['corpusText']

            #add file_path
            temp_filepath=septotallist[index_corpus]["file_path"]

            temp_sep_keywordlist=septotallist[index_corpus]["sep_keyword"]
            temp_sep_titlekey = septotallist[index_corpus]["sep_titlekey"]

            temp_sep_avgTone=septotallist[index_corpus]["sep_avgTone"]
            temp_sep_goldsteinscale = septotallist[index_corpus]["sep_goldsteinscale"]
            temp_sep_nummentions = septotallist[index_corpus]["sep_nummentions"]
            temp_sep_numarticles = septotallist[index_corpus]["sep_numarticles"]
            temp_sep_numsources = septotallist[index_corpus]["sep_numsources"]

            temp_date= septotallist[index_corpus]["date"]
            print("test out",temp_titlekeys,temp_mSrcName,temp_corpusText)
            str_corpus = "|".join([str(temp_id), temp_segtitle,temp_titlekeys, temp_keywords, temp_lda,
                                   time_stamp, temp_original,temp_url,temp_eventbasecode,temp_eventcode,
                                   temp_resouce,temp_avgTone,temp_goldsteinscale,temp_nummentions,temp_numarticles,
                                   temp_numsources,temp_mSrc_list,temp_docn_list,temp_mSrcName,temp_corpusText,
                                   temp_filepath,temp_sep_keywordlist,temp_sep_titlekey,temp_sep_avgTone,
                                   temp_sep_goldsteinscale,temp_sep_nummentions,temp_sep_numarticles,temp_sep_numsources,temp_date])
            #str_corpus = "|".join([str(temp_id),temp_segtitle,temp_keywords,temp_DF,temp_lda,time_stamp,temp_original])
            str_corpus=str_corpus+"\n"
            f.write(str_corpus)
        f.close()
    print("output done")
    return temp_count

if __name__=="__main__":
    # mSrc_list = '["www.msn.com", "www.dw.com", "tass.com", "menafn.com"]'
    # mSrc_list = '["dailytimes.com.pk"]'
    # mSrc_list = '["russiaherald.com","business-standard.com","omaha.com","indiatimes.com"]'
    # mSrc_list = '["russiaherald.com","business-standard.com","omaha.com","indiatimes.com"]'
    mSrc_list = '["irishexaminer.com", "sputniknews.com", "wandsworthguardian.co.uk", "romseyadvertiser.co.uk"]'

    # time_scope = '["2019-10-01","2020-01-31"]'
    time_scope = '["2021-10-01","2022-06-31"]'
    country_list = '["ALL"]'
    classnum = '["3","4"]'  # ѡ����


    genStoryForestInputMulti(time_scope,mSrc_list,classnum,country_list)

    # mergeTxt()
    # genStoryForestInput(time_scope,mSrc_list,classnum,country_list)

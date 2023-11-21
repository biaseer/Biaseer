from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from gaindata.dataprocess import mediaDataSet, mediaMatrixDataSet, concatMediaDiff
import json
from utils.helper import readJsontoDict
from keywordExtract.test import test
from keywordExtract.storytree import getStoryTreedata
from keywordExtract.treeDiff import gen_diff

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADER'] = 'Content-Type'


@app.route('/media_dataset', methods=['GET'])
@cross_origin()
def getMediaDataSet():
    data = mediaDataSet()
    # print(data)
    # args_dict = request.args
    # args_dict.to_dict()['mediatopData[]']
    return {'data': data}


@app.route('/media_matrix_dataset', methods=['GET'])
@cross_origin()
def getMediaMatrixDataSet():
    data = mediaMatrixDataSet()
    return {'data': data}

@app.route('/media_concat_diff', methods=['GET'])
@cross_origin()
def getMediaConcatDiffDataSet():
    args_dict = request.args
    mSrc_list = args_dict.getlist('mSrc_list[]')
    # print(mSrc_list)
    data = None
    if len(mSrc_list) > 1:
        data = concatMediaDiff(mSrc_list)
    return {'data': data}

@app.route('/media_matrix_stroytree', methods=['GET'])
@cross_origin()
def getMediaMatrixStoryTreeDataSet():
    args_dict = request.args
    topics = args_dict.getlist('topics[]')
    date_index = args_dict.getlist('date_index[]')
    date = args_dict.getlist('date[]')
    mSrc_list = args_dict.getlist('mSrc_list[]')
    
    print(topics)
    print(date_index)
    print(date)
    print(mSrc_list)

    date_index.sort()

    binDict = readJsontoDict("binDict.json")
    time_scope = [binDict[str(date_index[0])][0], binDict[str(date_index[-1])][-1]]

    # mSrc_list = ["msn.com", "bbc.com"]
    # time_scope = ["2022-02-01","2022-02-21"]
    country_list = ["ALL"]
    # classnum = '["3","4"]'
    classnum = topics
    time_scope = [binDict[str(date_index[0])][0], binDict[str(date_index[-1])][-1]]

    testdata = getStoryTreedata(time_scope,mSrc_list,classnum,country_list)
    # testdata = readJsontoDict("./tree_pro.json")
    return {'data': testdata}

@app.route('/tree_diff', methods=['GET'])
@cross_origin()
def getTreeDiff():
    args_dict = request.args.to_dict()
    print(args_dict)
    value_list=list(args_dict.values())
    tree_name=value_list.pop(-1)
    mSrc_list = value_list
    
    print("in main.py treediff")
    print(mSrc_list)
    data = None
    if len(mSrc_list) > 1:
        data = gen_diff(mSrc_list,tree_name)
    return {'data': data}
if __name__ == "__main__":
    print('run 0.0.0.0:14449')
    app.run(host='0.0.0.0', port=14449)


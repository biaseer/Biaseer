
import axios from 'axios'
let server_address = 'http://localhost:14449'

export function getMediaData(callback) {
    // let formData = {"mediaDataSet": params1}
    axios({
        methods: 'get',
        url: server_address + '/media_dataset',
        // params: formData,
        timeout: 1000000
    })
    .then((res) => {
        let mediaDataSet = res["data"]["data"];
        console.log('mediaDataSet:', mediaDataSet);
        callback(mediaDataSet);
    })
}

export function getMediaMatrixData(callback) {
    axios({
        methods: 'get',
        url: server_address + '/media_matrix_dataset',
        // params: formData,
        timeout: 1000000
    })
    .then((res) => {
        let mediaMatrixData = res["data"]["data"];
        console.log('mediaMatrixData:', mediaMatrixData);
        callback(mediaMatrixData);
    })
}


export function getMediaStoryTreeData(tree_param, meidaList, callback) {
    console.log("tree_param: ", tree_param);
    let topics = Array.from(tree_param['topics']);
    let date_index = Array.from(tree_param['date_index']);
    let date = Array.from(tree_param['date']);
    // console.log(topics);
    // console.log(date_index);
    // console.log(date);
    let formData = {
        "topics": topics,
        "date_index": date_index,
        "date": date,
        "mSrc_list": meidaList
    }
    axios({
        methods: 'get',
        url: server_address + '/media_matrix_stroytree',
        params: formData,
        timeout: 1000000,
    })
    .then((res) => {
        let mediaMatrixStoryTreeData = res["data"]["data"];
        console.log('mediaMatrixStoryTreeData:', mediaMatrixStoryTreeData);
        callback(mediaMatrixStoryTreeData);
    })
}



export function getMediaDiffConcatData(meidaList, callback) {
    let formData = {
        "mSrc_list": meidaList
    }
    axios({
        methods: 'get',
        url: server_address + '/media_concat_diff',
        params: formData,
        timeout: 1000000,
    })
    .then((res) => {
        let mediaDiffConcatData = res["data"]["data"];
        console.log('mediaDiffConcatData:', mediaDiffConcatData);
        callback(mediaDiffConcatData);
    })
}
export function getTreeDiff(meidaList, tree_name,callback) {
    let formData = {
        "mSrc_list": meidaList,
        "tree_name":tree_name
    }
    axios({
        methods: 'get',
        url: server_address + '/tree_diff',
        params: formData,
        timeout: 1000000,
    })
    .then((res) => {
        let tree_diff_data = res["data"]["data"];
        // console.log('tree_diff_data:', tree_diff_data);
        callback(tree_diff_data);
    })
}
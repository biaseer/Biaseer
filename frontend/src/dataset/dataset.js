export function Dataset () {
    this.buildingDatasetList = [];

    this.mediaDataSet = null;

    this.mediaMatrixDataSet = null;


    this.mediaConcatDiffDataSet = null;

    this.mediaMatrixSelected = null;

    this.storyTreeDataset = null;

    this.SankeyTreePathNode = null;

    this.mediaScatterSelected = ['msn.com', 'menafn.com','yahoo.com', 'interfax.com.ua'];

    this.mediaGraphList = [];

    this.keepMediaQueue = []; // keep or cancel mediuam list
}

Dataset.prototype = {
    init: function() {
    },
    updateBuildingDatasetList: function(data) {
        this.buildingDatasetList = data;
    },

    updateMediaDataSet: function(data) {
        this.mediaDataSet = data;
    },

    updateMediaMatrixDataSet: function(data) {
        this.mediaMatrixDataSet = data;
    },


    updateMediaConcatDiffDataSet: function(data){
        this.mediaConcatDiffDataSet = data;
    },

    updateMediaMatrixSelected: function(data) {
        this.mediaMatrixSelected = data;
    },

    updateStoryTreeDataset: function(data) {
        this.storyTreeDataset = data;
    },

    updateSankeyTreePathNode: function(data) {
        this.SankeyTreePathNode = data;
    },

    updateMediaScatterSelected: function(data) {
        if(this.mediaScatterSelected.indexOf(data)==-1){
            console.log(data + "不存在");
            this.mediaScatterSelected.push(data);
        }
        else{
            console.log(data + "已经存在");
        }
    },

    updateMediaGraphList: function(data) {
        if(this.mediaGraphList.indexOf(data)==-1){
            console.log(data + "不存在");
            this.mediaGraphList.push(data);
        }
        else{
            console.log(data + "已经存在");
        }
    }
}
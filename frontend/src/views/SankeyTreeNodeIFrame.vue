<template>
    <div class="sankeytree-node-iframe" ref="iframediv">

        <div class="mytip" v-for="(item,index) in node_details2" :id="item.media_source_index" :style="piecolorScale_1(item.media_source_index)">
            <el-collapse>
                <el-collapse-item >
                    <template #title>
                        <h3 class="el-collapse-item-title" :style="piecolorScale_2(item.media_source_index)"> {{ item.title.split("+")[0]+"."  }}</h3>
                    </template>
                    <p :style="piecolorScale_2(item.media_source_index)"> {{ item.lines }}</p>
                </el-collapse-item>
            </el-collapse>
        </div>

        <!-- <div class="wordcloud">
            <div ref='wordCloudBox'></div>
        </div> -->

    </div>
</template>
<script>
// Structors
import { mapState, mapMutations } from 'vuex';
import myCloud from '@/assets/js/myCloud.js';

export default {
    name: 'SankeyTreeNodeIFrame',
    props: {
        domain: String,
        storytree__loading: Boolean,
    },
    data() {
        return {
            node_details: [],
            node_details2: [],
            width: 400,
        }
    },
    components: {
    },
    beforeMount: function () {
    },
    mounted: function () {
        this.width = this.$refs.iframediv.clientWidth;

    },
    methods: {
        ...mapMutations([
            // 'UPDATE_STORYTREE_FINISH',
        ]),
        piecolorScale_1(i){
            // let colorArray=['#1d6d99','#e56b10','#a6761d','#c6c361']
            let colorArray=['#053061','#e56b10','#a6761d','#c6c361']
            return 'border-left: 5px solid ' + colorArray[i%4];
        },
        piecolorScale_2(i){
            let colorArray=['#000000','#000000','#000000','#000000']
            return 'color: ' + colorArray[i%4];
        },
        getWordCloud(wordList){
            let wordOption = {  
                wordList, 
                size:[this.width,257],  // 盒子的宽高
                svgElement: this.$refs.wordCloudBox  //使用ref选择节点
            }
            myCloud(wordOption,this.callBackFunc())
        },
        callBackFunc(){
            console.log("...")
        },
        drawWordCloud(){
            let root = d3.hierarchy(sysDatasetObj.storyTreeDataset);
            let wordList = [];
            root.each(d=>{
                if(d.data.name == 'ROOT' || d.data.time_e == 'time'){return}
                wordList.push(...d.data.tree_topickey)
                wordList.push(...d.data.tree_keyword.flat())
                wordList.push(...d.data.tree_titlekeyword.flat())
            })
            // console.log(wordList);
            const wordListCountDict = wordList.reduce((obj,key)=>{
                if (key in obj){
                    obj[key]++
                }else{
                    obj[key]=1
                }
                return obj
            },{})
            wordList = []
            for (const [key, value] of Object.entries(wordListCountDict)) {
                wordList.push({text: key, size: value * 10})
            }
            this.getWordCloud(wordList);
        }
    },
    computed: {
        ...mapState([
            'storytree_finish',
            'clickSankeyTreeNode'
        ])
    },
    watch: {
        clickSankeyTreeNode: function(){
            let self = this;
            let data = sysDatasetObj.SankeyTreePathNode;
            data.reverse();
            // console.log('data', data);
            self.node_details2 = []
            data.forEach(d=>{
                console.log(d);
                if(d.name == 'ROOT' || d.time_e == 'time'){return}
                // 提取出可能的媒体源
                let temp_mSrc_list = d.mSrc_list;
                d.node_detail_info.forEach(ele=>{
                    // 检测媒体源，加入媒体ele中
                    temp_mSrc_list.forEach((mele,imele)=>{
                        if(ele.url.split("/")[2].includes(mele)){
                            ele.media_source = mele;
                            ele.media_source_index = imele;
                        }
                    })
                    self.node_details2.push(ele)
                    if(ele.related_infos.length > 0){
                        ele.related_infos.forEach(e=>{
                            // 检测媒体源，加入媒体e中
                            temp_mSrc_list.forEach((mele,imele)=>{
                                if(e.url.split("/")[2].includes(mele)){
                                    e.media_source = mele;
                                    e.media_source_index = imele;
                                }
                            })
                            self.node_details2.push(e)
                        })
                    }
                })
            })
            console.log('node_details2', self.node_details2);
        },
        storytree_finish: function(){
            let self = this;
            let data = sysDatasetObj.storyTreeDataset;
            let root = d3.hierarchy(data);
            self.node_details = [];
            self.node_details2 = [];
            root.each(d=>{
                if(d.data.name == 'ROOT' || d.data.time_e == 'time'){return}
                // 提取出可能的媒体源
                let temp_mSrc_list = d.data.mSrc_list;
                d.data.node_detail_info.forEach(ele=>{
                    // 检测媒体源，加入媒体ele中
                    temp_mSrc_list.forEach((mele,imele)=>{
                        if(ele.url.split("/")[2].includes(mele)){
                            ele.media_source = mele;
                            ele.media_source_index = imele;
                        }
                    })
                    self.node_details2.push(ele)
                    if(ele.related_infos.length > 0){
                        ele.related_infos.forEach(e=>{
                            // 检测媒体源，加入媒体e中
                            temp_mSrc_list.forEach((mele,imele)=>{
                                if(e.url.split("/")[2].includes(mele)){
                                    e.media_source = mele;
                                    e.media_source_index = imele;
                                }
                            })
                            self.node_details2.push(e)
                        })
                    }
                })
            })            
        }
    }
}
</script>
  
<style lang="less" scoped>
.sankeytree-node-iframe{
    width: 100%;
    height: 100%;
    overflow-y: scroll;
    .el-collapse-item-title{
        width: 90%;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        text-align: left;
    }
}
</style>

<style>
.el-carousel__item h3 {
  color: #475669;
  font-size: 14px;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
}
 
.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}
 
.el-carousel__item:nth-child(2n+1) {
  background-color: #d3dce6;
}


.el-carousel__item--card{
  /* display: flex;
  align-items: center;
  justify-items: center; */
  overflow-y: auto;
  /* overflow-x: auto; */
}

.mytip {
    padding: 8px 16px;
    background-color: rgb(244 244 244);
    margin-bottom: 5px;
}
.el-collapse{
    background-color: rgb(244 244 244) !important;
}

.el-collapse-item__header,.el-collapse-item__wrap {
    background-color: transparent !important;
    border-bottom: 0 !important;
}

.el-collapse-item__header{
    height: 24px !important;
}
.el-collapse-item__content {
    padding-bottom: 0px !important;
}
</style>
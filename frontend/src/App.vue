<template>
  <div id="app" v-if="!loadingData">
    <el-menu
      class="el-menu-demo"
      mode="horizontal"
      background-color="#676767"
      text-color="#fff"
      :default-active="activeIndex"
      active-text-color="#ffd04b">
      <el-menu-item class='labelIcon' id="title">
        {{appName}}
      </el-menu-item>
      <!-- <el-tooltip class='labelIcon' v-for="operation in operationArray" :key="operation" :content="operation" effect="light">
        <el-menu-item :index="operation">
          <div type="text" v-if="operation==='submit selection'" @click="submitSelect" :loading="loadingSelect">
            {{loadingSelectInfo}}<i class="el-icon-upload el-icon--right"></i>
          </div>
          <div type="text" v-if="operation==='counter'">
            {{counter}}/100
          </div>
        </el-menu-item>
      </el-tooltip> -->
    </el-menu>


    <div class="media-topic">
      <div class="media-topic-vector-reduction-view">
        <MediaScatter></MediaScatter>
      </div>
      <div class="search-input">
          <el-select
            v-model="select_domain"
            filterable
            remote
            clearable
            placeholder="Searching domain"
            :remote-method="remoteMethod"
            :loading="option_loading">
            <el-option
              v-for="item in option_domains"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </div>
      <div class="media-topic-difference-concat-view">
        <div class="media-concat-list">
          <MediaTags></MediaTags>
        </div>
        <div class="media-concat-diffarea">
          <MediaMatrixTrend></MediaMatrixTrend>
        </div>
        
      </div>
    </div>
    <div class="event-evolution">
      <div class="union-event-evolution">
        <div class="event-evolution-storytree" id="story_tree_div">
          <MediaStoryTree :storytree__loading="storytree__loading"></MediaStoryTree>
          <!-- <MediaSankeyTree :storytree__loading="storytree__loading"></MediaSankeyTree> -->
        </div>
        <div class="event-iframeview">
          <SankeyTreeNodeIFrameVue></SankeyTreeNodeIFrameVue>
          <!-- <iframe :src="iframeSrc" class="iframe-class"></iframe> -->
        </div>
        
      </div>
      <div class="single-event-evolution">
        <el-card v-for="(item, index) in currentRankMedia"
        :key="index"
        :id="item.domain.replaceAll('.','_')"
        shadow="hover"
        @click.native="getTreeDiffData(item.domain)"
        style="margin-right:10px; width:25%">

          <div class="single-domain-tree" ref="singleTree" slot="header" >
            <span class="mSrcSpan" id="mSrcSpanId">{{item.domain}}</span>
            <!-- <svg class="mSrcSvg" width="20" height="15">
              <circle r="5" cx="8" cy="5" :fill=genMsrcColor(item.domain)></circle>
            </svg> -->
            <div class="mSrcSvg" :id="'mSrcSvg-'+item.domain.replaceAll('.','_')"></div>
            <!-- <el-button style="float: right; padding: 3px 0" type="text" @click="getTreeDiffData(item.domain)">Choose</el-button> -->
          </div>
          <SingleTree :storytree__loading="storytree__loading" :domain="item.domain"></SingleTree>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
// Structors
import { mapState, mapMutations } from 'vuex';
import { getMediaData, getMediaMatrixData, getTreeDiff} from '@/communication/communicator.js'
import { getMediaStoryTreeData, getMediaDiffConcatData } from '@/communication/communicator.js'
import { Dataset } from '@/dataset/dataset.js'
import { getDomains } from './assets/js/country_code'

// Components
import MediaScatter from './components/MediaScatter.vue';
import MediaTrend from './components/MediaTrend.vue';
import MediaHorizonChart from './components/MediaHorizonChart.vue';
import MediaMatrixTrend from './components/MediaMatrixTrend.vue';
import MediaStoryTree from './components/MediaStoryTree.vue';
import MediaSankeyTree from './components/MediaSankeyTree.vue';
import MediaTags from './views/MediaTags.vue';
import SingleTree from './views/SingleTree.vue';
import SankeyTreeNodeIFrameVue from './views/SankeyTreeNodeIFrame.vue';
import d3 from './assets/js/horizon';

export default {
  name: 'App',
  data() {
    return {
      appName: "BiaSeer",
      loadingData: true,
      topicCodeList: null,
      storytree__loading: false,
      drawer: true,
      currentSelectedMedia: null,
      currentRankMedia: null,
      activeIndex: 1,
      option_domains: [],
      select_domain: "",
      domain_list: [],
      option_loading: false,
      states: [],
      clicked_medium: "",
      system_topic_event: "RUS_UKR"

    }
  },
  components: {
    MediaScatter,
    MediaTrend,
    MediaHorizonChart,
    MediaMatrixTrend,
    MediaStoryTree,
    MediaSankeyTree,
    MediaTags,
    SingleTree,
    SankeyTreeNodeIFrameVue
  },
  beforeMount: function () {
    let self = this;
    window.sysDatasetObj = new Dataset();
    // lodaing data, during beforemount 
    let mediaDataDeferObj = $.Deferred();
    let mediaMatrixDataDeferObj = $.Deferred();

    $.when(mediaDataDeferObj, mediaMatrixDataDeferObj).then(async () => {
      self.loadingData = false;
    })
    getMediaData(function (data) {
      self.topicCodeList = data['topicCodeList'];
      sysDatasetObj.updateMediaDataSet(data);
      mediaDataDeferObj.resolve();
    });
    getMediaMatrixData(function (data) {
      sysDatasetObj.updateMediaMatrixDataSet(data);
      mediaMatrixDataDeferObj.resolve();
    });
  },
  mounted() {
    let self = this
    this.currentSelectedMedia = this.gainCurrentSelectedMedia();
    var rank_list=Array()
    var temp_value=1;
    for(var i=0;i<this.currentSelectedMedia.length;i++){
      var new_dict={}
      new_dict["domain"]=this.currentSelectedMedia[i].domain;
      new_dict["value"]=temp_value;
      temp_value=temp_value+10
      rank_list.push(new_dict);
    }
    this.currentRankMedia=rank_list;
    this.states = getDomains(self.system_topic_event)
    this.domain_list = this.states.map(item => {
      return { value: `${item}`, label: `${item}` };
    });
    self.drawMediaSpan()
  },
  methods: {
    drawMediaSpan(){
      let self=this
      console.log("span1,",d3.select("body").select(".event-evolution").selectAll(".single-event-evolution").selectAll("span").selectAll(".mSrcSpan"))
      console.log("span2,",d3.select("body").select(".event-evolution").selectAll(".single-event-evolution").selectAll("span"))
      console.log("span3,",d3.select("body").select(".event-evolution").selectAll(".single-event-evolution").selectAll(".mSrcSpan"))
      var span_list=d3.select("body").select(".event-evolution").selectAll(".single-event-evolution").selectAll(".mSrcSpan")
      // span_list.selectAll("svg").remove()
      // span_list.append("svg")
      //     .attr("class","mSrcCircle")
      //     .attr("height",12)
      //     .attr("width",20)
      //     .append("circle").attr("r",5)
      //     .attr("cx",9)
      //     .attr("cy",6)
      //     .attr("fill",piecolorScale_1())
      span_list=span_list._groups[0]
      console.log("in spanlist ",span_list[0])
      let piecolorScale_1 = (i)=>{
        let colorArray=['#053061','#e56b10','#a6761d','#c6c361']
        return colorArray[i%4];
      }
      var select_list=self.currentSelectedMedia
      console.log("select_list",select_list)
      for(var i=0; i < span_list.length; i++){
        for(var j=0; j < self.currentSelectedMedia.length; j++){
          if(d3.select(span_list[i]).text()==select_list[j].domain){
            console.log("domian and name",d3.select(span_list[i]).text(), j)
            
            if(d3.select(span_list[i]).text() == self.clicked_medium){
              d3.select("#mSrcSvg-" + self.clicked_medium.replaceAll('.','_')).style('background', piecolorScale_1(j))
            }

            d3.select(span_list[i]).style('color', piecolorScale_1(j))
            d3.select(span_list[i]).selectAll("svg").remove()
            // d3.select(span_list[i]).append("svg")
            //   .attr("class","mSrcCircle")
            //   .attr("height",12)
            //   .attr("width",20)
            //   .append("circle").attr("r",5)
            //   .attr("cx",9)
            //   .attr("cy",6)
            //   .attr("fill",piecolorScale_1(j))
            break
          }
        }
      }
    },
    genMsrcColor1(mSrc_name){
      console.log("in genMsrcColor!!!")
      var mSrc_list=this.currentSelectedMedia
      let piecolorScale_1=(i)=>{
          let colorArray=['#053061','#e56b10','#a6761d','#c6c361']
          return colorArray[i%4];
      }
      for(var i=0;i<mSrc_list.length;i++){
        if(mSrc_list[i].domian==mSrc_name)
          return "color:"+piecolorScale_1(i)
      }
      
    },
    ...mapMutations([
      'UPDATE_STORYTREE_FINISH',
      'UPDATE_CONCATDIFF_FINISH',
      'UPDATE_CONTOUR_SEARCH_DOMAIN',
    ]),
    remoteMethod(query) {
      if (query !== '') {
        this.option_loading = true;
        setTimeout(() => {
          this.option_loading = false;
          this.option_domains = this.domain_list.filter(item => {
            return item.label.toLowerCase().indexOf(query.toLowerCase()) > -1;
          });
        }, 200);
      } else {
        this.option_domains = [];
      }
    },
    gainCurrentSelectedMedia(){
      let result = []
      sysDatasetObj.mediaScatterSelected.forEach(element => {
        result.push({domain: element})
      });
      console.log(result);
      return result;
    },
    isToGetStroytree() {
      let data = sysDatasetObj.mediaMatrixSelected;
      console.log(data);
      console.log(data['date'].size);
      if (data['date'].size > 0) {
        return true;
      }
      return false;
    },
    getStroyTree() {
      let self = this;
      self.storytree__loading = true;
      let mediaMatrixSelectedDataDeferObj = $.Deferred();
      $.when(mediaMatrixSelectedDataDeferObj).then(async () => {
        self.storytree__loading = false;
        self.drawMediaSpan()
      })
      getMediaStoryTreeData(sysDatasetObj.mediaMatrixSelected,sysDatasetObj.mediaScatterSelected, function (data) {
        sysDatasetObj.updateStoryTreeDataset(data);
        self.UPDATE_STORYTREE_FINISH();
        mediaMatrixSelectedDataDeferObj.resolve();
      });
     

    },
    getTreeDiffData(tree_name){
      let self=this;
      self.clicked_medium = tree_name;
      let treeDifDeferObj=$.Deferred();
      $.when(treeDifDeferObj).then(async () => {
        
        self.drawMediaSpan()
      })
      getTreeDiff(self.currentSelectedMedia,tree_name,function(data){
        console.log("tree_diff_data",data)
        self.currentRankMedia=data;
        self.UPDATE_STORYTREE_FINISH();
        console.log("currentrank ",self.currentRankMedia)
        treeDifDeferObj.resolve();
      });
      
    },
    genMsrcColor(mSrc_name){
      console.log("in genMsrcColor!!!")
      var mSrc_list=this.currentSelectedMedia
      let piecolorScale_1=(i)=>{
          let colorArray=['#053061','#e56b10','#a6761d','#c6c361']
          return colorArray[i%4];
      }
      for(var i=0;i<mSrc_list.length;i++){
        if(mSrc_list[i].domian==mSrc_name)
          return piecolorScale_1(i)
      }
      
    },
    // drawMediaSpan(){
    //         let self=this
    //         let span1=d3.select("body").selectAll(".single-domain-tree").selectAll("span")
    //         // console.log("span,",d3.select("body"))
    //         // console.log("span,",d3.select("body").select(this.$refs.singleTree))
    //         // console.log("span,",d3.select("body").select(".event-evolution").selectAll(".single-domain-tree"))
    //         // console.log("span,",d3.select("body").select(".event-evolution").selectAll(".single-event-evolution"))
    //         // console.log("span,",d3.select("body").select(".event-evolution").selectAll(".single-event-evolution").selectAll(".el-card__body"))
    //         console.log("span1,",d3.select("body").select(".event-evolution").selectAll(".single-event-evolution").selectAll("span").selectAll(".mSrcSpan"))
    //         console.log("span2,",d3.select("body").select(".event-evolution").selectAll(".single-event-evolution").selectAll("span"))
    //         console.log("span3,",d3.select("body").select(".event-evolution").selectAll(".single-event-evolution").selectAll(".mSrcSpan"))
    //     },
    
  },
  computed: {
    ...mapState([
      'currMedium',
      'mediaMatrixSelectedSignal',
      'mediaDiffConcatSignal',
      'mediaScatterClick'
    ]),
    
    
    
  },
  watch: {
    select_domain: function(){
      this.UPDATE_CONTOUR_SEARCH_DOMAIN(this.select_domain);
    },
    mediaMatrixSelectedSignal: function () {
      let self = this;
      console.log(self.mediaMatrixSelectedSignal);
      if (self.isToGetStroytree()) {
        self.getStroyTree();
      }
    },
    mediaDiffConcatSignal: function(){
      let self = this;
      console.log("listening mediaDiffConcatSignal");
      let mediaDiffConcatDataDeferObj = $.Deferred();
      $.when(mediaDiffConcatDataDeferObj).then(async () => {
        self.UPDATE_CONCATDIFF_FINISH();
      })
      getMediaDiffConcatData(sysDatasetObj.mediaScatterSelected, function (data) {
        sysDatasetObj.updateMediaConcatDiffDataSet(data);
        mediaDiffConcatDataDeferObj.resolve();
      });
    },
    mediaScatterClick: function(){
      this.currentSelectedMedia = this.gainCurrentSelectedMedia();
      var rank_list=Array()
      var temp_value=1;
      for(var i=0;i<this.currentSelectedMedia.length;i++){
      var new_dict={}
      new_dict["domain"]=this.currentSelectedMedia[i].domain;
      new_dict["value"]=temp_value;
      temp_value+=10;
      rank_list.push(new_dict);
      }
      this.currentRankMedia=rank_list;
      
    }
  }
}
</script>

<style lang="less">
// div{
//   border-radius: 5px;
//   margin: .5px;
// }

@menu-height: 2.5rem;
@title-container-height: 160px;
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  position: absolute;
  top: 0%;
  bottom: 0%;
  left: 0%;
  right: 0%;
  overflow-x: hidden;
  overflow-y: hidden;

  .el-menu.el-menu--horizontal {
    .el-menu-item {
      height: @menu-height;
      line-height: @menu-height;
    }
    .el-menu-item {
      border-bottom-color: rgb(84, 92, 100) !important;
      font-weight: bolder;
      font-size: 1rem;
      color: #dadada !important;
      padding: 0 10px;
      .icon {
        color: #dadada !important;
      }
    }
  }
  .labelIcon {
    font-size: 1rem;
  }

  .media-topic {
    position: absolute;
    // top: 0%;
    top: @menu-height;
    bottom: 65%;
    left: 0%;
    right: 0%;
    .media-topic-vector-reduction-view {
      position: absolute;
      top: 0%;
      bottom: 0%;
      left: 0%;
      right: 50%;
      border-left: 1px solid gray;
      border-top: 1px solid gray;
    }

    .media-topic-difference-concat-view {
      position: absolute;
      top: 0%;     
      bottom: 0%;
      left: 50%;
      right: 0%;
      // border: 1px solid gray;
      .media-concat-list{
        position: absolute;
        top: 0%;
        bottom: 90%;
        left: 0%;
        right: 0%;
        border: 1px solid gray;
        display: flex;
        align-items: center;
      }
      .media-concat-diffarea{
        position: absolute;
        top: 10%;
        bottom: 0%;
        left: 0%;
        right: 0%;
        border-left: 1px solid gray;
      }
    }
  }

  .event-evolution {
    position: absolute;
    top: 35%;
    bottom: 0%;
    left: 0%;
    right: 0%;
    margin: 0px !important;

    .union-event-evolution {
      position: absolute;
      top: 0%;
      bottom: 30%;
      left: 0%;
      right: 0%;
      // border: 1px solid gray;
      .event-evolution-storytree{
        position: absolute;
        top: 0%;
        bottom: 0%;
        left: 0%;
        right: 30%;
        border: 1px solid gray;
      }
      .event-iframeview{
        position: absolute;
        top: 0%;
        bottom: 0%;
        left: 70%;
        right: 0%;
        border-top: 1px solid gray;
        border-bottom: 1px solid gray;
        border-right: 1px solid gray;
        .iframe-class{
          width: 100%;
          height: 100%;
        }
      }
    }

    .single-event-evolution {
      position: absolute;
      top: 70%;
      bottom: 0%;
      left: 0%;
      right: 0%;
      overflow-x: scroll;
      display: flex;
      .single-domain-tree{
        display: flex;
        align-items: center;
        .mSrcSvg {
          background: rgb(229, 228, 228);
          border-radius: 50%;
          width: 20px;
          height: 20px;
        }
        #mSrcSpanId{
          flex: 1
        }
      }
    }
  }
}

.search-input {
  width: 230px;
  margin-left: 37.5%;
  margin-top: 0.1%;
  .el-input__inner{
    height: 23px;
    font-size: 1em;
    font-weight: bolder;
    color: steelblue;
  }
  .el-input__suffix {
    width: 200px;
    top: 7px;
  }
  .el-input__icon {
    line-height: inherit;
  }
  .el-input__suffix-inner {
    display: inline-block;
  }
}
</style>

<template>
    <div class="single_tree"
    :class="domain"
    v-loading="storytree__loading"
    ref="singlestorytree"
    element-loading-text="Waiting Loading Story Tree">
    
    <svg id="single_storytree__svg"></svg>
    </div>
</template>
  
<script>
// Structors
import d3 from '@/assets/js/horizon';
import { mapState, mapMutations } from 'vuex';

export default {
    name: 'SingleTree',
    props: {
        domain: String,
        storytree__loading: Boolean,
    },
    data() {
        return {
            // dynamicTags:['msn.com'],
            width: 0,
            height: 0,
        }
    },
    components: {
    },
    beforeMount: function () {
        
    },
    mounted: function () {
        let self = this;
        self.width = self.$refs.singlestorytree.clientWidth;
        self.height = self.$refs.singlestorytree.clientHeight;
        // self.drawStoryTree(self.width, self.height);
        // self.drawMediaSpan()
        
        
    },
    methods: {
        ...mapMutations([
            // 'UPDATE_STORYTREE_FINISH',
        ]),
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
                    let colorArray=['#1d6d99','#e56b10','#a6761d','#c6c361']
                    return colorArray[i%4];
                }
            for(var i=0;i<span_list.length;i++){
                d3.select(span_list[i]).style('color',piecolorScale_1(i))
                d3.select(span_list[i]).selectAll("svg").remove()
                d3.select(span_list[i]).append("svg")
                .attr("class","mSrcCircle")
                .attr("height",12)
                .attr("width",20)
                .append("circle").attr("r",5)
                .attr("cx",9)
                .attr("cy",6)
                .attr("fill",piecolorScale_1(i))

                console.log('span i ', span_list[i])
            }
            
        },
        drawStoryTree(width, height) {
            let self = this;
            let margin = { top: 15, bottom: 15, left: 15, right: 15 };
            let innerWidth = width - margin.left - margin.right;
            let innerHeight = height - margin.top - margin.bottom;
            

            let renderStoryTree = (root, reScale, reScaleCircleRadia, delta_timeScale, attrsMaxMin, dx, dy, timescope) => {
                let x0 = 10;
                let x1 = -x0;
                root.each(d => {
                    if (d.x > x1) x1 = d.x;
                    if (d.x < x0) x0 = d.x;
                });//find max and min
                d3.select(self.$el).select("#single_storytree__svg").selectAll('g').remove();
                
                const svg = d3.select(self.$el).select("#single_storytree__svg")
                    .attr("width", width)
                    .attr("height", height);

                const g = svg
                    .append("g")
                    .attr("font-family", "sans-serif")
                    .attr("font-size", 10)
                    .attr("width", innerWidth)
                    .attr("height", innerHeight)
                    .attr("transform", `translate(${margin.left},${-dx / 2.5 + margin.top})`);

                const link = g
                    .append("g")
                    // .attr('transform', `translate(${reScale.bandwidth()/2},${-5})`)
                    .attr("fill", "none")
                    .attr("stroke", "grey")
                    .selectAll("path")
                    .data(root.links())
                    .join("path")
                    .attr("d", d=>{
                        if(d.source.data.time_e == d.target.data.time_e){
                            // alert("duplicate time [parent, child]")
                            let PosData = []
                            PosData.push([reScale(d.source.data.time_e), d.source.x])
                            PosData.push([reScale(d.target.data.time_e) + reScale.bandwidth()/2, d.target.x])
                            let lineGenerator = d3.line().curve(d3.curveStepBefore)
                            let lineData = lineGenerator(PosData)
                            return lineData;
                        }
                        else{
                            let PosData = []
                            PosData.push([reScale(d.source.data.time_e), d.source.x])
                            PosData.push([reScale(d.target.data.time_e), d.target.x])
                            let lineGenerator = d3.line().curve(d3.curveStepBefore)
                            let lineData = lineGenerator(PosData)
                            return lineData;
                            // return d3.linkHorizontal()
                            //     .x(d => reScale(d.data.time_e))
                            //     .y(d => d.x)(d)
                        }
                    })
                    .attr("stroke-opacity", d=>{
                        if(d.target.data.tree_mSrcName.indexOf(self.domain) < 0){
                            return 0.2;
                        }
                        return 1.0;
                    })
                    .on("mouseover", function(d) {
                        d3.select(this).classed("line-hover", true);
                    })
                    .on("mouseout", function(d) {
                        d3.select(this)
                            .classed("line-hover", false);
                    });

                let node = g
                    .append("g")
                    .attr("class", "storytree__node")
                    // .attr('transform', `translate(${reScale.bandwidth()/2},${-5})`)
                    .attr("stroke-linejoin", "round")
                    .attr("stroke-width", 3)
                    .selectAll(".story_tree_node")
                    .data(root.descendants())
                    .join("g")
                    .attr("class", "story_tree_node")
                    .attr("id",d=>{
                        return "story_tree_node_" + d.index;
                    })
                    .attr("transform", d => {
                        if(d.depth > 1 && d.parent.data.time_e == d.data.time_e){
                            d.y = reScale(d.data.time_e) + reScale.bandwidth() / 2;
                            return `translate(${reScale(d.data.time_e) + reScale.bandwidth() / 2},${d.x})`;
                        }
                        return `translate(${reScale(d.data.time_e)},${d.x})`;                        
                    });
                
                // ===================circle=================//
                let computeColorNeg = d3.interpolate('red', 'white');
                let linearVDataNeg = d3.scaleLinear()  
                    .domain([0.3, 0.5])
                    .range([0, 1]);
                
                let computeColorPos = d3.interpolate('white', 'green');
                let linearVDataPos = d3.scaleLinear()  
                    .domain([0.5, 0.8])
                    .range([0, 1]);
                
                node.each(ele=>{
                    // root node
                    if(ele.data.name == "ROOT"){
                        let ele_g = d3.select(this.$el).select("#story_tree_node_" + ele.index).append("g")
                            .attr("class", "ele-g");
                        ele_g.append('path')
                            .attr('d',d3.symbol().type(d3.symbolCircle).size(70))
                            .attr('fill','white')
                            .attr('stroke', 'gray')
                            .attr('stroke-width', '1px');
                    }
                })

                var rect=node
                    .append("rect");
                    rect.attr("fill", d=> {
                        if(d.data.tree_mSrcName.indexOf(self.domain) < 0){
                            return "white";
                        }else{
                            let index = d.data.mSrc_list.indexOf(self.domain)
                            let tone = +d.data.avg_avgTone[index]
                            if( tone < 0.5){
                                return computeColorNeg(linearVDataNeg(tone))
                            }else if( tone > 0.5){
                                return computeColorPos(linearVDataPos(tone))
                            }else{
                                return '#f9f9f9';
                            }                            
                        }
                    })
                    .attr("stroke", "grey")
                    .attr("stroke-dasharray", d=>{
                        if(d.data.tree_mSrcName.indexOf(self.domain) < 0){
                            return "2"
                        }
                        else{
                            return "0"
                        }
                    })
                    .attr("stroke-width", "1px")
                    .attr("width", d=> {
                        if(d.data.tree_mSrcName.indexOf(self.domain) < 0){
                            return 0;
                        }
                        else{
                            let index = d.data.mSrc_list.indexOf(self.domain)
                            return reScaleCircleRadia(+d.data.tree_nodeSrcN[index])
                        }
                    })
                    .attr("height",d=>{
                        if(d.data.tree_mSrcName.indexOf(self.domain) < 0){
                            return 0;
                        }
                        else{
                            let index = d.data.mSrc_list.indexOf(self.domain)
                            return reScaleCircleRadia(+d.data.tree_nodeSrcN[index])
                        }
                    })
                    var rect_y=rect.attr("y")
                    rect.attr("y",d=>{
                        if(d.data.tree_mSrcName.indexOf(self.domain) < 0){
                            return 0;
                        }
                        else{
                            let index = d.data.mSrc_list.indexOf(self.domain)
                            return -reScaleCircleRadia(+d.data.tree_nodeSrcN[index])/2
                        }
                        
                    })
                    .attr("x",d=>{
                        if(d.data.tree_mSrcName.indexOf(self.domain) < 0){
                            return 0;
                        }
                        else{
                            let index = d.data.mSrc_list.indexOf(self.domain)
                            return -reScaleCircleRadia(+d.data.tree_nodeSrcN[index])/2
                        }
                        
                    })
            }


            let data = sysDatasetObj.storyTreeDataset;
            
            let rootnode = d3.hierarchy(data);
            let dx = innerHeight / (rootnode.children.length + 3);
            let dy = innerWidth / (rootnode.height + 3);
            let nodes = rootnode.descendants().filter(ele => ele.data.time_e);
            let timescope = nodes.map(ele => ele.data.time_e.replaceAll("-", "")).sort((a, b) => a - b)
                .map(ele=>ele=="time" ? "time" : ele.slice(0,4)+"-"+ele.slice(4,6)+"-"+ele.slice(6,8));
            self.tree_timescope = timescope;
            let delta_timescope = timescope.filter(ele=>ele != "time");
            let uni_delta_timescope = [...new Set(delta_timescope)];
            let delta_time = [];
            for(let i = 0; i < uni_delta_timescope.length - 1; i++){
                delta_time.push(
                    Date.parse(uni_delta_timescope[i + 1]) - Date.parse(uni_delta_timescope[i])
                );
            }
            
            let delta_timeScale = d3.scaleLinear().domain(d3.extent(delta_time)).range([1,4]);

            let reScale = d3.scaleBand().domain(timescope).range([0, innerWidth]);
            let biasMaxMin = nodes.filter(ele=> ele.data.totalbias != "null").map(ele=>+ele.data.totalbias);
            // console.log("biasMaxMin: ", biasMaxMin);

            let attrsMaxMin = []
            let numsMaxMin = []
            let tree_maxCompatibilityMaxMin = []
            nodes.filter(ele=> ele.data.totalbias != "null")
                .map(ele=>{
                    attrsMaxMin.push(+ele.data.tree_vari_avgTone)
                    attrsMaxMin.push(+ele.data.tree_vari_gold)
                    attrsMaxMin.push(+ele.data.tree_vari_nummention)
                    attrsMaxMin.push(+ele.data.tree_vari_numarticle)
                    attrsMaxMin.push(+ele.data.tree_vari_numresouce)
                    attrsMaxMin.push(+ele.data.tree_vari_mSrcN)
                    tree_maxCompatibilityMaxMin.push(+ele.data.tree_maxCompatibility)
                    numsMaxMin.push(...ele.data.tree_nodeSrcN.map(Number))
                })
            
            let lineWidthScale = d3.scaleLinear().domain(d3.extent(tree_maxCompatibilityMaxMin)).range([2, 5]);
            let lineFillScale = d3.scaleLinear().domain(d3.extent(tree_maxCompatibilityMaxMin)).range([0.4, 1]);

            // let reScaleCircleRadia = d3.scaleLinear().domain(d3.extent(biasMaxMin)).range([5,10]);
            let reScaleCircleRadia = d3.scaleLinear().domain(d3.extent(numsMaxMin)).range([5, 10]);
            let tree = data => {
                let i = 0;
                const root = d3.hierarchy(data).eachBefore(d=>{d.index = i++;});
                return d3.cluster().size([innerHeight,innerWidth])(root);
            }
            let root = tree(data);
            renderStoryTree(root, reScale, reScaleCircleRadia, delta_timeScale, attrsMaxMin, dx, dy, timescope);
            
        },
    },
    computed: {
        ...mapState([
            'storytree_finish'
        ])
    },
    watch: {
        storytree_finish:function(){
            let self = this;
            // this.width = this.$refs.singlestorytree.clientWidth;
            // this.height = this.$refs.singlestorytree.clientHeight;
            // console.log("storytree width height",this.width,this.height)
            self.drawStoryTree(self.width, self.height);
        },
    }
}
</script>
  
<style lang="less" scoped>
.single_tree{
    width: 100%;
    height: 100%;  
}
</style>


<style>
.el-card__header {
  padding: 2px 10px !important;
  /* background-color: palegoldenrod; */
  background-color: rgb(229, 228, 228);
  
}
.el-card__body {
  padding: 0px !important;
  /* background-color: powderblue; */
}

</style>
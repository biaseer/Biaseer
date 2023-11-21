<template>
    <div class="media-storytree-container"
    id="div_id_storytree"
    v-loading="storytree__loading"
    element-loading-text="Waiting Loading Story Tree"
    ref="mediastorytree">
        <svg id="storytree__svg"></svg>
    </div>
</template>
  
<script>

import { mapState, mapMutations } from 'vuex';

export default {
    name: 'MediaStoryTree',
    props: {
        msg: String,
        topic_code: String,
        storytree__loading: Boolean,
    },
    data() {
        return {
            width: null,
            height: null,
            domain: 'msn.com',
            pie_r: 1,
            mediasources: null,
            drawer: false,
            gridData: [],
            piecolorScale: null,
            ego_path: null,
            ego_path__node: null,
            tree_node_circle_click_id: null,
            treeNodeDetailTooltipDivHidden: false,
            divPos: {top: 0, left: 0, width: 0, height: 0},
            tree_timescope: null,
        }
    },
    computed: {
        ...mapState([
            'currMedium',
            'storytree_finish',
            'tree_node_click'
        ])
    },
    watch: {
        currMedium: function () {
            let self = this;
        },
        storytree_finish:function(){
            let self = this;
            // console.log("storytree_finish:", this.storytree_finish);
            // console.log("sysDatasetObj.StoryTreeDataset",sysDatasetObj.StoryTreeDataset);
            // this.width = this.$refs.storytree.clientWidth;
            // this.height = this.$refs.storytree.clientHeight;
            self.drawStoryTree(self.width, self.height);
        },
        tree_node_click: function () {
            let self = this;
            let click_node_id = self.tree_node_click.split("+").slice(0,1);
            // console.log("self.tree_node_click", self.tree_node_click);
            // console.log("self.ego_path__node", self.ego_path__node);

            let curr_click_node = self.ego_path__node.filter(ele => ele.index == click_node_id)[0];
            // console.log("curr_click_node", curr_click_node);
            // alert(self.tree_node_click);

            let m_width = 300;
            let m_height = 150;
            let m_margin = { top: 10, right: 5, bottom: 15, left: 25 };
            let m_innerWidth = m_width - m_margin.left - m_margin.right;
            let m_innerHeight = m_height - m_margin.top - m_margin.bottom;

            let div_top = self.divPos.top;
            let div_left = self.divPos.left;
            let div_height = self.divPos.height;
            let div_width = self.divPos.width;

            d3.select("body").select("#div"+curr_click_node.index).remove();

            let detail_div = d3.select("body").append("div")
                .attr("class", "tree_node_detail_tooltip_div")
                .attr("id", "div"+curr_click_node.index)
                .style('position', 'absolute')
                .style('top', d => {
                    // if (div_top + curr_click_node.m1 > div_top + div_height - 2 * m_height) {
                    //     return (div_top + div_height - 2 * m_height) + "px"
                    // }
                    // else {
                    //     return div_top + curr_click_node.m1 + 20 + "px"
                    // }
                    return div_top + curr_click_node.m1 + 20 + "px"
                })
                .style('left', function () {
                    // if (div_left + curr_click_node.m0 > div_left + div_width - 2 * m_width) {
                    //     return (div_left + div_width - 1.5 * m_width) + "px"
                    // }
                    // else {
                    //     return div_left + curr_click_node.m0 + 50 + "px"
                    // }
                    return div_left + curr_click_node.m0 + 50 + "px"
                })
                .style('width', m_width + "px")
                .style('height', m_height + 30 + "px")
                // .style('background-color', "gray")
                // .style("overflow", "auto")
            
            
            detail_div.append("i")
                .attr("class", "el-icon-close close-icon")
                .on("click",function(){
                    d3.select("body").select("#div" + curr_click_node.index).remove();
                })
            let detail_div_link_container = detail_div.append("div")
                .attr("class", "detail_div_link_container");
            
            self.move("div" + curr_click_node.index);
            
            let tree_nodeSrcN = curr_click_node.data.tree_nodeSrcN.map(Number);
            
            let totalresource_n = curr_click_node.data.totalresource_n.map(Number);
            let avg_avgTone = curr_click_node.data.avg_avgTone.map(Number);
            let avg_goldsteinscale = curr_click_node.data.avg_goldsteinscale.map(Number);
            let avg_nummentions = curr_click_node.data.avg_nummentions.map(Number);
            let avg_numarticles = curr_click_node.data.avg_numarticles.map(Number);
            let avg_numresources = curr_click_node.data.avg_numresources.map(Number);

            let tree_nodeSrcN_lable = [];
            tree_nodeSrcN.forEach((ele,ie)=>{
                if(ele > 0){
                    tree_nodeSrcN_lable.push(ie);
                }
            })

            curr_click_node.data.node_detail_info.forEach((ele,ie)=>{
                let index = ie + 1;
                let link_ele = detail_div_link_container.append("div");
                link_ele.append("span")
                    .attr("class", "node_detail_span_1")
                    .append("a")
                    .style("text-decoration", "none")
                    .style("color", self.piecolorScale(tree_nodeSrcN_lable[ie]))
                    .attr("href", ele.url.split(",")[0])
                    .attr("target", "_blank")
                    .html("["+ index + "]" + ele.title+ ". " + ele.time + "." + " {Related: " + (ele.related_infos.length + 1) + "}.");
                
                link_ele.append("div").append("span")
                    .attr("class", "node_detail_span")
                    // .text(ele.lines.split(" ").slice(0,20).join(" ") + "...")
                    .text(ele.lines)
                
                let attrs_values = [
                    avg_avgTone[tree_nodeSrcN_lable[ie]],
                    avg_goldsteinscale[tree_nodeSrcN_lable[ie]],
                    // avg_nummentions[tree_nodeSrcN_lable[ie]],
                    // avg_numarticles[tree_nodeSrcN_lable[ie]],
                    // avg_numresources[tree_nodeSrcN_lable[ie]],
                    // totalresource_n[tree_nodeSrcN_lable[ie]]
                ]

                var table = link_ele.append("div").append("table").attr("id","ver-zebra");

                var thead = table.append("thead")
                    .append("tr");
                thead.selectAll("th")
                    .data(["tone:",attrs_values[0].toFixed(4), "impact:", attrs_values[1].toFixed(4)])
                    .enter()
                    .append("th")
                    .attr("id", d=>"ver-zebra-"+d)
                    .text(function (column) { return column; });
            })

            // let summary_div = detail_div.append("div")
            //     .attr("class", "summary_container")
            //     .style('width', m_width + "px")
            //     .style('height', m_height + "px")
            // summary_div.append("div")
            //     .append("span")
            //     .attr("class", "summary_container_title")
            //     .text("ChatGPT Summarized Result")

            // summary_div.append("div")
            //     .append("span")
            //     .attr("class", "node_detail_span")
            //     .text("Summary....")

            // let nodeSummaryDeferObj = $.Deferred()
            // $.when(nodeSummaryDeferObj).then(async() => {
            // })

            // let tree_filePath_1D = curr_click_node.data.tree_filePath.reduce(function(prev, next) {
            //     return prev.concat(next);
            // });
            // let summary_file_path_list = [];
            // curr_click_node.data.node_detail_info.forEach(ele=>{
            //     tree_filePath_1D.forEach(ele_1d=>{
            //         if(ele_1d.includes(ele.title)){
            //             summary_file_path_list.push(ele_1d);
            //         }
            //     })
            // })

            // getNodeClickSummary(summary_file_path_list.join("+"), function (data) {
            //     // self.UPDATE_TREE_NODE_CLICK_PATH_LIST(data.slice(1,5))
            //     self.UPDATE_TREE_NODE_CLICK_PATH_LIST(self.randomString(6))
            //     console.log("summary: ", data);
            //     sysDatasetObj.updateNodeClickSummary(data)
            //     nodeSummaryDeferObj.resolve()
            // });
        },
    },
    mounted: function () {
        let self = this;
        self.width = self.$refs.mediastorytree.clientWidth;
        self.height = self.$refs.mediastorytree.clientHeight;
        // self.drawStoryTree(self.width, self.height);
    },
    methods: {
        ...mapMutations([
            'UPDATE_TREE_NODE_CIRCLE_CLICK',
            'UPDATE_TREE_NODE_CLICK',
            'UPDATE_TREE_NODE_CLICK_PATH_LIST',
            'UPDATE_CLICK_SANKEY_TREE_NODE_MODE'
        ]),
        initLeftTopPos: function() {
            let odiv=document.getElementById('div_id_storytree');
            this.divPos.left = odiv.getBoundingClientRect().left;
            this.divPos.top = odiv.getBoundingClientRect().top;
            this.divPos.width = odiv.getBoundingClientRect().width;
            this.divPos.height = odiv.getBoundingClientRect().height;
        },
        randomString(e) {
            e = e || 32;
            let t = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678",
                a = t.length,
                n = "";
            for(let i = 0; i < e; i++) n += t.charAt(Math.floor(Math.random() * a));
            return n;
        },
        move(div_id) {
            console.log('div_id', div_id);
            var _move = false;
            div_id = '#'+div_id
            var _x, _y;
            $(div_id).click(function () {
                // alert("click")
            }).mousedown(function (e) {
                _move = true;
                _x = e.pageX - parseInt($(div_id).css("left"));
                _y = e.pageY - parseInt($(div_id).css("top"));
                $(div_id).fadeTo(20, 0.5);
            });
            $(document).mousemove(function (e) {
                if (_move) {
                    var x = e.pageX - _x;
                    var y = e.pageY - _y;
                    $(div_id).css({ top: y, left: x }); 
                }
            }).mouseup(function () {
                _move = false;
                $(div_id).fadeTo("fast", 1);
            });
        },
        drawStoryTree(width, height) {
            let self = this;
            console.log(width, height);
            let margin = { top:15, bottom:55, left:10, right:20 };
            let innerWidth = width - margin.left - margin.right;
            let innerHeight = height - margin.top - margin.bottom;
            

            let renderStoryTree = (root, reScale, reScaleCircleRadia, delta_timeScale, attrsMaxMin, dx, dy, timescope) => {
                let x0 = Infinity;
                let x1 = -x0;
                root.each(d => {
                    if (d.x > x1) x1 = d.x;
                    if (d.x < x0) x0 = d.x;
                });
                d3.select(self.$el).select("#storytree__svg").selectAll('g').remove();
                
                const svg = d3.select(self.$el).select("#storytree__svg")
                    .attr("width", width - 10)
                    .attr("height", height - 10);

                svg.append("defs").html(`
                    <style>
                    .highlight circle { fill:black }
                    .highlight circle { fill:black }
                    .highlight text { fill:black }
                    .leaf circle { fill:black }
                    .leaf circle { fill:black }
                    .leaf text { fill:black }
                    path.highlight { stroke:black }
                    <style>`);

                const g = svg
                    .append("g")
                    .attr("font-family", "sans-serif")
                    .attr("font-size", 10)
                    .attr("transform", `translate(${margin.left},${margin.top})`);
                
                const timeAxis = d3.axisBottom(reScale);
                const xAxisG = g.append('g').call(timeAxis)
                    .attr('transform', `translate(${0},${innerHeight})`);
                xAxisG.selectAll("text")
                    .attr("transform", "translate(-0,0)rotate(-30)")
                    .style("text-anchor", "end")
                    .on("mouseover", function(d) {
                        d3.select(this).classed("line-hover", true);
                    })
                    .on("mouseout", function(d) {
                        d3.select(this)
                            .classed("line-hover", false);
                    });
                xAxisG.selectAll('.domain').remove();

                let delta_time_space = 3
                const delta_time_g = g
                    .append("g")
                    .attr('transform', `translate(${0},${innerHeight})`)
                    .attr("class", "delta_time_g")
                    .selectAll('.delta_time_rect')
                    .data(delta_time)
                    .enter()
                    .append('rect')
                    .attr('class', 'delta_time_rect')
                    .attr('x', (d,i)=>reScale(uni_delta_timescope[i + 1]) - reScale.bandwidth() / 2 + delta_time_space)
                    .attr('y', d => delta_time_space - delta_timeScale(d) / 2)
                    // .attr('rx', d=> delta_timeScale(d) / 2)
                    .attr('width', reScale.bandwidth() - 2 * delta_time_space)
                    .attr('height', d=> delta_timeScale(d))
                    .on("mouseover", function(d) {
                        d3.select(this).classed("line-hover", true);
                    })
                    .on("mouseout", function(d) {
                        d3.select(this)
                            .classed("line-hover", false);
                    });
                    



                const link = g
                    .append("g")
                    .attr('transform', `translate(${reScale.bandwidth()/2},${0})`)
                    .attr("fill", "none")
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
                            // let PosData = []
                            // PosData.push([reScale(d.source.data.time_e), d.source.x])
                            // PosData.push([reScale(d.target.data.time_e), d.target.x])
                            // let lineGenerator = d3.line().curve(d3.curveStepBefore)
                            // let lineData = lineGenerator(PosData)
                            // return lineData;
                            
                            return d3.linkHorizontal()
                                .x(d => reScale(d.data.time_e))
                                .y(d => d.x)(d)
                        }
                    })
                    .attr("stroke", "gray")
                    .attr("stroke-width", d=>{
                        // return lineWidthScale(+d.target.data.tree_maxCompatibility)
                        return 3.5
                    })
                    .attr("stroke-opacity", d=>{
                        // return lineFillScale(+d.target.data.tree_maxCompatibility)
                        return 0.8
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
                    .attr('transform', `translate(${reScale.bandwidth()/2},${0})`)
                    .attr("stroke-linejoin", "round")
                    .attr("stroke-width", 2)
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
                // node
                //     .append("circle")
                //     .attr("fill", "steelblue")
                //     // .attr("r", 8);
                //     .attr("r", d=> d.data.totalbias !="null" ? reScaleCircleRadia(+d.data.totalbias) : 1);
                
                // ===================pie=================//
                let piecolorScale = d3.scaleOrdinal()
                        .domain(d3.range(4))
                        .range(d3.schemeCategory10);
                
                let piecolorScale_1 = (i)=>{
                    // let colorArray=['#1d6d99','#e56b10','#a6761d','#c6c361']
                    // let colorArray=['#8dd3c7','#ffffb3','#bebada','#fb8072']
                    let colorArray=['#053061','#e56b10','#a6761d','#c6c361']
                    return colorArray[i%4];
                }
                
                
                self.piecolorScale = piecolorScale_1;
                
                let pie = d3.pie();

                node.each(ele=>{
                    self.mediasources = ele.data.mSrc_list;
                    // console.log("mediasources", self.mediasources);
                    let ele_g = d3.select(this.$el).select("#story_tree_node_" + ele.index).append("g")
                        .attr("class", "ele-g");
                    
                    // root node
                    if(ele.data.name == "ROOT"){
                        ele_g.append('path')
                            .attr('d',d3.symbol().type(d3.symbolCircle).size(300))
                            .attr('fill','white')
                            .attr('stroke', 'gray')
                            .attr('stroke-width', 2);
                    }
                    
                    let pie_r = ele.data.totalbias !="null" ? reScaleCircleRadia(+ele.data.totalbias) : 1;
                    
                    ele_g.selectAll(".story_tree_node_pie")
                        .data(d=>{
                            let dataset = d.data.tree_nodeSrcN.map(Number);
                            return pie(dataset);
                        })
                        .enter()
                        .append("g")
                        .attr("class", "story_tree_node_pie")
                            .append("path")
                            .attr("d",function(d,i){
                                return d3.arc()
                                    .innerRadius(0)
                                    .outerRadius(pie_r)(d);
                            })
                            .attr("fill",function(d,i){
                                return self.piecolorScale(i);
                            });
                });
                

                node
                    .append("text")
                    .attr("dy", "2em")
                    .attr("text-anchor", "middle")
                    .attr("fill", "#4d4d4d")
                    .attr("font-weight", "bold")
                    .text(d=>{
                        let show_str = d.data.tree_topickey.slice(0,3).toString()
                        // .replaceAll(",","; ")
                        return d.data.tree_topickey.length == 0 ? 'ROOT' : show_str;
                    })
                    .clone(true)
                    .lower()
                    .attr("stroke", "white");
                
                
            
                // ===================color tips=================//
                const corlortips = svg.append("g").attr("class", "story_tree_colortips")
                    .attr('transform', `translate(${innerWidth/5.5},${margin.top/2})`);
                
                let circles_tips = corlortips.selectAll("story_tree_colortips_icircle")
                    .data(self.mediasources)
                    .enter()
                    .append("g")
                    .attr("class", "story_tree_colortips_icircle");

                circles_tips.append("circle")
                    .attr("r", 5)
                    .attr("cx", (d,i) => {return i * 150 + 150})
                    .attr("fill", (d,i) => self.piecolorScale(i));

                circles_tips.append("text")
                    .attr("class", "story_tree_colortips_itext")
                    .attr("x", (d,i) => {return i * 150 + 150})
                    .attr("dy", "0.31em")
                    .attr("dx", "0.5em")
                    .attr("text-anchor", "start")
                    .attr("font-size", 15)
                    .attr("fill", (d,i) => self.piecolorScale(i))
                    .text(d=>{return d});
                
                
                // ===================node click=================//
                node.on("click", function(d) {
                    console.log(d);
                    self.UPDATE_TREE_NODE_CLICK(d.index + "+" + self.randomString(6));
                    self.drawer = true;
                });

                self.initLeftTopPos();

                // node.append("title")
                //     .text(d => self.title(d.data));
                function dist2(a, b) {
                    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2;
                }
                g.selectAll(".storytree__node")
                    .on("mouseover", function () {
                        const m = d3.mouse(this);
                        console.log("m:", m);
                        const leaf = node.data()[
                            d3.scan(node.data().map(d => dist2([reScale(d.data.time_e), d.x], m)))
                        ];
                        console.log("leaf:", leaf);
                        // 如果mouseover在了根节点上直接返回
                        if(leaf.data.name == 'ROOT' || leaf.time_e == 'time'){
                            return;
                        }

                        let d = root
                            .links()
                            .filter(d => d.target === leaf)
                            .pop().target;
                        
                        d.m0 = m[0];
                        d.m1 = m[1];
                        
                        // console.log("d:", d);
                        d3.select("body").select("#div"+d.index).classed("hover_tree_node_click_div_highlight", true);

                        // add tree node hover tooltip
                        let m_width = 200;
                        let m_height = 80;
                        let m_margin = { top: 10, right: 5, bottom: 25, left: 30 };
                        let m_innerWidth = m_width - m_margin.left - m_margin.right;
                        let m_innerHeight = m_height - m_margin.top - m_margin.bottom;

                        let div_top = self.divPos.top;
                        let div_left = self.divPos.left;
                        let div_height = self.divPos.height;
                        let div_width = self.divPos.width;

                        d3.select("body").selectAll(".tree_node_hover_tooltip_div").remove();

                        let add_div = d3.select("body").append("div")
                            .attr("class", "tree_node_hover_tooltip_div");
                        
                        let hover_summary = add_div.append("div")
                            .attr("class", "tree_node_hover_tooltip_div_sub")
                            .attr("id","hover_summary"+m[0]);
                        
                        var sub_div = document.getElementById("hover_summary"+m[0]);
                        sub_div.innerHTML += d.data.name.split("+")[0] + ".";
                        let sub_div_height = sub_div.getBoundingClientRect().height;
                        let m_height_all = m_height + sub_div_height
                        // add_div
                        //     .style('position','absolute')
                        //     .style('top', d=>{
                        //         // console.log("location: ", m[1], m_height_all, m[1] + m_height_all, div_height)
                        //         if(m[1] + m_height_all > div_height){
                        //             return (div_top + m[1] - m_height_all) + "px"
                        //         }
                        //         else{
                        //             return div_top + m[1] - m_height +"px"
                        //         }
                        //     })
                        //     .style('left', function(){
                        //         if(m[0] + m_width  > div_width){
                        //             return (div_left + m[0] - m_width) + "px"
                        //         }
                        //         else{
                        //             return div_left + m[0] - 2 * m_height_all + "px"
                        //         }
                        //     })
                        //     .style('width', m_width + "px")
                        //     .style('background-color', "white");

                        
                        // let hover_toltip = add_div.append("svg")
                        //     .attr("class", "tree_node_hover_tooltip")
                        //     .attr("width", m_width)
                        //     .attr("height", m_height_all)
                        //     .append("g")
                        //     .attr("transform",`translate(${m_margin.left} , ${m_margin.top} )`);
                        
                        // let x_Attrs = ["tone","impact","#mentions","#articles","#sources", "#ratio"]//"#nums"]
                        // let dataset = []
                        // dataset.push(+d.data.tree_vari_avgTone)
                        // dataset.push(+d.data.tree_vari_gold)
                        // dataset.push(+d.data.tree_vari_nummention)
                        // dataset.push(+d.data.tree_vari_numarticle)
                        // dataset.push(+d.data.tree_vari_numresouce)
                        // dataset.push(+d.data.tree_vari_mSrcN)

                        // // // Add X axis
                        // var x = d3.scaleBand()
                        //     .domain(x_Attrs)
                        //     .range([0, m_innerWidth])
                        //     .padding(0.1);
                        
                        // hover_toltip.append("g")
                        //     .attr("transform", "translate(0," + m_innerHeight + ")")
                        //     .call(d3.axisBottom(x).ticks(4))
                        //     .selectAll("text")
                        //     .attr("transform", "translate(-6,0)rotate(-30)")
                        //     .style("text-anchor", "end");
                        
                        // // Y axis
                        // var y = d3.scaleLinear()
                        //     .range([m_innerHeight, 0])
                        //     .domain(d3.extent(attrsMaxMin));
                        
                        // hover_toltip.append("g")
                        //     .attr("class", "hover_toltip_axisYg")
                        //     .call(d3.axisLeft(y).ticks(3));
                        
                        // hover_toltip.append("g").selectAll("rect")
                        //     .data(dataset)
                        //     .enter()
                        //     .append("rect")
                        //     .attr("class", "myRect")
                        //     .attr("fill", "steelblue")
                        //     .attr("opacity", 0.4)
                        //     .attr("x", function (d, i) {
                        //         return x(x_Attrs[i]);
                        //     })
                        //     .attr("y", function (d) {
                        //         return y(d);
                        //     })
                        //     .attr("width", x.bandwidth())
                        //     .attr("height", function (d) {
                        //         return m_innerHeight - y(d);
                        //     });   
                        // hover_toltip.selectAll(".hover_toltip_axisYg").append('text')
                        //     .attr('class', 'variance_of_characteristics')
                        //     .attr('y', 3)
                        //     .attr('x', m_innerWidth)
                        //     .attr('fill', '#606266')
                        //     .attr('font-size', '1.3em')
                        //     .style('text-anchor', 'end')
                        //     .text("features variance");
                        
                        // compute this path node selection
                        const path__node = [];
                        const path = [];
                        do {
                            path__node.push(d);
                            path.push(d.data);
                        } while ((d = d.parent));

                        // console.log("path:", path);
                        self.gridData = []
                        
                        path.reverse();
                        path.forEach(ele=>{
                            if(ele.time_e != "time"){
                                let dic = new Array();
                                dic['date'] = ele.time_e;
                                dic['name'] = ele.tree_topickey.toString();
                                let medias = ele.tree_nodeSrcN;
                                for(let i=0;i<self.mediasources.length;i++){
                                    console.log(medias[i]);
                                    console.log(self.mediasources[i]);
                                    dic[self.mediasources[i].replaceAll(".","")] = medias[i];
                                }
                                self.gridData.push(dic);
                            }
                        })
                        self.ego_path = path;
                        self.ego_path__node = path__node;
                        node.classed("highlight", d => path.indexOf(d.data) > -1);
                        node.classed("leaf", d => path.indexOf(d.data) === 0);
                        link.classed("highlight", d => path.indexOf(d.target.data) > -1);

                        sysDatasetObj.updateSankeyTreePathNode(self.ego_path);
                        self.UPDATE_CLICK_SANKEY_TREE_NODE_MODE();

                    })
                    .on("mouseout", function () {
                        
                        d3.select("body").selectAll(".tree_node_hover_tooltip_div").remove();

                        d3.select("body").selectAll(".tree_node_detail_tooltip_div")
                            .classed("hover_tree_node_click_div_highlight", false);


                        node.classed("highlight", false);
                        node.classed("leaf", false);
                        link.classed("highlight", false);
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
                })

            // let lineWidthScale = d3.scaleLinear().domain([0, 0.5]).range([1, 10]);
            // let lineFillScale = d3.scaleLinear().domain([0, 0.5]).range([0.4, 1]);
            
            let lineWidthScale = d3.scaleLinear().domain(d3.extent(tree_maxCompatibilityMaxMin)).range([2, 5]);
            let lineFillScale = d3.scaleLinear().domain(d3.extent(tree_maxCompatibilityMaxMin)).range([0.4, 1]);

            let reScaleCircleRadia = d3.scaleLinear().domain(d3.extent(biasMaxMin)).range([8,15]);
            // console.log(timescope);
            // console.log(reScale("time"));
            let tree = data => {
                let i = 0;
                const root = d3.hierarchy(data).eachBefore(d=>{d.index = i++;});
                // root.dx = innerHeight / (root.children.length + 3);
                // root.dy = innerWidth / (root.height + 3);
                // return d3.tree().nodeSize([root.dx, root.dy])(root);
                // return d3.tree().size([innerHeight,innerWidth])(root);
                return d3.cluster().size([innerHeight,innerWidth])(root);
            }
            let root = tree(data);
            renderStoryTree(root, reScale, reScaleCircleRadia, delta_timeScale, attrsMaxMin, dx, dy, timescope);

        },
    }
}
</script>
  
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.media-storytree-container {
    width: 100%;
    height: 100%;
}
</style>
<style lang="less">
.tree_node_hover_tooltip_div {
    border: 1px solid black;
    word-wrap: break-word;
    // font-family: sans-serif;
    font-size: 12px;
    padding: 5px;
    .tree_node_hover_tooltip_div_sub{
        border-bottom: 1px solid black;
        // display: block;
        word-wrap: break-word;
    }
}
.tree_node_detail_tooltip_div {
    border: 1px dashed black;
    word-wrap: break-word;
    // z-index: 9999;
    background-color: white;
    padding: 5px;
    line-height: 16px;
    overflow-y: auto;
    overflow-x: hidden;
    .close-icon {
        float: right;
        right: 10px;
    }
    .node_detail_span{
        font-size: 13px;
    }
    .node_detail_span_1{
        font-size: 13px;
        font-weight: bold;
    }
    .summary_container {
        margin-top: 5px;
        margin-top: 2%;
        // position: absolute;
        // overflow-y: auto;
        // top: 50%;
        // height: 50%;
        // left: 0%;
        // width: 100%;
        .summary_container_title{
            text-align: center;
            display: block;
            font-weight: bold;
        }
    }
    .detail_div_link_container{
        // position: absolute;
        // overflow-y: auto;
        // top: 0%;
        // height: 48%;
        // left: 0%;
        // width: 100%;
    }
}
</style>
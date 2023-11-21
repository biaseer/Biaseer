<template>
    <div class="media-sankeytree-container"
    id="div_id_sankeytree"
    v-loading="storytree__loading"
    element-loading-text="Waiting Loading Story Tree"
    ref="mediasankeytree">
        <svg id="sankeytree__svg"></svg>
    </div>
</template>
  
<script>

import { mapState, mapMutations } from 'vuex';
// import { sankey as sankeyGraph, sankeyLinkHorizontal } from "d3-sankey";
import { sankey } from '../assets/js/sankey';


export default {
    name: 'MediaSankeyTree',
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
            cuurent_root_path: null,
            cuurent_root_path_node: null,
            node_template: 0,
            cuurent_root_path_node2: null,
        }
    },
    computed: {
        ...mapState([
            'currMedium',
            'storytree_finish',
            'tree_node_click',
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
            self.drawSankeyTree(self.width, self.height);
        },
        tree_node_click: function () {
            let self = this;
            let click_node_id = self.tree_node_click.split("+").slice(0,1);
            console.log("self.tree_node_click", self.tree_node_click);
            console.log("self.ego_path__node", self.ego_path__node);

            let curr_click_node = self.ego_path__node.filter(ele => ele.index == click_node_id)[0];
            console.log("curr_click_node", curr_click_node);
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
        self.width = self.$refs.mediasankeytree.clientWidth;
        self.height = self.$refs.mediasankeytree.clientHeight;
        // self.drawSankeyTree(self.width, self.height);
    },
    methods: {
        ...mapMutations([
            'UPDATE_TREE_NODE_CIRCLE_CLICK',
            'UPDATE_TREE_NODE_CLICK',
            'UPDATE_TREE_NODE_CLICK_PATH_LIST',
            'UPDATE_CLICK_SANKEY_TREE_NODE_MODE'
        ]),
        initLeftTopPos: function() {
            let odiv=document.getElementById('story_tree_div');
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
        drawSankeyTree(width, height) {
            let self = this;

            let margin = { top:15, bottom:55, left:10, right:20 };
            let innerWidth = width - margin.left - margin.right;
            let innerHeight = height - margin.top - margin.bottom;
            

            let renderSankeyTree = (root, sankeyData, biasMaxMin, wordSizeScale, wordListCountDict, reScale, reScaleCircleRadia, delta_timeScale, attrsMaxMin, dx, dy, timescope) => {
                let x0 = Infinity;
                let x1 = -x0;
                root.each(d => {
                    if (d.x > x1) x1 = d.x;
                    if (d.x < x0) x0 = d.x;
                });
                // clear before
                d3.select(self.$el).select("#sankeytree__svg").selectAll('g').remove();
                
                const svg = d3.select(self.$el).select("#sankeytree__svg")
                    .attr("width", width)
                    .attr("height", height)
                    .attr("viewBox", [0, 0, width, height])
                    .attr("style", "max-width: 100%; height: auto; font: 10px sans-serif;");
                
                const sankey = d3.sankey()
                    .nodeWidth(15)
                    .nodePadding(10)
                    .size([innerWidth, innerHeight]);
                
                let path = sankey.link();

                sankey
                    .nodes(sankeyData.nodes)
                    .links(sankeyData.links)
                    .nodeWidth(15)
                    .nodePadding(10)
                    .layout(32);
                
                // Defines a color scale.
                // const color = d3.scaleOrdinal(d3.schemeCategory10);
                const color = d3.scaleLinear().domain(d3.extent(biasMaxMin))
                    .range(["#ecf8ff", "#50bfff"])

                // add in the links
                var link = svg.append("g")
                    .attr('transform', `translate(${reScale.bandwidth()/2},${0})`)
                    .selectAll(".link")
                    .data(sankeyData.links)
                    .enter()

                var paths = link.append("path")
                    .attr("d", path)
                    .attr("fill", "none")
                    .attr("stroke-width", function (d) { return Math.max(1, d.dy); })
                    .attr("stroke", d => color(d.target.totalbias))
                    .attr("id", (d,i) => {return 'link' + i })
                    // .attr("stroke", "gray")
                    .attr("stroke-opacity", "0.5")
                    .sort(function (a, b) { return b.dy - a.dy; });

                // add the link titles
                // link.append("title")
                //     .text(function (d) {
                //         return d.source.name + " → " +
                //             d.target.name + "\n" + d.value;
                //     });
                
                let colorWord = d3.scaleOrdinal(d3.schemePaired);
                // let colorWord =()=>{return 'gray'};
                // add the link path text
                link.append('text')
                    .append('textPath')
                    .attr('xlink:href', function (d,i) { return '#link' + i; })
                    .selectAll(".tspan")
                    .data(d=>d.target.tree_topickey)
                    .enter()
                    .append("tspan")
                    .attr("font-size", d=> wordSizeScale(wordListCountDict[d])+"px" )
                    .attr("fill", (d,i)=> {return colorWord(i)})
                    .attr("y", '0.35em')
                    .text(function (d) { 
                        if(wordSizeScale(wordListCountDict[d]) > 10)
                            return "  " + d
                    })
                    // .text(function (d) { return d.target.title.split("+")[0]; })

                // add in the nodes
                var node = svg.append("g")
                    .attr("class", "sankeytree__node")
                    .attr('transform', `translate(${reScale.bandwidth()/2},${0})`)
                    .selectAll(".node")
                    .data(sankeyData.nodes)
                    .enter().append("g")
                    .attr("class", "node")
                    .attr("transform", function (d) {
                        return "translate(" + d.xPos + "," + d.y + ")";
                    })
                    .call(d3.drag()
                        .subject(function (d) {
                            return d;
                        })
                        .on("start", function () {
                            this.parentNode.appendChild(this);
                        })
                        .on("drag", dragmove));
                
                // add the rectangles for the nodes
                node.append("rect")
                    .attr("height", function (d) { return d.dy; })
                    .attr("width", sankey.nodeWidth())
                    // .attr("fill", "gray");
                    .attr("fill", d => {
                        if(d.title == "ROOT") return "white"
                        return color(d.totalbias)
                    })
                    .attr("stroke", "gray")
                    .attr("stroke-width", 1);
                
                node.append("title")
                    .text(d=>d.title);
                
                // add in the title for the nodes
                // node.append("text")
                //     .attr("x", -6)
                //     .attr("y", function (d) { return d.dy / 2; })
                //     .attr("dy", ".35em")
                //     .attr("text-anchor", "end")
                //     .attr("transform", null)
                //     .text(function (d) { return d.name; })
                //     .filter(function (d) { return d.x < width / 2; })
                //     .attr("x", 6 + sankey.nodeWidth())
                //     .attr("text-anchor", "start");

                // the function for moving the nodes
                function dragmove(d) {
                    d3.select(this).attr("transform",
                        "translate(" + (
                            d.xPos
                        )
                        + "," + (
                            d.y = Math.max(0, Math.min(height - d.dy, d3.event.y))
                        ) + ")");
                    sankey.relayout();
                    paths.attr("d", path);
                }

                // initdivPos
                self.initLeftTopPos();
                // func dist2
                function dist2(a, b) {
                    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2;
                }
                svg.selectAll(".sankeytree__node")
                    .on("mouseover", function () {

                        const m = d3.mouse(this);
                        // console.log("m:", m);
                        // console.log("node.data():", node.data());

                        const leaf = node.data()[
                            d3.scan(node.data().map(d => dist2([reScale(d.time_e), d.y], m)))
                        ];
                        // console.log("leaf:", leaf);
                        // 如果mouseover在了根节点上直接返回
                        if(leaf.title == 'ROOT' || leaf.time_e == 'time'){
                            return;
                        }
                        let d = root
                            .links()
                            .filter(d => {
                                // console.log(d)
                                return d.target.index === leaf.name; // 目的是为了获取当前mouseover的节点
                            })
                            .pop().target;
                        d.m0 = m[0];
                        d.m1 = m[1];
                        // console.log("d:", d);

                        //obtain the path from this node
                        self.mediasources = d.data.mSrc_list;

                        self.node_template = d;

                        const path__node = [];
                        const path = [];
                        do {
                            path__node.push(self.node_template);
                            path.push(self.node_template.data);
                        } while ((self.node_template = self.node_template.parent));


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
                        self.cuurent_root_path = path;
                        self.cuurent_root_path_node = path__node;
                        console.log('cuurent_root_path', self.cuurent_root_path)
                        sysDatasetObj.updateSankeyTreePathNode(self.cuurent_root_path);
                        self.UPDATE_CLICK_SANKEY_TREE_NODE_MODE();
                        console.log(sysDatasetObj.SankeyTreePathNode)
                        

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
                        add_div
                            .style('position','absolute')
                            .style('top', d=>{
                                // console.log("location: ", m[1], m_height_all, m[1] + m_height_all, div_height)
                                if(m[1] + m_height_all > div_height){
                                    return (div_top + m[1] - m_height_all) + "px"
                                }
                                else{
                                    return div_top + m[1] - m_height +"px"
                                }
                            })
                            .style('left', function(){
                                if(m[0] + m_width  > div_width){
                                    return (div_left + m[0] - m_width) + "px"
                                }
                                else{
                                    return div_left + m[0] - 2 * m_height_all + "px"
                                }
                            })
                            .style('width', m_width + "px")
                            .style('background-color', "white");

                        let hover_toltip = add_div.append("svg")
                            .attr("class", "tree_node_hover_tooltip")
                            .attr("width", m_width)
                            .attr("height", m_height_all)
                            .append("g")
                            .attr("transform",`translate(${m_margin.left} , ${m_margin.top} )`);

                        let x_Attrs = ["tone","impact","#mentions","#articles","#sources", "#ratio"]//"#nums"]
                        let dataset = []
                        dataset.push(+d.data.tree_vari_avgTone)
                        dataset.push(+d.data.tree_vari_gold)
                        dataset.push(+d.data.tree_vari_nummention)
                        dataset.push(+d.data.tree_vari_numarticle)
                        dataset.push(+d.data.tree_vari_numresouce)
                        dataset.push(+d.data.tree_vari_mSrcN)
                        // // Add X axis
                        var x = d3.scaleBand()
                            .domain(x_Attrs)
                            .range([0, m_innerWidth])
                            .padding(0.1);

                        hover_toltip.append("g")
                            .attr("transform", "translate(0," + m_innerHeight + ")")
                            .call(d3.axisBottom(x).ticks(4))
                            .selectAll("text")
                            .attr("transform", "translate(-6,0)rotate(-30)")
                            .style("text-anchor", "end");

                        // Y axis
                        var y = d3.scaleLinear()
                            .range([m_innerHeight, 0])
                            .domain(d3.extent(attrsMaxMin));

                        hover_toltip.append("g")
                            .attr("class", "hover_toltip_axisYg")
                            .call(d3.axisLeft(y).ticks(3));

                        hover_toltip.append("g").selectAll("rect")
                            .data(dataset)
                            .enter()
                            .append("rect")
                            .attr("class", "myRect")
                            .attr("fill", "steelblue")
                            .attr("opacity", 0.4)
                            .attr("x", function (d, i) {
                                return x(x_Attrs[i]);
                            })
                            .attr("y", function (d) {
                                return y(d);
                            })
                            .attr("width", x.bandwidth())
                            .attr("height", function (d) {
                                return m_innerHeight - y(d);
                            });   
                        hover_toltip.selectAll(".hover_toltip_axisYg").append('text')
                            .attr('class', 'variance_of_characteristics')
                            .attr('y', 3)
                            .attr('x', m_innerWidth)
                            .attr('fill', '#606266')
                            .attr('font-size', '1.3em')
                            .style('text-anchor', 'end')
                            .text("features variance");
                    })

                    .on("mouseout", function () {
                        
                        d3.select("body").selectAll(".tree_node_hover_tooltip_div").remove();

                        d3.select("body").selectAll(".tree_node_detail_tooltip_div")
                            .classed("hover_tree_node_click_div_highlight", false);
                    })
                
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
                    .attr('rx', d=> delta_timeScale(d) / 2)
                    .attr('width', reScale.bandwidth() - 2 * delta_time_space)
                    .attr('height', d=> delta_timeScale(d))
                    .on("mouseover", function(d) {
                        d3.select(this).classed("line-hover", true);
                    })
                    .on("mouseout", function(d) {
                        d3.select(this)
                            .classed("line-hover", false);
                    });
                
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

            // let reScale = d3.scaleBand().domain(timescope).range([0, innerWidth]);
            let reScale = d3.scaleBand().domain(timescope).range([0, width]);
            // console.log(timescope);
            // console.log(reScale("time"));


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

            let lineWidthScale = d3.scaleLinear().domain(d3.extent(tree_maxCompatibilityMaxMin)).range([2, 5]);
            let lineFillScale = d3.scaleLinear().domain(d3.extent(tree_maxCompatibilityMaxMin)).range([0.4, 1]);

            let reScaleCircleRadia = d3.scaleLinear().domain(d3.extent(biasMaxMin)).range([5,10]);

            let sankeyData = {nodes: [], links: []};

            let tree = data => {
                let i = 0;
                const root = d3.hierarchy(data).eachBefore(d=>{
                    d.index = i++;
                    d.size = d.leaves().length;
                    sankeyData.nodes.push({name: d.index, xPos: reScale(d.data.time_e), node: "node" + d.index, title: d.data.name, time_e: d.data.time_e,
                    tree_topickey: d.data.tree_topickey, totalbias: +d.data.totalbias});
                });
                root.each(d=>{
                    if(d.children){
                        d.children.forEach(eleChild=>{
                            sankeyData.links.push({source: d.index, target: eleChild.index, value: eleChild.size});
                        })
                    }
                })
                // const root = d3.hierarchy(data).eachBefore(d=>{d.index = i++; d.size = d.descendants().length <= 2 ? 1 : d.descendants().length - 1});
                // return d3.tree().size([innerHeight,innerWidth])(root);
                return d3.cluster().size([innerHeight,innerWidth])(root);
            }
            let root = tree(data);
            // console.log(root);

            // sankeyData = {nodes: root.descendants(), links: root.links()};
            console.log(sankeyData);


            let wordList = [];
            root.each(d=>{
                if(d.data.name == 'ROOT' || d.data.time_e == 'time'){return}
                wordList.push(...d.data.tree_topickey)
                wordList.push(...d.data.tree_keyword.flat())
                wordList.push(...d.data.tree_titlekeyword.flat())
            })
            const wordListCountDict = wordList.reduce((obj,key)=>{
                if (key in obj){
                    obj[key]++
                }else{
                    obj[key]=1
                }
                return obj
            },{})
            let wordSizeScale = d3.scaleLinear().domain(d3.extent(Object.values(wordListCountDict)))
                .range([10, 60])

            renderSankeyTree(root, sankeyData, biasMaxMin, wordSizeScale, wordListCountDict, reScale, reScaleCircleRadia, delta_timeScale, attrsMaxMin, dx, dy, timescope);

        },
    }
}
</script>
  
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.media-sankeytree-container {
    width: 100%;
    height: 100%;
}
</style>
<style lang="less">
.tree_node_hover_tooltip_div {
    border: 1px solid black;
    word-wrap: break-word;
    font-size: 12px;
    padding: 5px;
    .tree_node_hover_tooltip_div_sub{
        border-bottom: 1px solid black;
        word-wrap: break-word;
    }
}
.tree_node_detail_tooltip_div {
    border: 1px dashed black;
    word-wrap: break-word;
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
        .summary_container_title{
            text-align: center;
            display: block;
            font-weight: bold;
        }
    }
}
</style>
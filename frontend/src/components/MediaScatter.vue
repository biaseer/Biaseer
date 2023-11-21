<template>
    <div class="media-scatter-container" ref="mediascatter">
        <div class="flow-node-menu" id="nodeMenu" v-show="nodeMenuFlag">
            <div class="prop-menu-item">
                <el-button size="mini" @click="addFunc">add</el-button>
            </div>
            <div class="prop-menu-item">
                <el-button size="mini" @click="keepFunc">keep</el-button>
            </div>
            <div class="prop-menu-item">
                <el-button size="mini" @click="cancelFunc">cancel</el-button>
            </div>
        </div>
    </div>
</template>

<script>

import { mapState, mapMutations } from 'vuex';
import { getTopic } from '../assets/data/topicList'

export default {
    name: 'MediaScatter',
    props: {
        msg: String
    },
    data() {
        return {
            width: null,
            height: null,
            innerWidth: null,
            innerHeight: null,
            overlap: 2,
            margin: null,
            step: null,
            color: null,
            mirror: null,
            xValue: null,
            yValue: null,
            max: null,
            yScale: null,
            xScale: null,
            tmpdata: null,
            draw_data: null,
            data: null,
            svg: null,
            horizong: null,
            xg: null,
            clipPath: null,
            mouse_this: null,
            horizon_chart_class: null,
            right_click_div_class: null,
            lineGenerator: null,
            nodeMenuFlag: false,
            graph_g: null,
            label_g: null,
            zoomOperator: null,
            zoomMaxRatio: 16,
            zoomMinRatio: 1,
            rightDiv: null,
            currentViewedMediaList: null, // when zooming, can be viewed media
            filtering_data: null,
        }
    },
    mounted: function () {
        this.width = this.$refs.mediascatter.clientWidth;
        this.height = this.$refs.mediascatter.clientHeight;
        this.drawContour(this.width, this.height);
    },
    computed: {
        ...mapState([
            'currMedium',
            'mediaGraphLabel',
            'contour_search_domain',
            'isConcated'
        ]),
    },
    watch: {
        currMedium: function () {
            let self = this;
            // drawMediaHorizonChart
            // self.gainMediaHorizonChartData(self.currMedium);
            // self.drawMediaHorizonChart(self.currMedium);
        },
        mediaGraphLabel: function() {
            let self = this;
            self.drawMediaGraph([ ...sysDatasetObj.mediaGraphList, ...sysDatasetObj.mediaScatterSelected]);
        },
        contour_search_domain: function(){
            let self = this
            let search_domain = this.contour_search_domain;
            if(search_domain != ""){
                let node = this.filtering_data.filter(ele=>ele.domain == search_domain)[0];
                let nodePos = [self.xScale(node.x1),self.yScale(node.x2)];
                let zoomingRatio = self.zoomMaxRatio / 2;
                self.zoomOperation(node, nodePos, zoomingRatio);
            }
        },
        isConcated:function(){
            console.log(this.isConcated)
            let self = this
            if(!this.isConcated){
                let selected_media_len = sysDatasetObj.mediaScatterSelected.length
                console.log(selected_media_len)
                if(selected_media_len > 0){
                    self.UPDATE_CURRENT_MEDIUM(sysDatasetObj.mediaScatterSelected[selected_media_len - 1]);
                }else{
                    sysDatasetObj.mediaScatterSelected.push("msn.com");
                    self.UPDATE_CURRENT_MEDIUM("msn.com");
                }
            }
        }
    },
    methods: {
        ...mapMutations([
            'UPDATE_CURRENT_MEDIUM',
            'UPDATE_MEDIA_SCATTER_CLICK',
            'UPDATE_MEDIA_GRAPH_LABEL'
        ]),
        moveToCenterScale: function (point, zoomingRatio) {
            let self = this
            let treeVisMapCanvasHeight = self.$refs.mediascatter.clientWidth;
            let treeVisMapCanvasWidth = self.$refs.mediascatter.clientHeight;
            return d3.zoomIdentity
                .translate(treeVisMapCanvasHeight / 2, treeVisMapCanvasWidth / 2)
                .scale(zoomingRatio)
                .translate(-point[0], -point[1]);
        },
        zoomOperation: function(node, nodePos, zoomingRatio, callbackFunc=null) {
            let self = this
            let zoomOperator = self.zoomOperator;
            let transformEvent = self.moveToCenterScale(nodePos, zoomingRatio);
            self.transformEvent = transformEvent;
            d3.select(self.$el)
                .select('.media__contour__svg')
                .transition()
                .duration(3000)
                .call(zoomOperator.transform, transformEvent)
                .on("end", function() {
                    // self.updateZoomingRatio(transformEvent)
                    if (callbackFunc != null) {
                        callbackFunc(transformEvent)
                    }
                    self.unhighlightSearchDots();
                    self.highlightSearchDot(node.domain);
                });
        },
        unhighlightSearchDots(){
            // unhighlight all media
            d3.select(this.$el)
                .select(".media__contour__svg")
                .select(".media-point-circle-g")
                .selectAll("circle").classed("dot-search-hover", false);
                
            d3.select(this.$el)
                .select(".media__contour__svg")
                .select(".media-point-label-g")
                .selectAll("text_label").remove();
        },
        highlightSearchDot(domain){
            // highlight searched media
            d3.select(this.$el)
                .select(".media__contour__svg")
                .select(".media-point-circle-g")
                .select("#media_id_"+ domain.replaceAll(".","_")).classed("dot-search-hover", true);
        },
        keepFunc(){
            let self = this;
            // add currmedium to keep queue
            sysDatasetObj.keepMediaQueue.push(self.currMedium);
            // update
            self.UPDATE_MEDIA_GRAPH_LABEL();
            sysDatasetObj.updateMediaGraphList(self.currMedium);
            self.nodeMenuFlag = false;
        },
        cancelFunc(){
            let self = this;
            // cancel currmedium to keep queue
            sysDatasetObj.keepMediaQueue = sysDatasetObj.keepMediaQueue.filter(item => item !== self.currMedium);
            // update
            self.UPDATE_MEDIA_GRAPH_LABEL();
            sysDatasetObj.updateMediaGraphList(self.currMedium);            
            self.nodeMenuFlag = false;
        },
        addFunc(){
            let self = this;
            self.UPDATE_MEDIA_SCATTER_CLICK();
            sysDatasetObj.updateMediaScatterSelected(self.currMedium);
            self.nodeMenuFlag = false;
        },
        drawContour(width, height) {
            // https://vizhub.com/curran/65a26f760f5b4d3f976d1cd7cb43a221

            let self = this;

            d3.select(self.$el)
                .select(".media__contour__svg")
                .remove();

            const xValue = d => d.x1;
            const yValue = d => d.x2;
            const rValue = d => d.nums;

            const margin = { top: 4, right: 9, bottom: 4, left: 4 };
            const innerWidth = width - margin.left - margin.right;
            const innerHeight = height - margin.top - margin.bottom;

            const svg = d3
                .select(self.$el)
                .append("svg")
                .attr("class", "media__contour__svg")
                .attr("width", innerWidth)
                .attr("height", innerHeight)
                .attr("transform", `translate(${margin.left}, ${margin.top})`)
                // .attr('viewBox', [0, 0, 0.5 * width, 0.5 * height])

            let contour_g = svg.append("g")
                .attr("class", "media-point-contour-g")

            let graph_g = svg.append("g")
                .attr("class", "media-point-graph-g")
            self.graph_g = graph_g;

            let circle_g = svg.append("g")
                .attr("class", "media-point-circle-g")
            
            let label_g = svg.append("g")
                .attr("class", "media-point-label-g")
            self.label_g = label_g;
            
            let rightDiv = d3.select('.media-scatter-container')
                .select('.flow-node-menu');
            self.rightDiv = rightDiv;

            let xScale = d3.scaleLinear().range([0, innerWidth]);
            let yScale = d3.scaleLinear().range([innerHeight, 0]);
            let rScale = null;

            let xScaleCopy = xScale.copy();
            let yScaleCopy = yScale.copy();

            const colorScale = d3.scaleSequential(d3.interpolate(d3.interpolateReds(0), d3.interpolateReds(0.4)));
            let zoomScale_k = null;
            const t = svg.transition().duration(1000);
            const circle_r = 3.5;


            function xyScale(data) {
                xScale.domain(d3.extent(data, xValue));
                yScale.domain(d3.extent(data, yValue));
                let rMaxMin = d3.extent(data, rValue);
                console.log(rMaxMin);
                let system_topic_event = "RUS_UKR"
                rScale = (event_num) => {
                    if(system_topic_event == "RUS_UKR"){
                        if(event_num < 70) return d3.scaleLinear().domain([rMaxMin[0], 70]).range([1.5, 3])(event_num);
                        else if(event_num < 90) return d3.scaleLinear().domain([71, 90]).range([3.1, 6])(event_num);
                        else if(event_num < 150) return d3.scaleLinear().domain([91, 150]).range([6.1, 7])(event_num);
                        else if(event_num < 200) return d3.scaleLinear().domain([151, 200]).range([7.1, 9])(event_num);
                        else if(event_num < 300) return d3.scaleLinear().domain([201, 300]).range([9.1, 10])(event_num);
                        else if(event_num < 500) return d3.scaleLinear().domain([301, 500]).range([10.1, 11])(event_num);
                        else return d3.scaleLinear().domain([501, rMaxMin[1]]).range([11.1, 13])(event_num);
                    }
                }
                self.xScale = xScale;
                self.yScale = yScale;
                xScaleCopy.domain(d3.extent(data, xValue));
                yScaleCopy.domain(d3.extent(data, yValue));
            }

            function renderContours(data, bandwidth) {
                const contourData = d3.contourDensity()
                    .x(d => xScale(xValue(d)))
                    .y(d => yScale(yValue(d)))
                    .size([innerWidth, innerHeight])
                    .bandwidth(bandwidth)
                    (data);

                colorScale.domain(d3.extent(contourData, d => d.value));

                const contours = contour_g
                    .attr("stroke-linejoin", "round")
                    .selectAll("path").data(contourData);

                contours
                    .join(
                        enter => enter.append("path")
                            .attr("d", d3.geoPath())
                            .attr("fill", d => colorScale(d.value)),
                        update => update
                            .call(update => update
                                .attr("d", d3.geoPath())
                                .attr("fill", d => colorScale(d.value))
                            ),
                        exit => exit
                            .remove()
                    );
            }

            function renderCircles(data) {

                const circles = circle_g
                    .selectAll(".dot")
                    .data(data);

                circles
                    .join(
                        enter => enter.append("circle")
                            .attr("class", "dot")
                            .attr("fill-opacity", 0.5)
                            .attr("transform", transform)
                            .attr("id", d => "media_id_" + d.domain.replaceAll(".", "_"))
                            .attr("cx", function (d) { return xScale(d.x1); })
                            .attr("cy", function (d) { return yScale(d.x2); })
                            .attr("r", d => rScale(d.nums)),
                        update => update
                            .call(update => update
                                .attr("transform", transform)
                                .attr("id", d => "media_id_" + d.domain.replaceAll(".", "_"))
                                .attr("cx", function (d) { return xScale(d.x1); })
                                .attr("cy", function (d) { return yScale(d.x2); })
                                .attr("r", d => rScale(d.nums))),
                        exit => exit
                            .remove()
                    )
                    .on("mouseover", function (d) {
                        self.UPDATE_CURRENT_MEDIUM(d.domain);
                        
                        // update mouseLocation
                        self.mouse_this = d3.mouse(this);

                        // hover highlight
                        d3.select(this).classed("dot_mouseover1", true);
                        
                        // draw mediagraph
                        // 更改要画的媒体列表
                        sysDatasetObj.updateMediaGraphList(d.domain);
                        // 更改一个标记
                        self.UPDATE_MEDIA_GRAPH_LABEL();
                        // 画出这个graph
                        // 监听画出这个graph
                        // self.drawMediaGraph([d.domain]);

                        // hidden nodeMenu
                        self.nodeMenuFlag = false;
                    })
                    .on("mouseout", function (d) {
                        d3.select(this).classed("dot_mouseover1", false);
                        sysDatasetObj.mediaGraphList.splice(sysDatasetObj.mediaGraphList.indexOf(d.domain), 1);
                        // self.UPDATE_MEDIA_GRAPH_LABEL();

                        // judge concat info
                        console.log(self.isConcated)
                        if(self.isConcated){
                            self.UPDATE_MEDIA_SCATTER_CLICK();
                        }else{
                            let selected_media_len = sysDatasetObj.mediaScatterSelected.length
                            console.log(selected_media_len)
                            if(selected_media_len > 0){
                                self.UPDATE_CURRENT_MEDIUM(sysDatasetObj.mediaScatterSelected[selected_media_len - 1]);
                            }else{
                                sysDatasetObj.mediaScatterSelected.push("msn.com");
                                self.UPDATE_CURRENT_MEDIUM("msn.com");
                            }
                        }
                    })
                    .on("click", function (d) {
                        // self.UPDATE_MEDIA_SCATTER_CLICK();
                        // sysDatasetObj.updateMediaScatterSelected(d.domain);
                    })
                    .on("contextmenu", d => {
                        d3.event.preventDefault();
                        self.nodeMenuFlag = true;
                        // add a div
                        self.rightClickDiv();
                    })
            }

            function transform(d) {
                return `translate(${0}, ${0})`;
            }

            let data = sysDatasetObj.mediaDataSet;
            data['details'].forEach(d => {
                d.x1 = +d.x1;
                d.x2 = +d.x2;
                d.id = +d.id;
                d.nums = +d.nums;
            });

            // console.log('data:', data);
            let tdata = data['details'];
            self.filtering_data = tdata;

            xyScale(tdata);
            renderCircles(tdata);
            renderContours(tdata, 10);

            self.zoomOperator = d3.zoom()
                .extent([[0, 0], [innerWidth, innerHeight]])
                .scaleExtent([self.zoomMinRatio, self.zoomMaxRatio])
                .duration(1000)
                .on("zoom", zoomed)
                .on("end", d=>{
                    // zoom end, to redraw graph
                    console.log("zoom end...");
                    self.unhighlightSearchDots();
                });
            svg.call(self.zoomOperator);
            
            function zoomed() {
                // 1. clear media circle tooltip.
                circle_g
                    .select(".circlr_g__contour_tooltip")
                    .remove();
                // 2. rescale x y.
                xScale = d3.event.transform.rescaleX(xScaleCopy);
                yScale = d3.event.transform.rescaleY(yScaleCopy);

                // 3. get zoom scale.
                let zoomScale_k = d3.event.transform.k;
                // tdata = data.filter(d=> +d["zoom_"+Math.floor(zoomScale_k-1)] == 1);
                tdata = data["details"];
                // 4. transform media circle.
                d3.select(self.$el).selectAll(".dot").attr("transform", transform);
                // 5. render circles.
                renderCircles(tdata);
                // 6. filter media which can be viewed.
                let dots = d3.select(self.$el).selectAll(".dot").filter(function() {
                    return d3.select(this).attr("cx") > margin.left &&
                    d3.select(this).attr("cx") < innerWidth &&
                    d3.select(this).attr("cy") > margin.top &&
                    d3.select(this).attr("cy") < innerHeight;
                });
                // console.log("dots: ", dots);

                tdata = [];
                self.currentViewedMediaList = [];
                dots.filter(d=>{
                    tdata.push(d);
                    self.currentViewedMediaList.push(d.domain);
                });
                renderCircles(tdata);
                renderContours(tdata, 10);

                self.UPDATE_MEDIA_GRAPH_LABEL();
            }
        },
        drawMediaHorizonChart(domain) {
            console.log(domain);
            let self = this;
            let width = 761 / 2;
            let height = 293 / 2;

            let delta = 30;

            self.horizon_chart_class = "media_horizon_chart_tooltip_div";
            d3.select("body").selectAll("." + self.horizon_chart_class).remove();

            let add_div = d3.select("body").append("div")
                .attr("class", self.horizon_chart_class)
                .attr("id", "div1024")
                .style('position', 'absolute')
                .style('top', d => {
                    return delta + self.mouse_this[1] + "px";
                })
                .style('left', function () {
                    return delta + self.mouse_this[0] + "px"
                })
                .style('width', width + "px")
                .style('height', height + 19 + "px");

            add_div.append("i")
                .attr("class", "el-icon-close close-icon")
                .on("click", function () {
                    d3.select("body").select("#div1024").remove();
                })

            add_div.append("div")
                .append("span")
                .attr("class", "summary_container_title")
                .text(domain)

            self.move("div1024");
            self.drawMediaHorizonChartII(width, height, self.horizon_chart_class);
        },
        drawMediaHorizonChartII(width, height, selected_div) {
            let self = this;
            //==================
            self.overlap = 2;

            self.margin = { top: 0, right: 0, bottom: 0, left: 0 };
            self.innerWidth = width - self.margin.left - self.margin.right;
            self.innerHeight = height - self.margin.top - self.margin.bottom;

            self.step = (height - (self.margin.top + self.margin.bottom)) / self.draw_data.length - 1;
            let colorArr = ["#c73b3b", "#f06565", "#4393c3", "#92c5de", "#d6604d", "#fddbc7", "#f4a582"];
            self.color = i => colorArr[i + (i >= 0) + self.overlap];
            self.mirror = false;
            self.xValue = d => new Date(d.date);
            self.yValue = d => d.value + d.value1;
            self.max = d3.max(self.data, d => Math.abs(self.yValue(d)));
            self.yScale = d3.scaleLinear().range([self.overlap * self.step, -self.overlap * self.step]).domain([-self.max, +self.max]);
            self.xScale = d3.scaleTime().range([0, width]).domain(d3.extent(self.data, self.xValue));

            self.xAxis = g => g
                .attr("transform", `translate(0,${self.margin.top})`)
                .call(d3.axisTop(self.xScale).ticks(width / 40).tickSizeOuter(0))
                .call(g => g.selectAll(".tick").filter(d => self.xScale(d) < self.margin.left || self.xScale(d) >= width - self.margin.right).remove())
                .call(g => g.select(".domain").remove());

            self.areaGenerator = d3.area()
                .curve(d3.curveBasis)
                .x(d => self.xScale(self.xValue(d)))
                .y0(d => 0)
                .y1(d => self.yScale(self.yValue(d)));

            self.svg = d3.select("." + selected_div)
                .append("svg")
                .attr("width", width)
                .attr("height", height)
                .attr("viewBox", [0, 0, width, height])
                .attr("style", "font: 6px sans-serif;");

            self.horizong = self.svg.append("g").attr("class", "horizon-graph");

            self.horizong.selectAll('g').remove();

            self.clipPath = self.horizong.selectAll("g")
                .data(self.draw_data)
                .enter().append("g")
                .attr("class", "horizon-graph-sub")
                .attr("transform", (d, i) => `translate(0,${i * (self.step + 1) + self.margin.top})`)

            self.clipPath.append("clipPath")
                .attr("id", (d, i) => "area-clip-" + i)
                .append("rect")
                .attr("width", width)
                .attr("height", self.step);

            self.clipPath.append("defs").append("path")
                .attr("id", (d, i) => {
                    d.path = { 'id': "path-defs-" + i, 'href': '#path-defs-' + i }
                    return "path-defs-" + i;
                })
                .attr("d", d => self.areaGenerator(d.values));

            self.clipPath.append("g")
                .attr("clip-path", (d, i) => "url(#area-clip-" + i + ")")
                .selectAll("use")
                .data(d => {
                    return Array.from(
                        { length: self.overlap * 2 },
                        (_, i) => {
                            return Object.assign({ index: i < self.overlap ? -i - 1 : i - self.overlap }, d)
                        }
                    )
                })
                .enter().append("use")
                .attr("fill", d => {
                    return self.color(d.index)
                })
                .attr("transform", d => self.mirror && i < 0
                    ? `scale(1,-1) translate(0,${d.index * self.step})`
                    : `translate(0,${(d.index + 1) * self.step})`)
                .attr("xlink:href", d => d.path.href);

            self.clipPath.append("text")
                .attr("x", 4)
                .attr("y", self.step / 2)
                .attr("dy", "0.35em")
                .text(d => getTopic(d.key));
        },
        gainMediaHorizonChartData(domain) {
            let self = this;
            self.domain = domain;
            self.tmpdata = sysDatasetObj.mediaDataSet['details'].filter(ele => ele['domain'] == self.domain)[0];
            self.data = Object.values(self.tmpdata['doctone']).flat();
            self.draw_data = Object.values(self.tmpdata['doctone']).map(function (item, id) {
                return { 'key': id + 1, 'values': item };
            });
        },
        move(div_id) {
            console.log('div_id', div_id);
            var _move = false;
            div_id = '#' + div_id
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
        rightClickDiv(){
            let self = this;
            console.log(self.mouse_this);
            let width = 70;
            let height = 30;

            let delta = 20;

            // let rightDiv = d3.select('.media-scatter-container')
            //     .select('.flow-node-menu');
            self.rightDiv.attr("transform", d3.zoomTransform(this));
            self.rightDiv.style('top', d => {
                    return delta + self.mouse_this[1] + "px";
                })
                .style('left', function () {
                    return delta + self.mouse_this[0] + "px"
                })
                .style('width', width + "px")
                .style('height', height + "px")
        },
        clearHorizonGraphTooltip() {
            let self = this;
            d3.select("body").selectAll("." + self.horizon_chart_class).remove();
        },
        drawMediaGraph(domains) {
            let self = this;
            let mediagraph = sysDatasetObj.mediaDataSet['mediagraph'];
            
            let domainOneStep = {}
            let circlesLocation = {}
            domains.forEach(domain => {
                let domainLinks = {}
                Object.entries(mediagraph).forEach(([key, value]) => {
                    if (key.split("_").includes(domain)) {
                        domainLinks[key] = value
                    }
                });
                let items = Object.keys(domainLinks).map((key) => { return [key, domainLinks[key]] });
                items.sort(
                    (first, second) => { return second[1] - first[1] }
                );
                let keys = items.map(e=>e[0]);
                

                let circles = d3.select(self.$el).select(".media__contour__svg").select(".media-point-circle-g").selectAll('circle')
                // let circlesLocation = {}
                circles.each(function () {
                    const thisD3 = d3.select(this)
                    d3.select(this).classed("dot_mouseover", false);
                    d3.select(this).classed("dot-keep-domain-hover", false);
                    d3.select(this).attr("fill-opacity", 0.5);
                    circlesLocation[thisD3.attr('id').split('media_id_')[1]] = [+thisD3.attr('cx'), +thisD3.attr('cy')]
                })

                for(let i = 0; i < 5; i++){
                    let link_domain = keys[i].split("_");
                    let path = [];
                    if(self.currentViewedMediaList.includes(link_domain[0])
                     && self.currentViewedMediaList.includes(link_domain[1]) ){
                        // judge currMedium, show media which have relation with currMedium or keepMediaQueue.
                        if(self.currMedium == link_domain[0] || self.currMedium == link_domain[1]
                        || sysDatasetObj.keepMediaQueue.includes(link_domain[0]) || sysDatasetObj.keepMediaQueue.includes(link_domain[1])){
                            path.push(circlesLocation[link_domain[0].replaceAll('.','_')])
                            path.push(circlesLocation[link_domain[1].replaceAll('.','_')])
                            domainOneStep[keys[i]] = {location: path, value: domainLinks[keys[i]]}
                        }
                        else{
                            if(domains.includes(link_domain[0]) && domains.includes(link_domain[1])){
                                path.push(circlesLocation[link_domain[0].replaceAll('.','_')])
                                path.push(circlesLocation[link_domain[1].replaceAll('.','_')])
                                domainOneStep[keys[i]] = {location: path, value: domainLinks[keys[i]]}
                            }
                        }
                        
                    }
                }
            })
            console.log(domainOneStep);

            let mediagraphValues = Object.values(domainOneStep).map(ele=>ele.value);
            let edgeScale = d3.scaleLinear().domain(d3.extent(mediagraphValues)).range([4, 1]);
            // console.log(d3.max(mediagraphValues));

            Object.keys(domainOneStep).forEach(ele=>{
                let link_domain = ele.split("_");
                d3.select(this.$el).select(".media__contour__svg").select(".media-point-circle-g")
                    .select('#media_id_' + link_domain[0].replaceAll(".","_"))
                    .attr("fill-opacity", 1)
                    .classed("dot_mouseover", true)
                d3.select(this.$el).select(".media__contour__svg").select(".media-point-circle-g")
                    .select('#media_id_' + link_domain[1].replaceAll(".","_"))
                    .attr("fill-opacity", 1)
                    .classed("dot_mouseover", true)
                
                if(domains.includes(link_domain[0])){
                    d3.select(this.$el).select(".media__contour__svg").select(".media-point-circle-g")
                        .select('#media_id_' + link_domain[0].replaceAll(".","_"))
                        .classed("dot_mouseover", false)
                    d3.select(this.$el).select(".media__contour__svg").select(".media-point-circle-g")
                        .select('#media_id_' + link_domain[0].replaceAll(".","_"))
                        .classed("dot-keep-domain-hover", true)
                }
                if(domains.includes(link_domain[1])){
                    d3.select(this.$el).select(".media__contour__svg").select(".media-point-circle-g")
                        .select('#media_id_' + link_domain[1].replaceAll(".","_"))
                        .classed("dot_mouseover", false)
                    d3.select(this.$el).select(".media__contour__svg").select(".media-point-circle-g")
                        .select('#media_id_' + link_domain[1].replaceAll(".","_"))
                        .classed("dot-keep-domain-hover", true)
                }
            })

            // 补丁1：：将已选择的媒体高亮
            sysDatasetObj.mediaScatterSelected.forEach(ele=>{
                d3.select(this.$el).select(".media__contour__svg").select(".media-point-circle-g")
                    .select('#media_id_' + ele.replaceAll(".","_"))
                    .attr("fill-opacity", 1)
                    .classed("dot_mouseover", true)
                d3.select(this.$el).select(".media__contour__svg").select(".media-point-circle-g")
                    .select('#media_id_' + ele.replaceAll(".","_"))
                    .classed("dot_mouseover", false)
                d3.select(this.$el).select(".media__contour__svg").select(".media-point-circle-g")
                    .select('#media_id_' + ele.replaceAll(".","_"))
                    .classed("dot-keep-domain-hover", true)

            })


            self.lineGenerator = d3.line()
                .x(d => d[0])
                .y(d => d[1]);

            const t = d3.select(self.$el).select(".media__contour__svg").select(".media-point-graph-g").transition()
                .duration(300);
            
            self.graph_g
                .selectAll("path").remove()
            
            self.graph_g
                .selectAll("path")
                .data(Object.keys(domainOneStep),function(d, i) {
                    return i;})
                .join(
                    enter => enter.append("path")
                        .attr("class", "link")
                        .attr("d", d=>{
                            console.log(d.split("_"));
                            console.log("enter");
                            return self.lineGenerator(domainOneStep[d]['location']);
                        })
                        .attr('stroke-width', d=> edgeScale(domainOneStep[d]['value'] + 1))
                        ,
                    // update => update
                    //     .call(update => update.transition(t)
                    //         .attr("d", d=>{
                    //             console.log(d.split("_"));
                    //             console.log("update");
                    //             return self.lineGenerator(domainOneStep[d]['location']);
                    //         })
                    //         .attr('stroke-width', d=> edgeScale(domainOneStep[d]['value'] + 1))
                    //     ),
                    exit => exit
                        .remove()
                )

            // draw labels
            let doaminText = {}
            for (var key in domainOneStep) {
                let eles = key.split("_");
                doaminText[eles[0]] = domainOneStep[key]['location'][0]
                doaminText[eles[1]] = domainOneStep[key]['location'][1]
            }
            console.log(doaminText);

            // 补丁2：：将已选择的媒体名称显示
            sysDatasetObj.mediaScatterSelected.forEach(ele=>{
                if(self.currentViewedMediaList.includes(ele)){
                    doaminText[ele] = circlesLocation[ele.replaceAll(".", "_")]
                }
            })

            self.label_g
                .selectAll("text").remove()
            
            self.label_g
                .selectAll("text")
                .data(Object.keys(doaminText))
                .join(
                    enter => enter.append("text")
                        .attr("class", "text_label")
                        .attr("x", d=> doaminText[d][0])
                        .attr("y", d=> doaminText[d][1])
                        .attr("dy", "-0.75em")
                        .attr('text-anchor',"middle")
                        .attr("paint-order", "stroke")
                        .text(d=>d)
                        ,
                    // update => update
                    //     .call(update => update.transition(t)
                    //     .attr("x", d=> doaminText[d][0])
                    //     .attr("y", d=> doaminText[d][1])
                    //     .attr("dy", "-0.75em")
                    //     .attr('text-anchor',"middle")
                    //     .attr("paint-order", "stroke")
                    //     .text(d=>d)
                        // ),
                    exit => exit
                        .remove()
                )
        }
    },
}
</script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.media-scatter-container {
    width: 100%;
    height: 100%;
    .flow-node-menu{
        position: absolute;
        width: 50px;
        z-index:999;
        // height: 60px;      
        .el-button--mini {
            width: 100%;
        }
    }
}
</style>

<style>
.dot {
    fill: rgb(157, 157, 157);
    stroke: white;
    stroke-width: 0.4px;
}

.dot_mouseover {
    fill: #4682b4;
    stroke-width: 1px;
    stroke: white;
}
.dot_mouseover1 {
    fill: steelblue;
    stroke-width: 1px;
    stroke: white;
}

.media_horizon_chart_tooltip_div {
    border: 1px solid black;
    background-color: white;
}

.summary_container_title {
    text-align: center;
    display: block;
    font: sans-serif;
}

.close-icon {
    float: right;
    right: 12px;
}

.link{
    stroke: steelblue;
}

.text_label{
    counter-increment: none;
    font-size: 10px;
    fill: black;
    stroke: white;
    stroke-width: 1px;
}

.dot-search-hover{
    fill: #e34a33;
}

.dot-keep-domain-hover{
    fill: #e34a33;
}

.testcss{
    fill : #fddbc7;
    fill : #f4a582;
    fill : #4393c3;
    fill : #92c5de;
    fill : #d6604d;
    fill : #c73b3b;
    fill : #f06565;
}
</style>
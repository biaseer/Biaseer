<template>
    <div class="media-horizonchart-container" ref="mediahorizonchart">
    </div>
</template>
  
<script>

import { mapState, mapMutations } from 'vuex';
import { getTopic } from '../assets/data/topicList'

export default {
    name: 'MediaHorizonChart',
    props: {
        msg: String,
        topic_code: String,
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

        }
    },
    computed: {
        ...mapState([
            'currMedium',
        ]),
    },
    watch: {
        currMedium: function () {
            let self = this;
            self.gainMediaHorizonChartData(self.currMedium);
            self.renderMediaHorizonChart(self.width, self.height);
        },
    },
    mounted: function () {
        let self = this;
        self.width = self.$refs.mediahorizonchart.clientWidth;
        self.height = self.$refs.mediahorizonchart.clientHeight;
        console.log(self.currMedium);
        self.gainMediaHorizonChartData(self.currMedium);
        self.drawMediaHorizonChart(self.width, self.height);
        self.renderMediaHorizonChart(self.width, self.height);
    },
    methods: {
        gainMediaHorizonChartData(domain){
            let self = this;
            self.domain = domain;
            console.log(self.domain);
            self.tmpdata = sysDatasetObj.mediaDataSet['details'].filter(ele => ele['domain'] == self.domain)[0];
            self.data = Object.values(self.tmpdata['doctone']).flat();
            self.draw_data = Object.values(self.tmpdata['doctone']).map(function (item, id) {
                return {'key': id + 1, 'values': item};
            });
            console.log(self.draw_data);
        },
        drawMediaHorizonChart(width, height) {
            let self = this;
            //==================
            self.overlap = 2;
            
            self.margin = {top: 0, right: 0, bottom: 0, left: 0};
            self.innerWidth = width - self.margin.left - self.margin.right;
            self.innerHeight = height - self.margin.top - self.margin.bottom;

            self.step = (height - (self.margin.top + self.margin.bottom) ) /  self.draw_data.length - 1;
            let colorArr = ["#4393c3", "#92c5de", "#fddbc7", "#f4a582", "#d6604d", "#b2182b", "#67001f"];
            self.color = i => colorArr[i + (i >= 0) + self.overlap];
            // self.step = self.step * 1;
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
                // .curve(d3.curveStep)
                .curve(d3.curveBasis)
                .x(d => self.xScale(self.xValue(d)))
                .y0(d => 0)
                .y1(d => self.yScale(self.yValue(d)));
            
            self.svg = d3.select(self.$el)
                .append("svg")
                .attr("width", width)
                .attr("height", height)
                .attr("viewBox", [0, 0, width, height])
                .attr("style", "max-width: 100%; height: auto; font: 6px sans-serif;");
            
            // self.xg = self.svg.append("g")
            //     .call(self.xAxis);
            
            self.horizong = self.svg.append("g").attr("class", "horizon-graph");
            
        },
        renderMediaHorizonChart(width, height){
            let self = this;            
            
            self.horizong.selectAll('g').remove();

            self.clipPath = self.horizong.selectAll("g")
                .data(self.draw_data)
                .enter().append("g")
                    .attr("class", "horizon-graph-sub")
                    .attr("transform", (d, i) => `translate(0,${i * (self.step + 1) + self.margin.top})`)
            
            self.clipPath.append("clipPath")
                    .attr("id", (d,i)=>"area-clip-"+i)
                .append("rect")
                    .attr("width", width)
                    .attr("height", self.step);
            
            self.clipPath.append("defs").append("path")
                .attr("id", (d,i)=>{
                    d.path = {'id': "path-defs-"+i, 'href': '#path-defs-'+i}
                    return "path-defs-"+i;
                })
                .attr("d", d => self.areaGenerator(d.values));

            self.clipPath.append("g")
                    .attr("clip-path", (d,i) => "url(#area-clip-" + i + ")")
                .selectAll("use")
                .data(d => {
                    return Array.from(
                        {length: self.overlap * 2}, 
                        (_, i) => {
                            return Object.assign({index: i < self.overlap ? -i - 1 : i - self.overlap}, d)
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
        }
    }
}
</script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.media-horizonchart-container {
    width: 100%;
    height: 100%;
}
</style>

<style>
</style>
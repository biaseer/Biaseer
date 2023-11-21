<template>
    <div class="media-trend-container" ref="mediatrend">
    </div>
</template>
  
<script>

import { mapState, mapMutations } from 'vuex';

export default {
    name: 'MediaTrend',
    props: {
        msg: String,
        topic_code: String,
    },
    data() {
        return{
            xScale: null,
            xScale_1: null,
            yScale: null,
            xValue: null,
            yValue: null,
            yValue0: null,
            yValue1: null,
            xAxis: null,
            yAxis: null,
            xyg: null,
            clip: null,
            brush: null,
            svg: null,
            margin: null,
            innerHeight: null,
            innerWidth: null,
            lineg: null,
            updateg: null,
            lineGenerator: null,
            areaGenerator: null,
            all: null,
            actor1: null,
            actor2: null,
            keys: ["all"]
        }
    },
    computed: {
        ...mapState([
            'currMedium',
        ])
    },
    watch: {
        currMedium: function(){
            let self = this;
            self.renderFeatureTrending(self.currMedium, 'doctone', self.topic_code);
        }
    },
    mounted: function() {
        let self = this;
        self.width = self.$refs.mediatrend.clientWidth;
        self.height = self.$refs.mediatrend.clientHeight;
        console.log(self.currMedium);
        self.drawFeatureLine(self.width, self.height);
        self.renderFeatureTrending(self.currMedium, 'doctone', self.topic_code);
    },
    methods: {
        drawFeatureLine(width, height) {
            let self = this;
            // self.margin = { top: 10, right: 10, bottom: 35, left: 40 };
            self.margin = { top: 1, right: 10, bottom: 1, left: 10 };
            self.innerWidth = width - self.margin.left - self.margin.right;
            self.innerHeight = height - self.margin.top - self.margin.bottom;

            self.svg = d3.select(self.$el)
                .append("svg")
                .attr("width", width)
                .attr("height", height);
            
            self.xyg = self.svg.append('g')
                .attr('transform', `translate(${self.margin.left},${self.margin.top})`);
            
            self.xScale = d3.scaleTime().range([0, self.innerWidth]);
            self.xAxis = d3.axisBottom(self.xScale);//.ticks(5);
            self.xyg.append("g")
                .attr('transform', `translate(${0},${self.innerHeight})`)
                .attr("class","myXaxis");
            
            self.yScale = d3.scaleLinear().range([self.innerHeight, 0]);
            self.yAxis = d3.axisLeft(self.yScale).ticks(5);
            self.xyg.append("g")
                .attr("class","myYaxis");
            
            // Add a clipPath: everything out of this area won't be drawn.
            self.clip = self.xyg.append("defs").append("svg:clipPath")
                .attr("id", "clip")
                .append("svg:rect")
                .attr("width", self.innerWidth)
                .attr("height", self.innerHeight)
                .attr("x", 0)
                .attr("y", 0);
            
            self.brush = d3.brushX()
                .extent([[0, 0], [self.innerWidth, self.innerHeight]]);
            
            self.lineg = self.xyg.append('g')
                .attr("clip-path", "url(#clip)")
                .attr("class", "brush")
                .attr("cursor", "pointer")
                .attr("width", self.innerWidth)
                .attr("height", self.innerHeight)
                .attr("x", 0)
                .attr("y", 0);
            
            self.xValue = d => new Date(d.date);
            self.yValue = d => d.value + d.value1;

            self.yValue0 = d => d.value1;
            self.yValue1 = d => d.value;

            self.lineGenerator = d3.line()
                .x(d => self.xScale(self.xValue(d)))
                .y(d => self.yScale(self.yValue(d)));
            
            self.areaGenerator = d3.area()
                .x(d => self.xScale(self.xValue(d)))
                .y0(d => self.yScale(self.yValue0(d)))
                .y1(d => self.yScale(self.yValue1(d)))
        },
        renderFeatureTrending(medium, doctone, topic){
            let self = this;
            let tmpdata = sysDatasetObj.mediaDataSet['details'].filter(ele=>ele['domain'] == medium)[0];

            let draw_data = tmpdata[doctone][topic];
            
            let toneValue = d => d.value;
            let toneMinMax = d3.extent(draw_data, toneValue);
            let min_extent = -15;//toneMinMax[0];
            let max_extent = 10;//toneMinMax[1];

            // let min_extent = toneMinMax[0];
            // let max_extent = toneMinMax[1];

            self.xScale.domain(d3.extent(draw_data, self.xValue));

            // self.xyg.selectAll(".myXaxis").transition()
            //     .duration(750)
            //     .call(self.xAxis);
            // self.xyg.selectAll(".myXaxis").select('.domain').attr("stroke-width", 0.5);
            // self.xyg.selectAll(".myXaxis")
            //     .selectAll("text")
            //     // .attr("transform", "translate(-0,0)rotate(-30)")
            //     // .style("text-anchor", "end");
            //     .style("text-anchor", "middle");

            self.yScale.domain([min_extent, max_extent]);

            // self.xyg.selectAll(".myYaxis").transition()
            //     .duration(750)
            //     .call(self.yAxis);
            
            // self.xyg.selectAll(".myYaxis").select('.domain').attr("stroke-width", 0.5);
            // self.xyg.selectAll(".myYaxis").select('.feature_trending_title').remove();
            // self.xyg.selectAll(".myYaxis").append('text')
            //     .attr("transform", "translate(-0,0)rotate(-90)")
            //     .attr('class', 'feature_trending_title')
            //     .attr('y', -self.margin.left / 1.5)
            //     .attr('x', -self.innerHeight / 2)
            //     .attr('fill', '#606266')
            //     .attr('font-size', '1.3em')
            //     .style('text-anchor', 'middle')
            //     .text(medium);
            
            const t = self.lineg.transition()
                .duration(750);
            self.lineg.selectAll("path")
                .data([draw_data])
                .join(
                    enter => enter.append("path")
                            .attr("class", "feature_trending")
                            .attr("d", d=>self.areaGenerator(d))
                        ,
                    update => update.call(
                            update => update.transition(t)
                            .attr("d", d =>self.areaGenerator(d))
                        ),
                    exit => exit
                            .remove()
                );
        },
    }
}
</script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.media-trend-container {
    width: 100%;
    height: 5%;
}
</style>

<style>
.feature_trending{
    fill: #69b3a2;
    /* stroke: steelblue; */
}
</style>
<template>
    <div class="MediaConcat" style="display: flex; justify-content: space-between;">
        <div class="mediatags" style="order:1;">
            <div class="concat_text">
                <span>
                    SELECTED MEDIA:
                </span>
            </div>
            <el-tag size="medium" :key="tag" v-for="tag in dynamicTags" closable :disable-transitions="false"
                @close="handleClose(tag)">
                {{ tag }}
            </el-tag>
        </div>
        <div class="concatswitch" style="order:2;">
            <el-switch v-model="isConcated" active-text="concat" @change="changeConcatStatus" class="concat-switch">
            </el-switch>
        </div>
    </div>
</template>
  
<script>
// Structors
import { mapState, mapMutations } from 'vuex';

export default {
    name: 'MediaTags',
    data() {
        return {
            dynamicTags: ['msn.com'],
            isConcated: true
        }
    },
    components: {
    },
    beforeMount: function () {
    },
    mounted() {
        this.dynamicTags = sysDatasetObj.mediaScatterSelected;
        this.changeConcatStatus()
    },
    methods: {
        ...mapMutations([
            'UPDATE_MEDIA_DIFF_CONCAT_SIGNAL',
            'UPDATE_MEDIA_SCATTER_CLICK',
            'UPDATE_CONCAT_STATUS'
        ]),
        /************* v-model, update the concat state *************/
        changeConcatStatus(){
            this.UPDATE_CONCAT_STATUS(this.isConcated);
            // check the concat is or is not opened, if true to compute concat diff
            if(this.isConcated){
                this.gainConcatDiff();
            }
        },
        /************* when delete a media tag *************/
        handleClose(tag) {
            this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1);
            // check the concat is or is not opened, if true to compute concat diff
            if(this.isConcated){
                this.gainConcatDiff();
            }
        },
        /************* change the concat diff signal *************/
        gainConcatDiff() {
            let self = this;
            self.UPDATE_MEDIA_DIFF_CONCAT_SIGNAL();
            // self.UPDATE_MEDIA_SCATTER_CLICK();
            sysDatasetObj.mediaScatterSelected = self.dynamicTags;
        }
    },
    computed: {
        ...mapState([
            'mediaScatterClick'
        ])
    },
    watch: {
        /************* listening the adding-media action *************/
        mediaScatterClick: function () {
            this.dynamicTags = sysDatasetObj.mediaScatterSelected;
            // check the concat is or is not opened, if true to compute concat diff
            if(this.isConcated){
                this.gainConcatDiff();
            }
        }
    }
}
</script>
  
<style lang="less" scoped>
.concat_text {
    margin-right: 10px;
    text-align: center;
    font-weight: bold;
    margin-top: 2.5px;
}
.MediaConcat {
    width: 100%;
    padding: 10px;
}
.mediatags {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    .switch-div{
        width: 20px;
    }
    .tags-div{
        flex: 1;
    }
}
.concat-switch{
    margin-left: 5px;
    margin-right: 5px;
    // background-color: lightgray;
}
.el-tag {
    height: 20px;
    padding: 0 3px;
    line-height: 20px;
    margin-right: 5px;
    background-color: #4d4d4d;
    border-color: #4d4d4d;
    color: white;
}
</style>

<style>
.el-switch__core {
 width: 30px !important;
 height: 16px !important;
 border-color: #4d4d4d !important;
 background-color: #4d4d4d !important;
}
.el-tag .el-tag__close {
    color: white !important;
}
.el-switch__core::after {
 width: 12px !important;
 height: 12px !important;
 top: 1px !important;
}
.el-switch.is-checked .el-switch__core::after{
 margin-left: -13px !important;
}
.el-switch__label--right {
    margin-left: 2px !important;
}
.el-switch__label * {
    line-height: 1.5 !important;
    font-size: 12px !important;
    display: inline-block !important;
    color: #4d4d4d !important;
    font-weight: bold;
}
</style>
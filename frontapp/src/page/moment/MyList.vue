<template>
  <div>
    <head-top :head="head">
      <img slot="left" src="../../images/icon-return.png" @click="goBack"/>
    </head-top>
    <div class="contentBox" v-cloak>
      <dynamic-list ref="dynamic" height="-42" :dynamicList="dynamicList" @on-refresh="onRefresh" @on-loadMore="onLoadMore"></dynamic-list>
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
  import HeadTop from '@/components/Head.vue'
  import DynamicList from './DynamicList.vue'
  import { momentDynamicList } from '../../service/getData.js'
  import nativeCommon from '../../config/nativeCommon.js'
  import { initializeEnv, exitCurApp } from '@/components/framework/serviceMgr.js'
  import { hasActionBar } from '@/components/framework/activityMgr.js'

  export default {
    components: {
      HeadTop,
      DynamicList
    },
    data () {
      return {
        head:{
          icon: 'return',
          title: '个人风采',
          more: false
        },
        last_id: '',
        rows: '10',
        dynamicList: []
      }
    },
    created () {
      initializeEnv(this);
      this.backNative = new nativeCommon();
      this.momentDynamicList();
    },
    methods: {
      //返回
      goBack () {
        if(hasActionBar(this)) {
          this.$router.back();
        } else {
          exitCurApp(this);
        }
      },
      //上拉加载
      onLoadMore () {
        this.momentDynamicList();
      },
      //下拉刷新
      onRefresh () {
        this.last_id = '';
        this.dynamicList = [];
        this.momentDynamicList();
      },
      //获取圈子动态列表
      async momentDynamicList () {
        this.$vux.loading.show({
          text: '加载中'
        });
        let res = await momentDynamicList('3', '', this.last_id, this.rows, '', '', '');
        this.$vux.loading.hide();
        if (res.c == 0) {
          if (res.d.list.length > 0) {
            this.last_id = res.d.list[res.d.list.length-1].moment_id;
          }
          this.dynamicList = this.dynamicList.concat(res.d.list);

          //上拉下拉完成
          this.$nextTick(() => {
            this.$refs.dynamic.$refs.scroller.reset();
          });
          this.$refs.dynamic.$refs.scroller.donePullup();
          this.$refs.dynamic.$refs.scroller.donePulldown();
          //上拉加载启用禁用
          if(res.d.list.length < this.rows){
            this.$refs.dynamic.$refs.scroller.disablePullup();
          } else {
            this.$refs.dynamic.$refs.scroller.enablePullup();
          }
        } else {
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          })
        }
      }
    }
  }
</script>

<style scoped>

</style>

<template>
  <div>
    <head-top :head="head">
      <img slot="left" src="../../images/icon-return.png" @click="goBack"/>
    </head-top>
    <div class="contentBox" v-cloak>
      <div class="toolbar boxShadowGray">
        <div class="toolbar-title left">{{ clazz.class_name }} 风采</div>
        <div class="toolbar-filter right" @click="showFilterBox=true">筛选</div>
      </div>
      <dynamic-list ref="dynamic" :clazz="clazz" height="-142" :dynamicList="dynamicList" @on-refresh="onRefresh" @on-loadMore="onLoadMore"></dynamic-list>
      <publish-btn :clazz="clazz"></publish-btn>

      <!--筛选弹窗-->
      <x-dialog v-model="showFilterBox" :dialog-style="{'max-width': '100%', width: '17.25rem', 'margin-top': '1.5rem'}" hide-on-blur @on-hide="onRefresh">
        <div class="filter-box">
          <div>时间筛选</div>
          <ul class="filter-box-time">
            <li :class="{active: time_scope==0}" @click="time_scope='0'">全部</li>
            <li :class="{active: time_scope==1}" @click="time_scope='1'">今日</li>
            <li :class="{active: time_scope==2}" @click="time_scope='2'">本周</li>
            <li :class="{active: time_scope==3}" @click="time_scope='3'">本月</li>
            <li :class="{active: time_scope==6}" @click="time_scope='6'">本学期</li>
          </ul>
          <div>发起人</div>
          <input class="filter-box-input" type="text" placeholder="输入发起人姓名" v-model="keyword">
          <div>类型</div>
          <table width="100%" align="center">
            <tr>
              <td><div class="item-icon icon-moment" :class="{active: moment_type=='0,1,2,3'}" @click="moment_type='0,1,2,3'"></div></td>
              <td><div class="item-icon icon-dayoff" :class="{active: moment_type=='5'}" @click="moment_type='5'"></div></td>
              <td><div class="item-icon icon-evaluate" :class="{active: moment_type=='6'}" @click="moment_type='6'"></div></td>
            </tr>
            <tr>
              <td>风采</td>
              <td>请假</td>
              <td>评价</td>
            </tr>
          </table>
          <div class="filter-box-reset" @click="filterReset">重置</div>
        </div>
      </x-dialog>
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
  import Vue from 'vue'
  import HeadTop from '@/components/Head.vue'
  import DynamicList from './DynamicList.vue'
  import PublishBtn from './PublishBtn.vue'
  import { ConfigPlugin, XDialog } from 'vux'
  import { momentDynamicList } from '../../service/getData.js'

  //弹窗后阻止body内容滚动
  Vue.use(ConfigPlugin, {
    $layout: 'VIEW_BOX'
  });

  export default {
    components: {
      HeadTop,
      DynamicList,
      PublishBtn,
      XDialog
    },
    data () {
      return {
        head:{
          icon: 'return',
          title: '班级风采',
          more: false
        },
        clazz: this.$route.query.clazz,
        last_id: '',
        rows: '10',
        dynamicList: [],
        showFilterBox: false,
        time_scope: '0', //时间范围：0全部，1今日，2本周，3本月，6本学期
        keyword: '', //搜索关键字
        moment_type: '' //动态类型, 多个用逗号分隔, 空表示查询全部, '0'照片，'1'视频，'2'附件，'3'投票，'4'奖章，'5'请假，'6'评价
      }
    },
    created () {
      this.momentDynamicList();
    },
    methods: {
      //返回
      goBack () {
        this.$router.replace({
          name: 'momentList',
          query: {
            circle_type: 2
          }
        });
      },
      //筛选重置
      filterReset () {
        this.time_scope = '0';
        this.keyword = '';
        this.moment_type = '';
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
        let res = await momentDynamicList('2', this.clazz.class_id, this.last_id, this.rows, this.time_scope, this.keyword, this.moment_type);
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
  .toolbar {
    margin: 1.5rem 0.75rem 1rem;
    border-radius: 50px;
    overflow: hidden;
  }
  .toolbar-title {
    margin-left: 1rem;
    height: 2.5rem;
    line-height: 2.5rem;
    font-size: 0.75rem;
    font-weight: bold;
    color: #444;
  }
  .toolbar-filter {
    margin: 0.25rem;
    width: 2rem;
    height: 2rem;
    text-align: center;
    line-height: 2rem;
    font-size: 0.6rem;
    font-weight: bold;
    color: #fff;
    background-color: #ff9e35;
    border-radius: 50%;
  }
  .vux-popup-dialog {
    background: transparent;
  }
  .filter-box {
    padding: 1rem;
    text-align: center;
    font-size: 0.75rem;
    background: #fff;
    border-radius: 4px;
  }
  .filter-box-time {
    margin: 1.5rem 0;
    overflow: hidden;
  }
  .filter-box-time li {
    float: left;
    margin-right: 0.5rem;
    width: 2.5rem;
    height: 1.5rem;
    text-align: center;
    line-height: 1.5rem;
  }
  .filter-box-time li.active {
    color: #fff;
    background-color: #4685ff;
    border-radius: 4px;
  }
  .filter-box-input {
    margin: 1rem 0 1.5rem;
    width: 100%;
    height: 1.5rem;
    line-height: 1.5rem;
    border-bottom: 2px solid #dcdcdc;
    border-radius: 0;
  }
  ::-webkit-input-placeholder { /* WebKit, Blink, Edge */
    color: #aaa;
  }
  :-moz-placeholder { /* Mozilla Firefox 4 to 18 */
    color: #aaa;
  }
  ::-moz-placeholder { /* Mozilla Firefox 19+ */
    color: #aaa;
  }
  :-ms-input-placeholder { /* Internet Explorer 10-11 */
    color: #aaa;
  }
  .item-icon {
    margin: 1rem auto 0.5rem;
    width: 2.5rem;
    height: 2.5rem;
    border: solid 4px #eee;
    border-radius: 50%;
  }
  .icon-moment {
    background: #fff url('../../images/icon-moment.png') no-repeat center / 50%;
  }
  .icon-dayoff {
    background: #fff url('../../images/icon-dayoff.png') no-repeat center / 50%;
  }
  .icon-evaluate {
    background: #fff url('../../images/icon-evaluate.png') no-repeat center / 50%;
  }
  .icon-moment.active {
    border-color: #f16f6f;
  }
  .icon-dayoff.active {
    border-color: #4685ff;
  }
  .icon-evaluate.active {
    border-color: #f8b62d;
  }
  .filter-box-reset {
    margin-top: 2rem;
    color: #4685ff;
  }
</style>

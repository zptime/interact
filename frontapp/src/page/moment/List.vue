<template>
  <div>
    <head-top :head="head">
      <img slot="left" src="../../images/icon-return.png" @click="goBack"/>
    </head-top>
    <div class="contentBox" v-cloak>
      <tab v-model="circle_type" :line-width="4" custom-bar-width="60px" default-color="#444" active-color="#444" bar-active-color="#4685ff">
        <tab-item>最新风采</tab-item>
        <tab-item>学校风采</tab-item>
        <tab-item>班级风采</tab-item>
      </tab>
      <div>
        <!--最新风采、学校风采-->
        <div v-show="circle_type==0 || circle_type==1">
          <dynamic-list ref="dynamic" :circleType="circle_type" :dynamicList="dynamicList" @on-refresh="onRefresh" @on-loadMore="onLoadMore"></dynamic-list>
        </div>
        <!--班级列表-->
        <div class="clazz-list" v-if="circle_type==2">
          <!--教师-->
          <div v-if="userInfo.user_type_id==2">
            <div class="classify-title">我的班级</div>
            <div class="classify-clazz" v-for="clazz in classList" v-if="clazz.is_mentor==1" @click="goClassList(clazz)">
              <img class="left" src="../../images/icon-default-cluster.png" alt="群组">
              <div class="left">
                <div class="clazz-name">{{ clazz.class_name }}</div>
                <div class="clazz-info">教师{{ clazz.teacher_count }}人 学生{{ clazz.student_count }}人</div>
              </div>
              <div class="clazz-mentor right" v-if="clazz.mentors.length>0">班主任-{{ clazz.mentors[0].username }}</div>
            </div>
            <div class="classify-title">我的任教班级</div>
            <div class="classify-clazz" v-for="clazz in classList" v-if="clazz.is_mentor==0" @click="goClassList(clazz)">
              <img class="left" src="../../images/icon-default-cluster.png" alt="群组">
              <div class="left">
                <div class="clazz-name">{{ clazz.class_name }}</div>
                <div class="clazz-info">教师{{ clazz.teacher_count }}人 学生{{ clazz.student_count }}人</div>
              </div>
              <div class="clazz-mentor right" v-if="clazz.mentors.length>0">班主任-{{ clazz.mentors[0].username }}</div>
            </div>
          </div>
          <!--家长-->
          <div v-if="userInfo.user_type_id==4">
            <div class="classify-title">孩子班级</div>
            <div class="classify-clazz" v-for="clazz in classList" @click="goClassList(clazz)">
              <img class="left" src="../../images/icon-default-cluster.png" alt="群组">
              <div class="left">
                <div class="clazz-name">{{ clazz.class_name }}</div>
                <div class="clazz-info">教师{{ clazz.teacher_count }}人 学生{{ clazz.student_count }}人</div>
              </div>
              <div class="clazz-mentor right" v-if="clazz.mentors.length>0">班主任-{{ clazz.mentors[0].username }}</div>
            </div>
          </div>
        </div>
      </div>
      <publish-btn :circleType="circle_type"></publish-btn>
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
  import HeadTop from '@/components/Head.vue'
  import DynamicList from './DynamicList.vue'
  import PublishBtn from './PublishBtn.vue'
  import { Tab, TabItem } from 'vux'
  import { momentDynamicList, getUserInfo, getClassList } from '../../service/getData.js'
  import nativeCommon from '../../config/nativeCommon.js'
  import {initializeEnv, exitCurApp} from '../../components/framework/serviceMgr'

  export default {
    components: {
      HeadTop,
      DynamicList,
      PublishBtn,
      Tab,
      TabItem
    },
    data () {
      return {
        head:{
          icon: 'return',
          title: '风采',
          more: false
        },
        circle_type: this.$route.query.circle_type ? Number(this.$route.query.circle_type) : 0, //导航（圈子类型）
        last_id: '',
        rows: '10',
        dynamicList: [],
        userInfo: {},
        classList: {}
      }
    },
    watch: {
      circle_type: function () {
        if (this.circle_type==0 || this.circle_type==1) {
          this.$nextTick(() => {
            this.$refs.dynamic.$refs.scroller.reset({top: 0});
            this.$refs.dynamic.$refs.scroller.disablePullup();
          });
        }

        this.init();
      }
    },
    created () {
      initializeEnv(this);
      this.backNative = new nativeCommon();
      this.init();
    },
    methods: {
      //返回
      goBack () {
        exitCurApp(this);
      },
      //初始化
      init () {
        if (this.circle_type==0 || this.circle_type==1) {
          //最新风采、学校风采
          this.onRefresh();
        } else {
          //班级列表
          this.getUserInfo();
          this.getClassList();
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
      //跳转班级风采列表页
      goClassList (clazz) {
        this.$router.replace({
          name: 'momentClassList',
          query: {
            clazz: clazz
          }
        });
      },
      //获取圈子动态列表
      async momentDynamicList () {
        this.$vux.loading.show({
          text: '加载中'
        });
        let res = await momentDynamicList(this.circle_type, '', this.last_id, this.rows, '', '', '');
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
      },
      //获取用户基本信息
      async getUserInfo () {
        let res = await getUserInfo('','','');
        if (res.c == 0) {
          this.userInfo = res.d;
        } else {
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          })
        }
      },
      //获取本人所关联班级
      async getClassList () {
        let res = await getClassList();
        if (res.c == 0) {
          this.classList = res.d;
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
  .clazz-list {
    position: fixed;
    width: 100%;
    padding: 0 0.75rem;
    overflow: scroll;
    top: 4.3rem;
    bottom: 0;
  }
  .classify-title {
    line-height: 1.75rem;
    font-size: 0.7rem;
    color: #888;
  }
  .classify-clazz {
    overflow: hidden;
    border-top: 1px solid #eee;
  }
  .classify-clazz img {
    margin: 0.25rem 0.25rem 0.25rem 0;
    width: 3rem;
  }
  .clazz-name {
    margin-top: 0.5rem;
    line-height: 1.35rem;
    font-size: 0.85rem;
    color: #111;
  }
  .clazz-info {
    font-size: 0.65rem;
    color: #666;
  }
  .clazz-mentor {
    margin-top: 0.5rem;
    line-height: 1.4rem;
    font-size: 0.55rem;
    color: #aaa;
  }
</style>

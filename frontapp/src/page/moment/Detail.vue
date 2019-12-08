<template>
  <div>
    <head-top :head="head">
      <img slot="left" src="../../images/icon-return.png" @click="goBack"/>
    </head-top>
    <div class="contentBox" v-cloak>
      <dynamic-list :isDetail="true" height="-42" :dynamicList="dynamicList" @on-refresh="momentDynamicDetail"></dynamic-list>
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
  import HeadTop from '@/components/Head.vue'
  import DynamicList from './DynamicList.vue'
  import { momentDynamicDetail, momentDynamicRead } from '../../service/getData.js'

  export default {
    components: {
      HeadTop,
      DynamicList
    },
    data () {
      return {
        head:{
          icon: 'return',
          title: '风采详情',
          more: false
        },
        moment_id: this.$route.query.moment_id,
        dynamicList: []
      }
    },
    created () {
      this.momentDynamicDetail();
    },
    methods: {
      //返回
      goBack () {
        if (this.$route.query.circle_type != undefined) {
          this.$router.replace({
            name: 'momentList',
            query: {
              circle_type: this.$route.query.circle_type
            }
          });
        } else if (this.$route.query.clazz != undefined) {
          this.$router.replace({
            name: 'momentClassList',
            query: {
              clazz: this.$route.query.clazz
            }
          });
        } else {
          this.$router.replace({
            name: 'momentMyList'
          });
        }
      },
      //获取圈子动态详情
      async momentDynamicDetail () {
        momentDynamicRead(this.moment_id);
        let res = await momentDynamicDetail(this.moment_id);
        if (res.c == 0) {
          this.dynamicList = [];
          this.dynamicList.push(res.d);
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

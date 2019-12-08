<template>
  <div class="phone">
    <head-top :head="head">
      <img slot="left" src="../../images/icon-return.png" @click="goBack"/>
    </head-top>
    <div class="contentBox" v-cloak>
      <div class="content">
        <div class="title">请给您的小组起个名字</div>
        <div class="tip">每个小组至少2个人</div>
        <div class="num">{{ change() }} / 10</div>
        <div class="name">
          <x-input :max="10" @on-change="change" v-model="groupName" :show-clear="false"></x-input>
        </div>
        <!--<div class="node boxShadowBlue" @click="goChoose">下一步</div>-->
        <div class="node-step step-common" @click="goChoose">
          <span class="step-common">
            <img class="step-common" src="../../images/icon-step.png">
          </span>
          <span class="next-step step-common">下一步</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script type="es6">
  import HeadTop from '@/components/Head.vue'
  import XInput from 'vux/src/components/x-input/index.vue'
  import { getClassList } from '../../service/getData'
  import { mapMutations } from 'vuex'
  export default {
    data(){
      return {
        head:{
          icon: 'return',
          title: '创建小组',
          more: false
        },
        groupName:'',//小组名称
        classIds:'',
      }
    },
    components: {
      HeadTop,
      XInput,
    },
    methods:{
      ...mapMutations([
        'NAV_FLAG',
      ]),

      goBack(){
        this.NAV_FLAG(2);
        this.$router.back();
      },

      async getItems(){
        let res = await getClassList();
        if(res.c==0){
          this.classIds = '';
          for(let i=0;i<res.d.length;i++){
            this.classIds += res.d[i].class_id+',';
          }
          this.classIds = this.classIds.slice(0,this.classIds.length-1);
        }else{
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          });
        }
      },

      //输入值变化事件
      change(){
        return this.groupName.length;
      },

      //进入选择人员界面
      goChoose(){
        if(this.groupName.length>0){
          this.$router.push({
            name:'choosePerson',
            query:{
              gName:this.groupName
            }
          });
        }else{
          this.$vux.toast.show({
            type: 'text',
            text: '请输入小组名称'
          });
        }
      }
    }
  }
</script>

<style scoped>
  .content{
    padding:0 0.75rem;
    width:100%;
    overflow: hidden;
  }
  .title{
    font-size: 1.2rem;
    color:#444;
    margin:4rem auto 1rem auto;
  }
  .tip{
    font-size: 0.6rem;
    color:#aaa;
  }
  .num{
    color:#444;
    font-size: 0.6rem;
    text-align: right;
    margin:3.2rem 0.5rem 1rem 0;
  }
  .name{
    border-bottom: 2px solid #eee;
    margin-bottom:4rem;
  }
  .node{
    width: 5rem;
    height:5rem;
    border-radius: 2.5rem;
    color:#fff;
    font-size: 0.75rem;
    margin:0 auto;
    text-align: center;
    display:flex;/*Flex布局*/
    display: -webkit-flex; /* Safari */
    justify-content: center;/*实现水平居中*/
    align-items:center; /*实现垂直居中*/
    background: -webkit-linear-gradient(left, #70a8f9 , #4685ff); /* Safari 5.1 - 6.0 */
    background: -o-linear-gradient(right, #70a8f9, #4685ff); /* Opera 11.1 - 12.0 */
    background: -moz-linear-gradient(right, #70a8f9, #4685ff); /* Firefox 3.6 - 15 */
    background: linear-gradient(to right, #70a8f9 , #4685ff); /* 标准的语法 */
  }
  .step-common{
    width: 6.4rem;
    height:6.4rem;
    border-radius: 3.2rem;
  }
  .node-step{
    margin:0 auto;
    position: relative;
  }
  .node-step span{
    display: inline-block;
    float: left;
    line-height: 6.4rem;
  }
  .node-step img{
    width: 6.4rem;
    height:6.4rem;
  }
  .node-step .next-step{
    position: absolute;
    color:#fff;
    font-size: 0.75rem;
    left:0;
  }
</style>

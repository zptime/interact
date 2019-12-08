<template>
  <div class="head" v-if="show">
    <span class="h-col h-left oper">
        <slot name="left">
          <img v-if="head.icon=='return'" src="../images/icon-return.png" @click="go_back()"/>
          <img v-if="head.icon=='close'" src="../images/icon-close.png" @click="do_close()"/>
        </slot>
    </span>
    <span class="h-col h-center title">
        <slot name="middle">
            {{head.title}}
        </slot>
    </span>
    <span class="h-col h-right more color-blue" v-if="head.more">
        <slot name="right">
          <img src="../images/icon-more.png" @click="go_moreChoice()"/>
        </slot>
    </span>
  </div>
</template>

<script type="es6">
  import Global from '../components/Global.vue'
  import { hasActionBar } from '../components/framework/activityMgr.js'
  export default {
    props: ["head"],
    data () {
      return {
        icon: 'return',
        title: '办公OA',
        more: true,
        goBackUrl:'',
        show:'',//是否显示头部-微信中不显示
      }
    },
    created(){
      //console.log('Global-showHead-init....'+Global.showHead);
      //console.log('hasActionBar-is-weixin....'+hasActionBar(this));
      //Global.setHeadVal(!hasActionBar(this));
      //console.log('Global-showHead-change....'+Global.showHead);
      this.show = Global.showHead;
    },
    methods: {
      go_back() {
        if(this.head.goBackUrl && this.head.goBackUrl.length > 0) {
          this.$router.push({
            path: this.head.goBackUrl,
          });
        }else{
          this.$router.back();
        }
      },

      do_close() {
        finishActivity();
      },

      go_moreChoice (){
        this.$router.push('moreChoice');
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style type="text/css" scoped>
  .head{
    position: fixed;
    width: 100%;
    height: 2.1rem;
    left: 0;
    background-color: #fff;
    z-index: 99;
  }
  .head .h-col{
    height: 100%;
    position: relative;
    display: inline-block;
    vertical-align: middle;
  }
  .head .h-left{
    position: absolute;
    left: 0;
  }
  .head .h-center{
    position: absolute;
    left: 50%;
    transform: translate(-50%,0);
  }
  .head .h-right{
    position: absolute;
    right: 0;
  }
  .head .oper{
    line-height: 2.1rem;
    padding-left: 0.6rem;
  }
  .head .oper img{
    width: 20px;
    height: 20px;
    padding: 10px;
    position: absolute;
    top: 50%;
    transform: translate(-10px, -50%);
  }
  .head .title{
    font-size: 0.8rem;
    color: #030303;
    line-height: 2.1rem;
    white-space: nowrap;  /*强制span不换行*/
    display: inline-block;  /*将span当做块级元素对待*/
    width: 60%;  /*限制宽度*/
    overflow: hidden;  /*超出宽度部分隐藏*/
    text-overflow: ellipsis;  /*超出部分以点号代替*/
    text-align: center;
  }
  .head span{
      color:#4685ff;
      font-size:0.7rem;
      line-height:2.1rem;
  }
  .head .more{
    height: 2.1rem;
    padding-right: 0.6rem;
      line-height: 2.1rem;
      font-size:0.7rem;
  }

  .head .more img{
    width: 20px;
    height: 20px;
    padding: 10px;
    position: relative;
    top: 50%;
    transform: translate(10px, -50%);
  }
</style>

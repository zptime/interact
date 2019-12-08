<template>
  <div>
    <head-top :head="head"></head-top>
    <div style="padding: 3.6rem 0.75rem 0;">
       <div class="switch-items">
           <div class="item boxShadowGray borderRadius">
               <div class="img-box boxShadowGray"><img src="" alt=""></div>
               <div class="item-msg">
                   <div class="item-name">呵呵呵  (xxx父亲)</div>
                   <div class="item-school">光谷一小 · 00213214</div>
                   <div class="item-select"></div>
               </div>
           </div>
           <div class="item boxShadowGray borderRadius">
               <div class="img-box boxShadowGray"><img src="" alt=""></div>
               <div class="item-msg">
                   <div class="item-name">呵呵呵  (xxx父亲)</div>
                   <div class="item-school">光谷一小 · 00213214</div>
                   <div class="item-select"></div>
               </div>
           </div>
           <div class="item boxShadowGray borderRadius">
               <div class="img-box boxShadowGray"><img src="" alt=""></div>
               <div class="item-msg">
                   <div class="item-name">呵呵呵  (xxx父亲)</div>
                   <div class="item-school">光谷一小 · 00213214</div>
                   <div class="item-select"></div>
               </div>
           </div>
       </div>
       <div class="bottomButton boxShadowBlue">+ 添加角色</div>
    </div>
  </div>
</template>

<script type="es6">
  import HeadTop from '@/components/Head.vue'
  import { TransferDomDirective as TransferDom  } from 'vux'
  export default {
    directives: {
        TransferDom
    },
    data () {
      return {
        head:{
          icon: 'return',
          title: '互动系统-个人中心',
          more: false
        },
      }
   },
   methods:{

   },
    components: {
      HeadTop,
    },
  }

</script>

<style scoped>
.switch-items{margin-top: 1.5rem;}
.switch-items .item{padding: 0.75rem;height: 2.5rem;box-sizing: content-box;position: relative;margin-bottom: 0.75rem;}
.switch-items .item .img-box{width: 2.5rem;height: 2.5rem;position: absolute;left: 0.75rem;top: 0.75rem;border-radius: 50%;}
.switch-items .item .item-msg{margin-left: 3rem;height: 100%;}
.switch-items .item .item-msg .item-name{font-size: 0.75rem;color: #444444;margin-top: 0.2rem;}
.switch-items .item .item-msg .item-school{font-size: 0.6rem;color: #888;margin-top: 0.3rem;}
.switch-items .item .item-msg .item-select{position: absolute;right: 0;top:50%;transform: translateY(-50%)}
.bottomButton{  width:7.5rem;  margin:2.5rem auto;height: 2rem;  line-height: 2rem;  text-align: center;  background-color: #4685ff;  color:#fff;  font-size: 0.75rem;  -webkit-border-radius: 1rem;  -moz-border-radius: 1rem;  -ms-border-radius: 1rem;  -o-border-radius: 1rem;  border-radius: 1rem;}
</style>

<template>
  <div>
    <head-top :head="head"></head-top>
    <div style="padding: 3.6rem 0.75rem 0;">
        <div class="add-btn" @click="go_invite()">邀请家庭成员</div>
        <div class="f-items">
            <div class="item boxShadowGray">
                <div class="item-imgbox"><img src="" alt=""></div>
                <div class="item-name">尚先生 - 先生</div>
                <div class="item-write"></div>
                <div class="item-out"></div>
            </div>
            <div class="item boxShadowGray">
                <div class="item-imgbox"><img src="" alt=""></div>
                <div class="item-name">尚先生 - 先生</div>
                <div class="item-write"></div>
                <div class="item-out"></div>
            </div>
            <div class="item boxShadowGray">
                <div class="item-imgbox"><img src="" alt=""></div>
                <div class="item-name">尚先生 - 先生</div>
                <div class="item-write"></div>
                <div class="item-out"></div>
            </div>
            <div class="item boxShadowGray">
                <div class="item-imgbox"><img src="" alt=""></div>
                <div class="item-name">尚先生 - 先生</div>
                <div class="item-write"></div>
                <div class="item-out"></div>
            </div>
        </div>
        <div class="bottomButton boxShadowBlue">+ 添加孩子</div>
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
        go_invite(){
            this.$router.push('/m/personal/parent/invite')
        }
   },
    components: {
      HeadTop,
    },
  }

</script>

<style scoped>
.add-btn{height: 2rem;border-radius: 1rem;text-align: center;line-height: 2rem;border: solid 1px #4685ff;color: #4685ff;font-size: 0.75rem;}
.f-items{margin-top: 1.5rem;}
.f-items .item{height: 2.5rem;border-radius: 1rem;position: relative;padding: 0.25rem;margin-bottom: 1rem;}
.f-items .item .item-imgbox{width: 2rem;height: 2rem;border-radius: 50%;overflow: hidden;position: absolute;left: 0.25rem;top: 0.25rem;}
.f-items .item .item-name{padding-left: 2.75rem;line-height: 2rem;font-size: 0.75rem;color: #444444;}
.f-items .item .item-write{width: 1.25rem;height: 1.25rem;position: absolute;top: 0.625rem;right: 3.5rem;}
.f-items .item .item-out{width: 1.25rem;height: 1.25rem;position: absolute;top: 0.625rem;right: 1rem;}
.bottomButton{  width:7.5rem;  margin:2.5rem auto;height: 2rem;  line-height: 2rem;  text-align: center;  background-color: #4685ff;  color:#fff;  font-size: 0.75rem;  -webkit-border-radius: 1rem;  -moz-border-radius: 1rem;  -ms-border-radius: 1rem;  -o-border-radius: 1rem;  border-radius: 1rem;}
</style>

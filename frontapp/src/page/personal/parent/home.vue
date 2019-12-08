<template>
  <div>
    <head-top :head="head"></head-top>
    <div class="person" style="padding: 2.1rem 0.75rem 0;">
        <div class="p-top">
            <div class="left-box">
                <div class="item-name">萨达姆 - 家长</div>
                <div class="item-msg">032103213 • 萨达姆父亲</div>
            </div>
            <div class="right-imgbox"><img src="" alt=""></div>
        </div>
        <div class="oper-items">
            <div class="item" @click="go_switch()" ><span class="item-name" >切换身份</span><div class="item-ico"><img src="../../../images/refresh-icon.png" alt=""></div></div>
            <div class="item" @click="go_infor()" ><span class="item-name"  >个人信息</span><div class="item-ico"><img src="../../../images/user-icon.png" alt=""></div></div>
            <div class="item"><span class="item-name" >我的动态</span><div class="item-ico"><img src="../../../images/shouchang.png" alt=""></div></div>
            <div class="item" @click="go_family()" ><span class="item-name"  >我的家庭</span><div class="item-ico"><img src="../../../images/home-icon.png" alt=""></div></div>
        </div>
    </div>
  </div>
</template>

<script type="es6">
  import HeadTop from '@/components/Head.vue'
  import { TransferDomDirective as TransferDom  } from 'vux'
  import { Cell, CellBox, Group } from 'vux'
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
      onClick(){
            console.log(213213213)
      },
      go_infor(){
        this.$router.push('/m/personal/parent/information')
      },
      go_family(){
        this.$router.push('/m/personal/parent/family')
      },
      go_switch(){
        this.$router.push('/m/personal/parent/switch')
      }
   },
    components: {
      HeadTop,
      Cell,
      CellBox,
      Group
    },
  }

</script>

<style scoped>
    .p-top{height: 3.75rem;margin-top: 1.5rem;position: relative;}
    .p-top .left-box{width: 10.5rem;height:100%;}
    .p-top .item-name{height: 2.25rem;color: #444444;font-size: 1.5rem;text-align: center;line-height: 1;}
    .p-top .item-msg{height: 1.5rem;color: #888888;font-size: 0.75rem;width: 100%;background: #f5f5f5;border-radius: 0.75rem;line-height: 1.5rem;text-align: center;}
    .p-top .right-imgbox{position: absolute;right: 0;top: 0;width: 3.75rem;height: 3.75rem;box-sizing: border-box;border: solid 0.125rem #FFFFFF;border-radius: 50%;box-shadow: 0 0 0.15rem rgba(0,0,0,0.2);}
    .oper-items .item{height: 3.75rem;border-bottom: solid 1px #eee;}
    .oper-items .item .item-name{line-height: 3.75rem;font-size: 0.9rem;color: #444;}
    .oper-items .item .item-ico{float: right;width: 1.25rem;height: 1.25rem;margin-top: 1.25rem;overflow: hidden; }
    .oper-items .item .item-ico img{display: block;width: 100%;}


</style>

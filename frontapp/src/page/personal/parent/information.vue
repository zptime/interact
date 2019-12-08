<template>
  <div>
    <head-top :head="head"></head-top>
    <div style="padding: 2.1rem 0.75rem 0;">
        <div class="p-top">
            <div class="left-box">
                <div class="item-name">萨达姆 - 家长</div>
                <div class="item-msg">032103213 • 萨达姆父亲</div>
            </div>
            <div class="right-imgbox"><img src="" alt=""></div>
        </div>
        <div>
            <group  label-width="5.5em" label-margin-right="2em" label-align="justify">
                <popup-radio title="性别" :options="sexs" v-model="sex" placeholder="请选择"   ></popup-radio>
                <datetime title="生日" v-model="time" value-text-align="right"  placeholder="请选择"   ></datetime>
                <x-address title="籍贯" v-model="addressValue" raw-value :list="addressData" value-text-align="right" label-align="justify" placeholder="请选择"     ></x-address>
            </group>
        </div>
    </div>
  </div>
</template>

<script type="es6">
  import HeadTop from '@/components/Head.vue'
  import { TransferDomDirective as TransferDom,Group, Cell, Datetime,ChinaAddressData, XAddress,PopupRadio } from 'vux'
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
        time:'',
        addressData: ChinaAddressData,
        addressValue: ['', '', ''],
        sexs:["男","女"],
        sex:'',
      }

   },
   methods:{

   },
    components: {
      HeadTop,
      Group,
      Cell,
      Datetime,
      ChinaAddressData,
      XAddress,
      PopupRadio
    },
  }

</script>

<style scoped>
.p-top{height: 3.75rem;margin-top: 1.5rem;position: relative;}
.p-top .left-box{width: 10.5rem;height:100%;}
.p-top .item-name{height: 2.25rem;color: #444444;font-size: 1.5rem;text-align: center;line-height: 1;}
.p-top .item-msg{height: 1.5rem;color: #888888;font-size: 0.75rem;width: 100%;background: #f5f5f5;border-radius: 0.75rem;line-height: 1.5rem;text-align: center;}
.p-top .right-imgbox{position: absolute;right: 0;top: 0;width: 3.75rem;height: 3.75rem;box-sizing: border-box;border: solid 0.125rem #FFFFFF;border-radius: 50%;box-shadow: 0 0 0.15rem rgba(0,0,0,0.2);}

.switch-items{margin-top: 1.5rem;}
.switch-items .item{padding: 0.75rem;height: 2.5rem;box-sizing: content-box;position: relative;margin-bottom: 0.75rem;}
.switch-items .item .img-box{width: 2.5rem;height: 2.5rem;position: absolute;left: 0.75rem;top: 0.75rem;border-radius: 50%;}
.switch-items .item .item-msg{margin-left: 3rem;height: 100%;}
.switch-items .item .item-msg .item-name{font-size: 0.75rem;color: #444444;margin-top: 0.2rem;}
.switch-items .item .item-msg .item-school{font-size: 0.6rem;color: #888;margin-top: 0.3rem;}
.switch-items .item .item-msg .item-select{position: absolute;right: 0;top:50%;transform: translateY(-50%)}
.bottomButton{  width:7.5rem;  margin:2.5rem auto;height: 2rem;  line-height: 2rem;  text-align: center;  background-color: #4685ff;  color:#fff;  font-size: 0.75rem;  -webkit-border-radius: 1rem;  -moz-border-radius: 1rem;  -ms-border-radius: 1rem;  -o-border-radius: 1rem;  border-radius: 1rem;}
</style>

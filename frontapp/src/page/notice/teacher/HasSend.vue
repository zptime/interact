<template>
  <div>
    <head-top :head="head"></head-top>

    <div class="contentBox" v-cloak >
        <actionsheet v-model="show" :menus="menus2" @on-click-menu="clickcall" show-cancel></actionsheet>
        <div>
           <tab :line-width=2 active-color='#fc378c' v-model="index" v-if="false">
            <tab-item class="vux-center" :selected="demo === item " v-for="(item, index) in list" @click="demo = item" :key="index">{{item}}</tab-item>
          </tab>
            <div style="margin-top: 0.8rem;" v-if="index==0">
                <search :search="search"></search>
            </div>
          <div style="">
                <swiper v-model="index" height="27rem"  :show-dots="false">
            <swiper-item v-for="(item, index) in list" :key="index">
              <div class="tab-swiper item-box">
                  <div v-if="index==0" style="max-height: 27rem;overflow: scroll;" >
                    <div v-for="i in 100"   class="item" :class="{ p2rem : operbox }" >
                        <icon v-if="false" style="position: absolute;top: 1rem;left: 0rem;" type="success"></icon>
                        <icon v-if="operbox" style="position: absolute;top: 1rem;left: 0rem;" type="circle"></icon>
                        <div  :class=" { l2rem : operbox }"  class="img-box"><img src="" alt=""><div class="item-read"></div></div>
                        <div class="item-content">
                            <div class="item-top"><span class="item-type">班级通知 - </span><span class="item-name">刘谨,刘谨,刘谨,刘谨,刘谨,刘谨，刘谨,刘谨,刘谨，刘谨,刘谨,刘谨</span><span class="item-time">9:00</span></div>
                            <div class="item-txt">这是一段很长的介绍文字这是一段很长的介绍文字这是一段很长的介绍文字这是一段很长的介绍文字</div>
                        </div>
                    </div>
                  </div>
                  <div v-if="index==1" style="text-align: center;line-height: 5rem;" @click="show_div()">这是另外一个tab</div>
              </div>
            </swiper-item>
          </swiper>
          </div>

        </div>
        <div class="edit-btn" v-if="!operbox" @click="operbox=true">编辑</div>

        <flexbox v-if="operbox">
          <flexbox-item><div class="flex-demo">全选</div></flexbox-item>
          <flexbox-item><div class="flex-demo" @click="operbox=false" >删除所选</div></flexbox-item>
          <flexbox-item><div class="flex-demo" >清空</div></flexbox-item>
        </flexbox>


        <div v-transfer-dom>
          <x-dialog  hide-on-blur    :dialog-style="{ 'height': 'auto','right':'1.125rem','bottom':'-15.6rem','background':'none','width':'3.5rem'}"      v-model="showdialog" class="dialog-extend clb" >
                <router-link to="/m/notice/teacher/noticeSend"><div class="dialog-item">作业通知</div></router-link>
                <div class="dialog-item">普通通知</div>
                <div class="dialog-item">已发通知</div>
                <div class="dialog-item">编辑</div>
          </x-dialog>
        </div>

    </div>
  </div>
</template>

<script type="es6">
  import HeadTop from '@/components/Head.vue'
  import Search from '@/components/m-search/Search.vue'
  import { Tab, TabItem,Swiper, SwiperItem ,Confirm ,TransferDomDirective as TransferDom ,Actionsheet,XDialog,Box, Icon ,Flexbox, FlexboxItem } from 'vux'
  import { testLogin }  from '../../../service/getData.js'
  export default {
    directives: {
        TransferDom
    },
    data () {
      return {
        head:{
          icon: 'return',
          title: '互动系统-消息通知',
          more: false
        },
        search:{
          is_focus:false,
          search_txt:'',
          placehoder_txt:'',
        },
        disabled: typeof navigator !== 'undefined' && /iphone/i.test(navigator.userAgent) && /ucbrowser/i.test(navigator.userAgent),
        demo:'',
        list:["消息通知"],
        index:0,
        show:false,
        txt:"提示文字",
        menus2: {
            menu1: "分享到朋友圈",
            menu2: "分享到新浪微博",
        },
        showdialog:false,
        operbox:false,
      }
    },
    methods:{
        async login(){
            let res = await testLogin('fenghuo','fhuo_03');
            console.log(res)
        },
        show_div(){
            this.show = !this.show;
        },
        clickcall(key){
            alert("you just click the "+ key);
            console.log(this.menus2[key])
        },
        go_detail(){
                this.$router.push("/m/notice/teacher/noticeDetail");
        }
    },
    watch:{
        index:(cur,old)=>{console.log(cur)}
    },
    created(){

    },
    components: {
      HeadTop,
      Search,
      Tab,
      TabItem,
      Swiper,
      SwiperItem,
      Confirm,
      Actionsheet,
      XDialog,
      Box,
      Icon,
      Flexbox,
      FlexboxItem
    },
  }
</script>

<style scoped>
    .edit-btn{width: 7.5rem;height: 2rem;background: #4685ff;border-radius: 1rem;text-align: center;line-height: 2rem;color: #FFFFFF;font-size: 0.75rem;position: fixed;bottom: 1rem;left: 50%;transform: translateX(-50%)}
    .dialog-extend{}
    .dialog-extend .weui-dialog{background:none;}
    .dialog-item{height: 2.25rem;width: 4.5rem;line-height: 2.25rem;color: #FFFFFF;font-size: 0.7rem;background: none;}
    .navitems{height: 2rem;margin-bottom: 0.2rem;}
    .navitems .item-nav{width: 50%;height: 2rem;float: left;text-align: center;line-height: 2rem;position: relative;}
    .navitems .item-nav.active::after{content: "";display: block;position: absolute;left: 50%;bottom: 0;width: 40%;height: 0.2rem;background: #308ce3;transform: translateX(-50%)}
    .item{padding: 0.5rem 0;width: 100%;box-sizing: border-box;position: relative;height: 3.25rem;border-bottom: solid 1px #f1f1f1;}
    .item .img-box{position: absolute;left: 0rem;top: 0.5rem;width: 2.25rem;height: 2.25rem;border-radius: 50%;overflow: hidden;border: solid 1px #eeeeee;}
    .item .img-box .item-read{position: absolute;right: 0;top: 0;width: 0.6rem;height: 0.6rem;background: #f74747;border-radius: 50%;}
    .item .item-content{padding-left: 2.6rem;line-height: 1.2rem;}
    .item .item-top{position: relative;width: 100%;overflow: hidden;text-overflow: ellipsis;white-space: nowrap;box-sizing: border-box;padding-right: 3rem;}
    .item .item-top .item-time{position: absolute;top: 0.2rem;right: 0;color: #666666;font-size: 0.3rem;}
    .item .item-txt{font-size: 0.3rem;color: #666;width: 100%;overflow: hidden;text-overflow: ellipsis;white-space: nowrap;line-height: 0.8rem;position: relative;box-sizing: border-box;padding-right: 1.6rem;}
    .item .oper-box{position: absolute;right: 0;top: 1.6rem;}
    .item .item-type {color: #000;font-size: 0.8rem}
    .item .item-name{font-size: 0.8rem;color: #000;}
    .vux-center{line-height: 5rem;text-align: center;}
    .item-box{padding: 1.5rem 0.8rem;}
    .hover-publish{width: 2.25rem;height: 2.25rem;background: #4785ff;border-radius: 50%;overflow: hidden;position: fixed;bottom: 2rem;right: 1rem;color: #FFFFFF;text-align: center;line-height: 2rem;font-size: 1.6rem;border: solid 0.1rem #FFFFFF;box-shadow: 0 0 20px #c6d9ef;box-sizing: content-box;}
    .flex-demo {text-align: center;color: #fff;background-color: #4785ff;border-radius: 4px;background-clip: padding-box;height: 1.6rem;line-height: 1.6rem;font-size: 0.75rem;}
    .p2rem{padding-left: 2rem}
    .item .l2rem{left: 2rem;}
</style>

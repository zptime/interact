<template>
  <div v-cloak>
    <head-top :head="head"></head-top>
      <div style="padding-top: 2.1rem;background: #FFFFFF;">
          <div v-if="show" class="d-top clb">
              <div class="img-box"><img v-if="detail.sender_avatar !=''" :src="detail.sender_avatar" alt=""><img v-if="detail.sender_avatar =='' "   src="../../../images/icon-default-avatar.png" alt=""></div>
              <div class="t-right">
                  <div class="top">{{ detail.sender_username }}</div>
                  <div class="bottom clb">
                      <div v-if="false" class="fujian"></div>
                      <div class="t-time">{{ detail.create_time }}</div>
                  </div>
              </div>
              <div class="t-detail" @click="show=false">详情</div>
          </div>
          <div v-if="!show" class="excluded" style="padding-top: 1.75rem;position: relative;">
              <div class="shouqi" @click="show=true" >收起</div>
              <div class="item clb">
                  <div class="item-left fl">发起人:</div>
                  <div class="item-right fl">{{  detail.sender_username  }}</div>
              </div>
              <div class="item clb">
                  <div class="item-left fl">收件人:</div>
                  <div class="item-right fl namelist"><div class="name-item"  v-for="item in receivers"  >{{ item }}</div></div>
              </div>
              <!--
              <div class="item clb">
                  <div class="item-left fl">范围:</div>
                  <div class="item-right fl">李明</div>
              </div>
              -->
              <div class="item clb">
                  <div class="item-left fl">时间:</div>
                  <div class="item-right fl" style="color: #aaa;">{{ detail.create_time }}</div>
              </div>
              <div class="item clb" v-if="voiceArr.length !=0 && fileArr.length !=0">
                  <div class="item-left fl" >附件:</div>
                  <div class="item-right fl">
                      <p style="margin-bottom: 1.4rem"  v-for="item in voiceArr"   >{{ item.voice_name }}</p>
                      <p style="margin-bottom: 1.4rem;"   v-for="item in fileArr">{{ item.file_name }}</p>
                  </div>
              </div>
          </div>
          <div class="content">
              <div  class="content-txt">{{ detail.content }}</div>
                  <Maudio :contentSecStyle="myFileStyle1" :popupBtn="false"   :removeIcon="false"  url="voice_converted_url"  :origin="voiceArr" />
                  <Mfile  :contentSecStyle="myFileStyle2"   :fileData="fileArr"  :showDelete="false"  :popupBtn="false" />
              <div class="readnum"  @click="showpopup=true" v-if="detail.read_count>=0" >已有{{ detail.read_count }}人阅读</div>
          </div>

          <popup v-model="showpopup" width="100%" height="100%" position="right" :show-mask=false>
            <read   @goback="showpopup=false"   :notify_id="notify_id" />
          </popup>
      </div>
  </div>
</template>

<script type="text/ecmascript-6">
  import HeadTop from '@/components/Head.vue'
  import { Popup } from 'vux'
  import read from './read.vue'
  import { getNoticeDetail,getNoticeSendList,setReaded } from '../../../service/getData.js'
  import Mfile from '@/components/m-file/chooseFile'
  import Maudio from '@/components/m-audio/index'
  export default {
    data () {
      return {
        head:{
          icon: 'return',
          title: '通知详情',
          more: false
        },
        showpopup:false,
        show:true,
        str:'已经有100人阅读',
        detail:{},
        receivers:'',//接收者们
        notify_id:'',
        fileArr:[],
        voiceArr:[],
        myFileStyle1:{
             'marginTop':'1rem'
        },
        myFileStyle2:{
             'marginTop':'1rem',
        }
      }
    },
    methods:{
        goReader(){
            this.$router.push("/m/notice/teacher/read")
        },
        async initDetail(notify_id){
            let res = await getNoticeDetail(notify_id) ;
            if(res.c==0){
                this.detail=res.d;
                console.log(res.d);
              //  this.str = this.detail.read_count;
                this.fileArr = [];
                for(let i in res.d.files){
                      res.d.files[i].downloadState=0;
                      this.fileArr.push(res.d.files[i]);
                }
                this.voiceArr = [];
                for(let i in res.d.voices){
                      this.voiceArr.push(res.d.voices[i]);
                }
            }
        },
        async getSendReceivers(notify_id){
            let res = await getNoticeSendList(notify_id);
            this.receivers = res.d.name_list;
        },
    },
    created(){
        let notify_id = this.$route.query.notify_id;
        this.notify_id = notify_id;
        this.initDetail(notify_id);
        this.getSendReceivers(notify_id);

    },
    components: {
      HeadTop,
      read,
      Popup,
      Mfile,
      Maudio
    },
  }
</script>

<style scoped>
    .fl{float: left}
    .name-item{width: 4rem;line-height: 1.2rem;float: left}
    .d-top{padding: 1rem 0.75rem;border-bottom: solid 1px #eeeeee;position: relative;}
    .d-top .img-box{width: 2.5rem;height: 2.5rem;border-radius: 50%;overflow: hidden;float: left;border: solid 1px #eeeeee;}
    .d-top .img-box img{width: 100%;}
    .d-top .t-right{float: left;height: 100%;line-height:1rem;margin-left: 0.5rem; }
    .d-top .t-right .top{font-size: 0.8rem;color: #111111;margin-top: 0.3rem;}
    .d-top .t-right .bottom{height: 1rem;font-size: 0.6rem;margin-top: 0.1rem;position: relative;width: 12rem;}
    .d-top .t-right .bottom .fujian{float: left;width: 2rem;height: 1rem;margin-right: 0.5rem;}
    .d-top .t-right .bottom  .t-time{float: left;color: #AAAAAA;white-space: nowrap;}
    .d-top  .t-detail{position: absolute;color: #4685ff;bottom: 1.1rem;right: 0.75rem;font-size: 0.8rem;}
    .content{background: #f5f5f5;padding: 0.75rem;}
    .content-txt{padding: 1rem 0;font-size: 0.8rem;}
    .content-fujian .item-fj{border-radius: 0.1rem;height: 4rem;box-sizing: border-box;padding: 0.75rem;border: solid 1px #eeeeee;border-radius: 4px;position: relative;margin-bottom: 1rem;}
    .content-fujian .item-fj .item-imgbox{width: 2rem;height: 2.2rem;position: absolute;left: 0.75rem;top: 0.75rem;border-radius: 0.1rem;overflow: hidden;border: solid 1px #eee;}
    .content-fujian .item-fj .item-name{position: absolute;top: 0.75rem;left: 4rem;color:#444;font-size: 0.8rem; }
    .content-fujian .item-fj .item-size{position: absolute;bottom: 0.75rem;left: 4rem;color:#666;font-size: 0.3rem; }
    .content-fujian .item-fj .item-btn{width: 4.5rem;height: 1.9rem;line-height: 1.9rem;color: #FFFFFF;text-align: center;position: absolute;right: 0.75rem;top: 1rem;background: #4685ff;border-radius: 0.1rem;font-size: 0.8rem}
    .hasread{font-size: 0.8rem;color: #aaa;}
    .readnum .readnum-icon{width: 1rem;height: 1rem;float: right;margin-top: 0.5rem;background: url("../../../images/icon-arrow.png")no-repeat center center ; background-size: 100% 100%;transform:rotate(-90deg);-ms-transform:rotate(-90deg); 	/* IE 9 */  -moz-transform:rotate(7deg); 	/* Firefox */  -webkit-transform:rotate(-90deg); /* Safari 和 Chrome */  -o-transform:rotate(-90deg); 	/* Opera */}
    .readnum{color: #4685ff;font-size: 0.8rem;margin-top: 1rem;}
    .excluded .item{margin-bottom: 1rem;font-size: 0.8rem;}
    .excluded .item .item-left{color: #AAAAAA;width: 3.75rem;text-align: right;}
    .excluded .item .item-right{color: #444;width:10rem;padding-left: 0.8rem;}
    .excluded .item .item-right.namelist{width: 14rem;}
    .excluded .shouqi{right: 0.75rem;top: 1.6rem;color: #4685ff;font-size: 0.8rem;position: absolute;}
</style>

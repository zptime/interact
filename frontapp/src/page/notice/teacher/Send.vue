<template>
  <div>
    <head-top :head="head"></head-top>
    <div class="content" style="padding: 3.6rem 0.75rem 0rem 0.75rem;">
        <div class="textarea-box boxShadowGray borderRadius">
            <textarea  v-model="sendmsg.content"   placeholder="输入您想要发布的内容"  style="width: 100%;height: 100%;resize: none;padding: 0.2rem;font-size: 0.8rem;"  ></textarea>
        </div>
        <div style="height: 0.1rem;"></div>
        <div  class="oper-box clb">
            <m-choose   class="chooseView"
                        ref="mChooseView"
              :_subComponents="m3_choose._subComponents"
              :_mAudio="m3_choose._mAudio"
              :_mImg="m3_choose._mImg"
              :_cFile="m3_choose._cFile"
              :_mVideo="m3_choose._mVideo"
              @on-mAudioChange="audioChanged"
              @on-cFileChange="fileProgressed"
              @on-shouldShowH5Record="shouldShowH5Record">
            </m-choose>
        </div>

        <div style="margin-top: 2.5rem;">
            <group  label-width="4.5em" label-margin-right="2em" >
              <cell title="选择对象"   @click.native="choose()"   :value="sendmsg.str"  is-link></cell>
            </group>
        </div>

        <actionsheet v-model="show" :menus="menus" @on-click-menu="sendclick" ></actionsheet>
        <div class="btns boxShadowGray clb">
            <div class="item-btn fl" @click="cancel()">取消</div>
            <div class="item-btn fl"  @click="send()"  style="color: #4085ff;">确定</div>
        </div>

          <popup v-model="showpopup2" width="100%" height="100%" position="right" :show-mask=false>
            <choosePerson    @backPopup="togglePopup"   :hasChose="sendmsg.hasChose"      @onGoBack="showpopup2" />
          </popup>




    </div>
    <!--modify by perry-->
    <popup v-model="needRecordAudio" height="12.5rem" @on-hide="popupHide" is-transparent >
      <recordView ref="audioView" @on-startRecord="startRecord" @on-stopRecord="stopRecord" @on-makeSure="makeSure" @on-cancleClick="cancelClick"></recordView>
    </popup>
  </div>
</template>

<script type="es6">
  import HeadTop from '@/components/Head.vue'
  import { Group, Cell , TransferDom, Actionsheet,Popup } from 'vux'
  import { sendNotice } from '../../../service/getData.js'
  import MChoose from '@/components/m-choose/index'
  import choosePerson from './choosePerson.vue'
  import popup from 'vux/src/components/popup/index.vue'
  import recordView from '../../../components/m-recordAudioView/index.vue'
  export default {
    data () {
      return {
        needRecordAudio:false,
        head:{
          icon: 'return',
          title: '',
          more: false
        },
        sendmsg:{
            content:'',
            voice_ids:'',
            file_ids:'',
            type:'',
            receivers:'',
            choosedArr:[],
            str:'',
            hasChose:false,
        },
        show: false,
        menus:{
            menu1:'只通知家长',
            menu2:'同时通知家长和学生'
        },
        showpopup1:false,
        showpopup2:false,
        m3_choose: {
          _cFile:{
            popupBtn:true,
            showDelete:true
          },
          _subComponents: ['m-audio','choose-file'],
          _mAudio: {
            url: 'voice_url'
          },
          _mImg: {
            maxCount: 9,
            url:'origin_image_url',
          },
          _mVideo: {
            popupBtn:false,
          },
        },
      }
    },
    directives: {
        TransferDom
    },
    methods:{
        choose(){
            this.showpopup2 = true ;
        },
        sendclick(key){
            console.log(key)
        },
        togglePopup(data){
            this.sendmsg.hasChose = true ;
            this.showpopup2 = false;
            if(data.length>0){
                this.sendmsg.choosedArr = data;
            }
            this.sendmsg.str =  '共选择'+ this.sendmsg.choosedArr.length +'名学生';

        },
        cancel(){
            this.$router.back(-1);
        },
        async send(){
            let str = '';
            for(let i in this.sendmsg.choosedArr){
                str+= this.sendmsg.choosedArr[i].account_id +','+this.sendmsg.choosedArr[i].user_type_id+','+this.sendmsg.choosedArr[i].school_id+';'
            }
            if(this.sendmsg.content==''){
                this.$vux.toast.show({
                 text: '请填写通知内容!',
                 time:'1000',
                })
                return;
            }
            if(str==''){
                this.$vux.toast.show({
                 text: '请选择通知人员',
                 time:'1000',
                })
                return;
            }
            this.$vux.loading.show();
            let res = await sendNotice(this.sendmsg.content,this.sendmsg.voice_ids,this.sendmsg.file_ids,this.sendmsg.type,str);
            this.$vux.loading.hide();
            if(res.c==0){
                this.$router.back(-1);
            }
        },
        audioChanged(data){
            let str = '';
            for(let i in data){
                str = data[i].voice_id+','

            }
            this.sendmsg.voice_ids = str;
        },
        fileProgressed(data){
           let str = '';
            for(let i in data){
                str = data[i].file_id+','
            }
            this.sendmsg.file_ids = str;
        },
      // modify by perry
      shouldShowH5Record(shouldShow) {
        //alert("shouldShowH5Record" + shouldShow);
        this.needRecordAudio = shouldShow;
      },
      popupHide() {
        this.$refs.mChooseView.execAudioAction('stopRecord',null);
        this.$refs.audioView.cancleRecord();
      },
      startRecord() {
        this.$refs.mChooseView.execAudioAction('startRecord',null);
      },
      stopRecord() {
        this.$refs.mChooseView.execAudioAction('stopRecord',null);
      },
      makeSure(time) {
        this.$refs.mChooseView.execAudioAction('makeSure',time);
        this.needRecordAudio = false;
      },
      cancelClick() {
        this.$refs.mChooseView.execAudioAction('cancelClick',null);
        this.needRecordAudio = false;
      },
    },
    created(){
        if(this.$route.query.type=='class'){
            this.sendmsg.type=1;
            this.head.title = "发班级通知"
        }else if(this.$route.query.type=='work'){
            this.sendmsg.type=2;
            this.head.title = "发作业通知"
        }
    },
    components: {
      HeadTop,
      Group,
      Cell,
      TransferDom,
      Actionsheet,
      Popup,
      MChoose,
      choosePerson,
      recordView,
      popup,
    },
  }
</script>

<style scoped>
    .fl{float: left;}
    .textarea-box{height: 7.5rem;margin-bottom: 1rem;}
    .oper-btn{width: 4rem;height: 1.5rem;border: solid 1px #4685ff;text-align: center;line-height: 1.5rem;color: #4685ff;font-size: 0.6rem;border-radius: 0.75rem;}
    .delete-xx{ display:block;width: 0.75rem;height: 0.75rem;background: #aaa;text-align: center;line-height: 0.6rem;color: #FFFFFF;font-size: 0.5rem;border-radius: 50%;}
    .luyin{width: 8rem;height: 2rem;background: #4685ff;border-radius: 1rem;line-height: 2rem;padding: 0 1rem;text-align: right;color: #FFFFFF;position: relative;margin-top: 1.5rem;margin-bottom: 1rem;}
    .up-doc{width: 15rem;height: 2.5rem;box-sizing: border-box;padding:0.375rem 0.5rem;border: solid 1px #eeeeee;position: relative;margin-bottom: 2.5rem;}
    .docimg-box{width: 1.75rem;height: 1.75rem;position: absolute;top: 0.375rem;left: 0.5rem;border: solid 1px #eeeeee;}
    .docimg-box img{display: block;}
    .doc-name{color: #444444;font-size: 0.6rem;width: 9.5rem;overflow: hidden;text-overflow: ellipsis;white-space: nowrap;position: absolute;top: 0.4rem;left: 2.6rem;}
    .doc-size{color: #AAAAAA;font-size: 0.6rem;position: absolute;left: 2.6rem;top: 1.4rem;}
    .btns{width: 10rem;height: 2rem;margin: 2rem auto 1rem;border-radius: 1rem;line-height: 2rem;text-align: center;position: relative;}
    .btns:after{content: "";position: absolute;left: 50%;top: 50%;transform: translateX(-50%)translateY(-50%);width: 2px;height:0.75rem;background: #eee; }
    .btns .item-btn{width: 50%;font-size: 0.75rem;}
</style>

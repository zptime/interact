<template>
  <div>
    <head-top :head="head">
      <img slot="left" src="../../images/icon-return.png" @click="goBack"/>
    </head-top>
    <div class="contentBox" @click="detail_all" v-cloak>
      <div class="nav clb">
        <span :class="{'active':navId==item.id}" v-for="item in navItem" @click="changeNav(item.id)">
          {{ item.item }}
        </span>
      </div>
      <div class="select_student boxShadowGray borderRadiusRem" @click="showChoosePerson=true">
        <span v-if="personList.length===0">请选择学生</span>
        <span v-else>{{ personShow }}</span>
      </div>
      <span class="title_detail">发送到</span>
      <div class="DropBox" @click="show=true;flag=0">
        <span class="DropBoxShow" v-if="checkboxList.length">{{ checkboxShow }}等</span><span class="DropBoxShow">{{checkboxList.length}}个班级</span>
        <span id="triangle-down" ></span>
      </div>

      <!--表扬-->
      <div class="list" v-show="navId==1">
        <x-textarea class="moment_textarea boxShadowGray borderRadius" :placeholder="textareaCfg.placeholder"
                    :height="textareaCfg.height"
                    v-model="content">
        </x-textarea>
        <m-choose class="chooseView"
          ref="mChooseView"
          :_subComponents="m_choose._subComponents"
          :_mAudio="m_choose._mAudio"
          :_mImg="m_choose._mImg"
          :_cFile="m_choose._cFile"
          @on-shouldShowH5Record="shouldShowH5Record"
          @on-mAudioChange="audioChanged"
          @on-mImgChange="imgChanged"
          @on-cFileChange="fileProgressed">
        </m-choose>
      </div>

      <!--批评-->
      <div class="list" v-show="navId==2">
        <x-textarea class="moment_textarea boxShadowGray borderRadius" :placeholder="textareaCfg.placeholder"
                    :height="textareaCfg.height" v-model="content">
        </x-textarea>
        <m-choose class="chooseView"
          :_subComponents="m2_choose._subComponents"
          :_mAudio="m2_choose._mAudio"
          :_mImg="m2_choose._mImg"
          :_cFile="m2_choose._cFile"
          @on-mAudioChange="audioChanged"
          @on-mImgChange="imgChanged"
          @on-cFileChange="fileProgressed">
        </m-choose>
      </div>

      <!--发布和取消-->
      <div class="list btns boxShadowGray clb">
        <div class="item-btn fl" @click="goBack">取消</div>
        <div class="item-btn fl" style="color: #4085ff;" @click="publish(navId)">发布</div>
      </div>

      <!--下拉弹框-->
      <div class="div_select boxShadowGray" v-if="show">
        <ul @click="flag=0">
          <li class="border_bottom" v-if="navId==2" @click="is_visible_for_parent_related=(is_visible_for_parent_related==1?0:1)">
            <div class="div_select_view">
              <img class="left" src="../../components/m-personChoose/images/icon_choosed.png" v-if="is_visible_for_parent_related==1"/>
              <img class="left" src="../../components/m-personChoose/images/icon_choosed_not.png" v-else/>
              <span class="left" style="color: #4685ff;">批评仅被批评学生的家长可见</span>
            </div>
          </li>
          <li v-for="(item,index) in this.ClassList" @click="pushCheckBox(item.state,index)">
            <div class="div_select_title" v-if="index==0">班级内学生和家长可见</div>
            <div class="div_select_view">
              <img class="left" src="../../components/m-personChoose/images/icon_choosed.png" v-if="item.state"/>
              <img class="left" src="../../components/m-personChoose/images/icon_choosed_not.png" v-else/>
              <span class="left">{{ item.class_name }}</span>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <!--选择学生-->
    <popup v-model="showChoosePerson" width="100%" height="100%" position="right" :show-mask=false>
      <choosePerson @backPopup="backPopup" />
    </popup>

    <!--modify by perry-->
    <popup v-model="needRecordAudio" height="12.5rem" @on-hide="popupHide" is-transparent >
      <recordView ref="audioView" @on-startRecord="startRecord" @on-stopRecord="stopRecord" @on-makeSure="makeSure" @on-cancleClick="cancelClick"></recordView>
    </popup>
  </div>
</template>

<script type="text/ecmascript-6">
  const MImg = r => require.ensure([], () => r(require('../../components/m-img/index')), 'MImg');
  import HeadTop from '@/components/Head.vue'
  import MAudio from '../../components/m-audio/index.vue'
  import choosePerson from './choosePerson.vue'
  import { publish_evaluate } from '../../service/getData.js'
  import { getClassList }  from '../../service/getData.js'
  import MChoose from '../../components/m-choose/index'
  import XTextarea from 'vux/src/components/x-textarea/index.vue'
  import { mapState,mapMutations } from 'vuex'
  import { CheckIcon  } from 'vux'
  import recordView from '../../components/m-recordAudioView/index.vue'
  import popup from 'vux/src/components/popup/index.vue'

  export default {
    data () {
      return {
      	content:'',
        needRecordAudio: false, // modify by perry
        head:{
          icon: 'return',
          title: '发评价',
          more: false
        },
        navId:1,//导航栏ID
        navItem:[{'item':'被表扬的学生','id':1},{'item':'被批评的学生','id':2}],
        textareaCfg: {
          placeholder: '请输入你想发送的内容',
          height: 150,
        },
        m_choose: {
          _cFile:{
            popupBtn:false,
            showDelete:false
          },
          _subComponents: ['m-audio','m-img','choose-file'],
          _mAudio: {
            url: 'voice_url'
          },
          _mImg: {
            maxCount: 9,
            url:'origin_image_url',
          },
        },
        m2_choose: {
          _cFile:{
            popupBtn:false,
            showDelete:false
          },
          _subComponents: ['m-audio','m-img','choose-file'],
          _mAudio: {
            url: 'voice_url'
          },
          _mImg: {
            maxCount: 9,
            url:'origin_image_url',
          },
        },
        show:false, //下拉菜单
        flag:1,
        checkboxList:[],   //存放已选的list
        checkboxShow:'',
        image_ids:['',''],
        voice_ids:['',''],
        is_visible_for_parent_related:1, //批评仅被批评学生的家长可见
        ClassList:[],
        showChoosePerson:false, //选择学生
        personList:[], //存放已选的学生
        personShow:''
      }
    },
    components: {
      HeadTop,
      MImg,
      MAudio,
      MChoose,
      XTextarea,
      CheckIcon,
      recordView,
      popup,
      choosePerson
    },
    computed:{
      ...mapState([
        'user_info',
        'user_type_id',
      ])
    },
    created(){
      this.init_data();
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
        }
      },

    	//获取本人相关班级
      async init_data(){
        let res = await getClassList();
        for (let i=0;i<res.d.length;i++){
        	this.ClassList.push({"class_id": res.d[i].class_id, "class_name": res.d[i].class_name,"state":false})
        }
      },

      //点击其他部分隐藏弹框
      detail_all(){
        if (this.flag ==1){
          this.show = false
        }
        this.flag = 1
      },

      //切换tab栏
      changeNav(id){
        this.navId = id;
        this.initData();
      },

      //初始化数据
      initData(){
      	this.content = '';
      	this.checkboxList=[];   //存放已选的list
        this.checkboxShow='';
        for (let i=0;i<this.ClassList.length;i++){
        	this.ClassList[i].state = false
        }
      },

      //接受文件的数据
      fileProgressed(data){

      },

      //图片
      imgChanged(data){
        this.image_ids[this.navId]="";
        if(data){
          for (let i = 0 ; i < data.length; i++){
            this.image_ids[this.navId] += data[i].image_id +',';
          }
          this.image_ids[this.navId] = this.image_ids[this.navId].slice(0,this.image_ids[this.navId].length-1);
        }
      },

      // modify by perry
      shouldShowH5Record(shouldShow) {
          //alert("shouldShowH5Record" + shouldShow);
          this.needRecordAudio = shouldShow;
      },
      popupHide() {
        this.$refs.mChooseView.execAudioAction('startRecord',null);
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
      //语音
      audioChanged(data){
        this.voice_ids[this.navId]="";
        if(data){
          for (let i = 0 ; i < data.length; i++){
            this.voice_ids[this.navId] += data[i].voice_id +',';
          }
          this.voice_ids[this.navId] = this.voice_ids[this.navId].slice(0,this.voice_ids[this.navId].length-1);
        }
      },

      //下拉框中单选框的处理
      pushCheckBox(state,index){
        //注意此时的index 并不是你点玩后的状态  而是你点击之前的状态
        //所以判断是反过来的  手机与pc是相反的！！！
        this.checkboxList=[];   //存放已选的list
        this.checkboxShow='';
        if (state == true){
          this.ClassList[index].state = false
        }else {
        	this.ClassList[index].state = true
        }
        for (let i=0;i<this.ClassList.length;i++){
        	if (this.ClassList[i].state == true){
        		this.checkboxList.push(this.ClassList[i].class_name)
          }
        }
        if(this.checkboxList.length<=2){
        	for(let i=0; i<this.checkboxList.length; i++){
            this.checkboxShow += this.checkboxList[i] +'、'
          }
        }else{
          for(let i=0; i<2; i++){
            this.checkboxShow += this.checkboxList[i] +'、'
          }
        }
        this.checkboxShow = this.checkboxShow.substr(0,this.checkboxShow.length-1)
      },

      //提交
      async publish(evaluate_type){
        //评价对象的三元组列表
        let evaluate_user_triples = '';
        for (let i=0; i<this.personList.length; i++) {
          evaluate_user_triples += this.personList[i].account_id + ',' + this.personList[i].user_type_id + ',' + this.personList[i].school_id + ';'
        }

        //发布到的班级
      	let class_ids = '';
        for (let i=0;i<this.ClassList.length;i++){
        	if(this.ClassList[i].state == true){
            class_ids += this.ClassList[i].class_id +',';
          }
        }
        class_ids = class_ids.slice(0,class_ids.length-1);

        if (this.personList.length === 0) {
          this.$vux.toast.show({
            type: 'text',
            text: '请选择学生！'
          })
        } else if (this.content == '') {
          this.$vux.toast.show({
            type: 'text',
            text: '请输入动态文字内容！'
          })
        } else if (class_ids == '') {
          this.$vux.toast.show({
            type: 'text',
            text: '请选择发送到的班级！'
          })
        } else {
          this.$vux.loading.show({
            text: '发布中'
          });
          let res = await publish_evaluate(this.content,this.voice_ids[this.navId],this.image_ids[this.navId],evaluate_type,evaluate_user_triples,'','',evaluate_type==1?'':this.is_visible_for_parent_related,class_ids);
          this.$vux.loading.hide();
          if (res.c == 0){
            this.goBack();
          }else{
            this.$vux.toast.show({
              type: 'text',
              text: res.m
            })
          }
        }
      },

      // 选择学生popup
      backPopup(data){
        this.showChoosePerson = false;
        if(data.length>0){
          this.personList = data;
        }
        this.personShow = '共选择'+ this.personList.length +'名学生';
      }
    }
  }
</script>

<style scoped>
  .list{
    margin: 0.75rem;
  }
  .nav{
    width:10rem;
    text-align: center;
    margin: 1rem auto 0 auto;
    border: 1px solid #4685ff;
    -webkit-border-radius: 4px;
    -moz-border-radius: 4px;
    -ms-border-radius: 4px;
    -o-border-radius: 4px;
    border-radius: 4px;
  }
  .nav span{
    display: inline-block;
    width: 50%;
    height: 1.5rem;
    line-height: 1.5rem;
    font-size: 0.6rem;
    color: #444;
    float:left;
  }
  .nav span:last-child{
    float: right;
  }
  .nav span.active{
    background-color: #4685ff;
    color:#fff;
  }
  .evaluation_title{
    margin-top: 1rem;
    text-align: center;
    font-size: 0.6rem;
  }
  .evaluation_title button{
    float:left;
  }
  .title_detail{
    margin: 0 0.75rem;
    display: inline-block;
    font-size: 0.75rem;
  }
  .DropBox{
    display: inline-block;
    margin-left: 0.75rem;
  }
  .DropBoxShow{
    font-size: 0.75rem;
    color: #4685ff;
  }
  .boxShadowGray{
    box-shadow: 0 0 16px 4px rgba(0, 0, 0, 0.08);
    -moz-box-shadow: 0 0 3px 3px rgba(0, 0, 0, 0.08);
    -webkit-box-shadow: 0 0 3px 3px rgba(0, 0, 0, 0.08);
  }
  .borderRadiusRem{
    -webkit-border-radius: 1.25rem;
    -moz-border-radius: 1.25rem;
    -ms-border-radius: 1.25rem;
    -o-border-radius: 1.25rem;
    border-radius: 1.25rem;
  }

  .select_student{
    height: 2.5rem;
    margin: 1.5rem 0.75rem;
    text-align: center;
    font-size: 0.75rem;
    font-weight: bold;
    line-height: 2.5rem;
    color: #444;
  }
  .moment_textarea{
    font-size: 0.75rem;
    color: #888;
    width: 100%;
    display: inline-block;
  }
  .btns{
    width: 10rem;
    height: 2rem;
    margin: 2rem auto 1rem;
    border-radius: 1rem;
    line-height: 2rem;
    text-align: center;
    display: -webkit-box;
  }
  .btns .item-btn{
    width: 50%;
    font-size: 0.75rem;
  }
  .chooseView{
    margin-top: 4.5rem!important;
  }
  .div_select{
    width: 14rem;
    position: absolute;
    top: 9.5rem;
    left: 4rem;
    padding: 0.5rem;
    z-index: 999;
    background: #fff;
    /*text-align: center;*/
    font-size: 0.75rem;
  }
  .div_select ul li{
    float: left;
    width: 94%;
    padding: 0.25rem 0;
  }
  .border_bottom{
    border-bottom: 1px #eee solid;
    padding-bottom: 0.25rem;
  }
  .div_select_title{
    color: #aaa;
    margin-bottom: 0.25rem;
  }
  .div_select_view {
    margin: 0.5rem 0;
    line-height: 1rem;
    overflow: hidden;
  }
  .div_select_view img {
    width: 1rem;
  }
  .div_select_view span {
    margin-left: 0.5rem;
    font-size: 0.75rem;
  }
  #triangle-down {
    display: inline-block;
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 10px solid #4685ff;
  }
</style>

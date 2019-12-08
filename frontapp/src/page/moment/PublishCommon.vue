<template>
  <div>
    <head-top :head="head">
      <img slot="left" src="../../images/icon-return.png" @click="goBack"/>
    </head-top>
    <div class="contentBox" @click="detail_all" v-cloak>
      <tab v-model="index" :line-width=4 custom-bar-width="40px" active-color="#666" bar-active-color="#4685ff">
        <tab-item>图片</tab-item>
        <tab-item>视频</tab-item>
        <tab-item v-if="userInfo.user_type_id==2">附件</tab-item>
        <tab-item v-if="userInfo.user_type_id==2">投票</tab-item>
      </tab>
      <div class="float_box">
        <span class="title_detail">发送到</span>
        <div class="DropBox" @click="show=true;flag=0">
          <span class="DropBoxShow">{{ checkboxShow }}<span v-if="checkboxList.length>2">等</span>{{checkboxList.length}}个圈子</span>
          <span id="triangle-down" ></span>
        </div>
        <div class="tab-swiper">
          <x-textarea class="moment_textarea borderRadius boxShadowGray" :placeholder="textareaCfg.placeholder"
                      :height="textareaCfg.height" v-model="content">
          </x-textarea>
        </div>
        <div class="tab-swiper vux-center" v-show="index==0">
          <m-choose   class="chooseView"
                      ref="mPubCommonChooseView0"
                      :_subComponents="m_choose._subComponents"
                      :_mAudio="m_choose._mAudio"
                      :_mImg="m_choose._mImg"
                      :_cFile="m_choose._cFile"
                      :_mVideo="m_choose._mVideo"
                      @on-shouldShowH5Record="shouldShowH5Record"
                      @on-mAudioChange="audioChanged"
                      @on-mImgChange="imgChanged"
                      @on-cFileChange="fileProgressed"
                      @on-mVideoChange="videoChanged">
          </m-choose>
        </div>

        <div class="tab-swiper vux-center" v-show="index==1">
          <m-choose   ref="mPubCommonChooseView1"
                      class="chooseView"
                      :_subComponents="m2_choose._subComponents"
                      :_mAudio="m2_choose._mAudio"
                      :_mImg="m2_choose._mImg"
                      :_cFile="m2_choose._cFile"
                      :_mVideo="m2_choose._mVideo"
                      @on-shouldShowH5Record="shouldShowH5Record"
                      @on-mAudioChange="audioChanged"
                      @on-mImgChange="imgChanged"
                      @on-cFileChange="fileProgressed"
                      @on-mVideoChange="videoChanged">
          </m-choose>
        </div>

        <div class="tab-swiper vux-center" v-show="index==2">
          <m-choose   ref="mPubCommonChooseView2"
                      class="chooseView"
                      :_subComponents="m3_choose._subComponents"
                      :_mAudio="m3_choose._mAudio"
                      :_mImg="m3_choose._mImg"
                      :_cFile="m3_choose._cFile"
                      :_mVideo="m3_choose._mVideo"
                      @on-shouldShowH5Record="shouldShowH5Record"
                      @on-mAudioChange="audioChanged"
                      @on-mImgChange="imgChanged"
                      @on-cFileChange="fileProgressed"
                      @on-mVideoChange="videoChanged">
          </m-choose>
        </div>

        <div id="vote" class="tab-swiper vux-center" v-if="index==3">
          <span class="single_vote">单选投票，最多添加10个选项，每个选项限输入30个字</span>
          <div class="input_area" v-for="(item,index) in input_list">
            <img src="../../components/m-img/icon-delete.png" @click="closeInput(index)">
            <input type="text" :placeholder="item.name" v-model="item.value" class="select_input boxShadowGray">
          </div>
          <div class="add" @click="addInput()" v-if="add_show">
            <img src="../../images/icon-add.png" alt="">
            <span>添加选项</span>
          </div>
          <datetime class="endTime boxShadowGray" v-model="time_show" format="YYYY-MM-DD HH:mm" title="结束时间"></datetime>
        </div>

        <!--发布和取消-->
        <div class="btns boxShadowGray clb">
          <div class="item-btn fl" @click="goBack()">取消</div>
          <div class="item-btn fl" style="color: #4085ff;" @click="publish(index)">发布</div>
        </div>
      </div>

      <!--下拉弹框-->
      <div class="div_select boxShadowGray" v-if="show">
        <ul @click="flag=0">
          <li class="border_bottom" v-if="$route.query.publish_type==2" @click="is_visible_for_teacher=(is_visible_for_teacher==1?0:1)">
            <div class="div_select_view">
              <img class="left" src="../../components/m-personChoose/images/icon_choosed.png" v-if="is_visible_for_teacher==1"/>
              <img class="left" src="../../components/m-personChoose/images/icon_choosed_not.png" v-else/>
              <span class="left" style="color: #4685ff;">请假仅被教师可见</span>
            </div>
          </li>
          <li class="border_bottom" v-if="$route.query.publish_type==1">
            <div class="div_select_title">通讯录人员可见</div>
            <div class="div_select_view">
              <img class="left" src="../../components/m-personChoose/images/icon_choosed.png" />
              <span class="left" style="line-height: 1rem">个人风采</span>
            </div>
          </li>
          <li class="border_bottom" v-if="$route.query.publish_type==1" @click="pushCheckBox(ClassList[0].state,0)">
            <div class="div_select_title" >学校内人员可见</div>
            <div class="div_select_view">
              <img class="left" src="../../components/m-personChoose/images/icon_choosed.png" v-if="ClassList[0].state"/>
              <img class="left" src="../../components/m-personChoose/images/icon_choosed_not.png" v-else/>
              <span class="left">学校风采</span>
            </div>
          </li>
          <li v-for="(item,index) in this.ClassList" v-if="index>0" @click="pushCheckBox(item.state,index)">
            <div class="div_select_title" v-if="index==1">班级内学生和家长可见</div>
            <div class="div_select_view">
              <img class="left" src="../../components/m-personChoose/images/icon_choosed.png" v-if="item.state"/>
              <img class="left" src="../../components/m-personChoose/images/icon_choosed_not.png" v-else/>
              <span class="left">{{ item.class_name }}</span>
            </div>
          </li>
        </ul>
      </div>
    </div>
    <!--modify by perry-->
    <popup v-model="needRecordAudio" height="12.5rem" @on-hide="popupHide" is-transparent >
      <recordView ref="audioView" @on-startRecord="startRecord" @on-stopRecord="stopRecord" @on-makeSure="makeSure" @on-cancleClick="cancelClick"></recordView>
    </popup>
  </div>
</template>

<script type="text/ecmascript-6">
  import HeadTop from '@/components/Head.vue'
  import MChoose from '../../components/m-choose/index'
  import XTextarea from 'vux/src/components/x-textarea/index.vue'
  import { Tab, TabItem, Swiper, SwiperItem, Datetime } from 'vux'
  import { getUserInfo, getClassList, publish_basic, publish_vote, publish_dayoff }  from '../../service/getData.js'
  import popup from 'vux/src/components/popup/index.vue'
  import recordView from '../../components/m-recordAudioView/index.vue'

  export default {
    data () {
      return {
        needRecordAudio:false,
        head:{
          icon: 'return',
          title: this.$route.query.publish_type==1 ? '发风采' : '发请假',
          more: false
        },
        userInfo: {},
        textareaCfg: {
          placeholder: '请输入你想发送的内容',
          height: 150,
        },
        m_choose: {
          _cFile:{
            popupBtn:false,
            showDelete:false
          },
          _subComponents: ['m-audio','m-img'],
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
        m2_choose: {
          _cFile:{
            popupBtn:false,
            showDelete:false
          },
          _subComponents: ['m-audio','m-video'],
          _mAudio: {
            url: 'voice_url'
          },
          _mImg: {
            maxCount: 9,
            url:'origin_image_url',
          },
          _mVideo: {
            popupBtn:true,
          },
        },
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
        nav: 1,
        index: 0,
        navArr:[],
        show:false, //下拉菜单
        flag:1,
        checkboxList:this.$route.query.publish_type==1 ? ['个人风采'] : [],   //存放已选的list
        checkboxShow:this.$route.query.publish_type==1 ? '个人风采' : '',
        ClassList:[{"class_id": -1, "class_name":'学校风采',"state":false}],
        voice_ids:['','',''],
        image_ids:['','',''],
        video_ids:['','',''],
        file_ids:['','',''],
        moment_type:'', //动态类型 '0'照片，'1'视频，'2'附件
        content:'',//textArea内容
        time:'',       //当前时间
        time_show:'', //显示时间
        input_list:[{name:'选项1',value:''},{name:'选项2',value:''}],
        add_show:true,
        is_visible_for_teacher: 1,
      }
    },
    components: {
      HeadTop,
      Tab,
      TabItem,
      Swiper,
      SwiperItem,
      MChoose,
      XTextarea,
      Datetime,
      recordView,
      popup,
    },
    created(){
      this.getUserInfo();
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

      //获取用户基本信息
      async getUserInfo () {
        let res = await getUserInfo('','','');
        if (res.c == 0) {
          this.userInfo = res.d;
        } else {
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          })
        }
      },

      //获取本人相关班级
      async init_data(){
      	//获取时间
        this.time = this.CurentTime();
        this.time_show = this.time.substring(0,this.time.length-3);
        let res = await getClassList();
        for (let i=0;i<res.d.length;i++){
        	this.ClassList.push({"class_id": res.d[i].class_id, "class_name": res.d[i].class_name,"state":false})
        }
      },

      //取消下拉框
      detail_all(){
         if (this.flag ==1){
    			this.show = false
         }
         this.flag = 1
       },

      //添加input框
      addInput(){
        if(this.input_list.length<10){
      		//小于等于10个选项
          this.input_list.push({name:'选项'+(this.input_list.length+1),value:''})
        }else{
        	alert("最多添加10个选项")
           this.add_show = false;
        }
      },

      //删除input框
      closeInput(index){
      	if(this.input_list.length>2){
          this.add_show = true;
      		this.input_list.splice(index,1);
          for (let i=0;i<this.input_list.length;i++){
            this.input_list[i].name='选项'+(i+1)
          }
        }else{
          this.$vux.toast.show({
            type: 'text',
            text: "最少需要2个选项"
          })
        }
      },

      //下拉框中单选框的处理
      pushCheckBox(state,index){
        //注意此时的index 并不是你点玩后的状态  而是你点击之前的状态
        //所以判断是反过来的  手机与pc是相反的！！！
        this.checkboxList=this.$route.query.publish_type==1 ? ['个人风采'] : [];   //存放已选的list
        this.checkboxShow='';
        if(state == true){
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

      //接受文件的数据
      fileProgressed(data){
        this.file_ids[this.index]="";
        //this.file_ids[this.index]=[];
        if(data){
          for (let i = 0 ; i < data.length; i++){
              this.file_ids[this.index] += data[i].file_id +',';
          }
          this.file_ids[this.index] = this.file_ids[this.index].slice(0,this.file_ids[this.index].length-1);
        }
        this.file_ids[this.index] = file_ids;
      },
      //图片
      imgChanged(data){
        this.image_ids[this.index]="";
        if(data){
          for (let i = 0 ; i < data.length; i++){
              this.image_ids[this.index] += data[i].image_id +',';
          }
          this.image_ids[this.index] = this.image_ids[this.index].slice(0,this.image_ids[this.index].length-1);
        }
      },
      //语音
      audioChanged(data){
        this.voice_ids[this.index]="";
        if(data){
          for (let i = 0 ; i < data.length; i++){
            this.voice_ids[this.index] += data[i].voice_id +',';
          }
          this.voice_ids[this.index] = this.voice_ids[this.index].slice(0,this.voice_ids[this.index].length-1);
        }
      },
      //视频
      videoChanged(data){
      	//视频只有一个 data为对象
      	this.video_ids[this.index]="";
        if(data){
          this.video_ids[this.index] += data.video_id;
        }
      },

      //提交
      async publish(type){
        let class_ids = '';
        let is_publish_to_school = 0;
        for (let i=1;i<this.ClassList.length;i++){
        	if(this.ClassList[i].state == true){
            class_ids += this.ClassList[i].class_id +',';
          }
        }
        class_ids = class_ids.slice(0,class_ids.length-1);

        if (this.ClassList[0].state == true){
          is_publish_to_school = 1
        }else{
        	is_publish_to_school = 0
        }
        if (this.$route.query.publish_type==2) {
          //请假
          if (this.content == '') {
            this.$vux.toast.show({
              type: 'text',
              text: '请输入动态文字内容！'
            })
          } else if (class_ids.length == 0) {
            this.$vux.toast.show({
              type: 'text',
              text: '请选择发送到的班级！'
            })
          } else {
            this.$vux.loading.show({
              text: '发布中'
            });
            let res = await publish_dayoff(this.content,this.voice_ids[this.index],this.image_ids[this.index],this.is_visible_for_teacher,class_ids);
            this.$vux.loading.hide();
            if (res.c == 0){
              this.goBack();
            } else{
              this.$vux.toast.show({
                type: 'text',
                text: res.m
              })
            }
          }
        } else if (type == 3){
        	//投票
          if (this.content == '') {
            this.$vux.toast.show({
              type: 'text',
              text: '请输入动态文字内容！'
            })
          } else if (this.time_show == '') {
            this.$vux.toast.show({
              type: 'text',
              text: '请输入投票截止时间！'
            })
          } else {
            let branches = [];
            for (let j=0;j<this.input_list.length;j++){
              branches.push({"branch":this.input_list[j].value, "sort":j})
            }
            this.$vux.loading.show({
              text: '发布中'
            });
            let res = await publish_vote(this.content,this.content,this.time_show,JSON.stringify(branches),is_publish_to_school,class_ids);
            this.$vux.loading.hide();
            if (res.c == 0){
              this.goBack();
            } else{
              this.$vux.toast.show({
                type: 'text',
                text: res.m
              })
            }
          }
        }else{
        	//其他3类
          if (this.content == '') {
            this.$vux.toast.show({
              type: 'text',
              text: '请输入动态文字内容！'
            })
          } else {
            this.$vux.loading.show({
              text: '发布中'
            });
          	let res = await publish_basic(this.content,type,this.voice_ids[this.index],this.image_ids[this.index],this.video_ids[this.index],this.file_ids[this.index],is_publish_to_school,class_ids);
            this.$vux.loading.hide();
            if (res.c == 0){
              this.goBack();
            } else{
              this.$vux.toast.show({
                type: 'text',
                text: res.m
              })
            }
          }
        }
      },

      //获取当前时间
      CurentTime(){
        let now = new Date();
        let year = now.getFullYear();       //年
        let month = now.getMonth() + 1;     //月
        let day = now.getDate();            //日
        let hh = now.getHours();            //时
        let mm = now.getMinutes();          //分
        let ss = now.getSeconds();         //秒
        let clock = year + "-";
        if(month < 10)
            clock += "0";
        clock += month + "-";
        if(day < 10)
            clock += "0";
        clock += day + " ";
        if(hh < 10)
            clock += "0";
        clock += hh + ":";
        if (mm < 10)
        	  clock += '0';
        clock += mm + ":";
        if (ss < 10)
        	  clock += '0';
        clock += ss;
        return(clock);
      },
      // modify by perry
      shouldShowH5Record(shouldShow) {
        //alert("shouldShowH5Record" + shouldShow);
        this.needRecordAudio = shouldShow;
      },
      popupHide() {
        let str = 'mPubCommonChooseView' + this.index;
        this.$refs[str].execAudioAction('stopRecord',null);
        this.$refs.audioView.cancleRecord();
      },
      startRecord() {
        let str = 'mPubCommonChooseView' + this.index;
        this.$refs[str].execAudioAction('startRecord',null);
        // alert('startRecord' + this.$refs[str]);
      },
      stopRecord() {
        let str = 'mPubCommonChooseView' + this.index;
        this.$refs[str].execAudioAction('stopRecord',null);
        // alert('stopRecord' + this.$refs[str]);
      },
      makeSure(time) {
        let str = 'mPubCommonChooseView' + this.index;
        this.$refs[str].execAudioAction('makeSure',time);
        // alert('makeSure' + this.$refs[str]);
        this.needRecordAudio = false;
      },
      cancelClick() {
        let str = 'mPubCommonChooseView' + this.index;
        this.$refs[str].execAudioAction('cancelClick',null);
        // alert('cancelClick' + this.$refs[str]);
        this.needRecordAudio = false;
      },
    },
    watch:{
    	//初始化数据 tab切换的时候清空数据
    	index:function () {

    	  this.needRecordAudio =false;
      	this.content='';
        this.checkboxList=this.$route.query.publish_type==1 ? ['个人风采'] : [];   //存放已选的list
        this.checkboxShow=this.$route.query.publish_type==1 ? '个人风采' : '';
        for (let i=0;i<this.ClassList.length;i++){
        	this.ClassList[i].state = false
        }
      }
    }
  }
</script>

<style scoped>
  .tab-swiper{
    margin: 0.75rem;
  }
  .moment_textarea{
    width: 100%;
    height: 10rem;
    border: 1px #f5f5f5 solid;
    border-radius: 4px;
    position: initial;
    margin: 0.75rem 0 1rem 0;
    font-size: 0.75rem;
    color: #f5f5f5;
  }
  .chooseView{
    margin-top: 4.5rem!important;
  }
  .float_box{
    position: fixed;
    width: 100%;
    overflow: scroll;
    bottom: 0;
    top: 86px;
  }
  .title_detail{
    display: inline-block;
    margin: 1.5rem 0.75rem 0 0.75rem;
    font-size: 0.75rem;
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
  .moment_img img{
    width:2rem;
    height:2rem;
  }
  .DropBox{
    display: inline-block;
  }
  .DropBoxShow{
    font-size: 0.75rem;
    color: #4685ff;
  }
  .DropBoxShow span {
    color: #4685ff;
  }
  .div_select{
    width: 14rem;
    position: absolute;
    top: 5.5rem;
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
  .input_area{
    position: relative;
  }
  .input_area img{
    width: 1rem;
    height: 1rem;
    position: absolute;
    top: 1rem;
    left: 16rem;
    background-color: #f5f5f5;
    border-radius: 0.5rem;
  }
  .add{
    width: 100%;
    margin-bottom: 1rem;
  }
  .add img{
    border: 1px #4685ff solid;
    margin-right: 0.5rem;
    width: 1rem;
    height: 1rem;
  }
  .add span{
    display: inline-block;
    vertical-align: text-top;
    color: #4685ff;
    font-size: 0.75rem;
  }
  .endTime{
    font-size: 0.75rem;
  }
  .single_vote{
    font-size: 0.5rem;
    color: #aaa;
  }
  .select_input{
    width: 80%;
    height: 2rem;
    margin: 0.5rem 0 1rem 0;
    padding: 0.25rem;
    -webkit-appearance: none;
    font-size: 0.85rem;
  }

  /*灰色虚边阴影*/
  .boxShadowGray{
    box-shadow: 0 0 16px 4px rgba(0, 0, 0, 0.08);
    -moz-box-shadow: 0 0 3px 3px rgba(0, 0, 0, 0.08);
    -webkit-box-shadow: 0 0 3px 3px rgba(0, 0, 0, 0.08);
  }
    /*蓝色虚边阴影*/
  .boxShadowBlue{
    box-shadow: 0 0 10px 1px rgba(70, 133, 255, 0.4);
    -moz-box-shadow: 0 0 10px 1px rgba(70, 133, 255, 0.4);
    -webkit-box-shadow: 0 0 10px 1px rgba(70, 133, 255, 0.4);
  }
</style>

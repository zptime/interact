<template>
  <div>
    <head-top :head="head">
      <img slot="left" src="../../images/icon-return.png" @click="goBack"/>
    </head-top>
    <div class="contentBox" v-cloak>
      <div class="fixed" v-if="user_type_id==2" :style="fixedTop('nav',0)">
        <div class="nav borderRadius clb">
        <span :class="{'active':navId==item.id}" v-for="item in navItem" @click="changeNav(item.id)">
          {{ item.item }}
        </span>
        </div>
      </div>
      <div class="search fixed" :style="fixedTop('search',2.5)" v-if="navId==1">
        <m-search :search="search"  @onsearch="mySearch"></m-search>
      </div>
      <div class="list" v-if="navId==1" :style="fixedTop('list',7.3)">
        <div class="item" v-for="(item,parentIndex) in list">
          <!--<div class="item-title clb" @click="isShow(parentIndex)" v-if="item.number>0">-->
          <div class="item-title clb" @click="isShow(parentIndex)">
            <span class="arrow left" :class="item.show?'':'rotate90'"></span>
            <span class="title left">{{ item.title }}</span>
            <span class="number right">{{ item.number }}</span>
          </div>
          <div v-for="(itemData,index) in filterData(item.data,parentIndex)" :class="item.show?'show':'hide'">
            <div class="item-detail clb" :class="{'item-border-none': (parentIndex==list.length-1 && index==item.data.length-1)}">
              <span class="other-all">
                <span class="avatar left">
                  <img :src="itemData.avatar" v-if="itemData.avatar">
                  <img src="../../images/icon-default-avatar.png" v-else>
                </span>
                <span class="username left">{{ itemData.username }}</span>
                <span class="desc left">{{ itemData.desc }}</span>
              </span>
              <span class="phone right" v-if="itemData.stu_relate_parent && itemData.stu_relate_parent.length>0">
                <img src="../../images/icon-arrow.png" class="right" @click="openParent($event)">
                <span class="parent right">
                  家长  ({{ itemData.stu_relate_parent.length }})
                </span>
              </span>
              <span class="phone right" v-else>
                <a :href="'tel:'+itemData.phone" v-if="itemData.phone!=''">
                  <img src="../../images/icon-phone.png">
                </a>
                <img class="right" src="../../images/icon-phone.png" @click="callPhone(itemData.phone)" v-else>
              </span>
            </div>
            <div class="item-parent" v-if="itemData.stu_relate_parent && itemData.stu_relate_parent.length>0">
              <div class="item-detail item-detail-parent clb" v-for="parent in itemData.stu_relate_parent">
                <span class="other-all">
                  <span class="avatar left">
                    <img :src="parent.avatar" v-if="parent.avatar">
                    <img src="../../images/icon-default-avatar.png" v-else>
                  </span>
                  <span class="username left">{{ parent.username }}</span>
                  <span class="desc left">{{ parent.desc }}</span>
                </span>
                <span class="phone right">
                  <a :href="'tel:'+parent.phone" v-if="parent.phone!=''">
                    <img src="../../images/icon-phone.png">
                  </a>
                  <img class="right" src="../../images/icon-phone.png" @click="callPhone()" v-else>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="list"  :style="fixedTop('list',4)" v-else>
        <cluster-list :clusterList="clusterList"></cluster-list>
      </div>
    </div>
  </div>
</template>

<script type="es6">
  import HeadTop from '@/components/Head.vue'
  import MSearch from '@/components/m-search/Search.vue'
  import ClusterList from '@/page/phone/ClusterList.vue'
  import global from '../../components/Global.vue'
  import { mapState,mapMutations } from 'vuex'
  import { getBookContact,getUserInfo,getBookCluster } from '../../service/getData.js'
  import nativeCommon from '../../config/nativeCommon.js'
  import {initializeEnv, exitCurApp} from '../../components/framework/serviceMgr.js'

  export default {
    data () {
      return {
        head:{
          icon: 'return',
          title: '通讯录',
          more: false
        },
        search:{//搜索框参数设置
          is_focus:false,
          search_txt:'',
          placeholder_txt:'请输入姓名',
        },
        backNative:{},//返回原生界面
        navId:1,//导航栏ID
        navItem:[{'item':'联系人','id':1},{'item':'小组','id':2}],
        list:[],//通讯录列表
        clusterList:[],//群组列表
        keyword:'',//搜索框关键字
        filterFlag:false,//是否启用筛选查询
      }
    },
    components: {
      HeadTop,
      MSearch,
      ClusterList,
    },
    computed:{
      ...mapState([
        'user_info',
        'user_type_id',
        'clazz_list',
        'nav_flag',
      ])
    },
    created(){
      initializeEnv(this);
      this.userInfo();
      this.initData();
      this.backNative = new nativeCommon();
    },
    methods:{
      ...mapMutations([
        'USER_INFO',
        'USER_TYPE_ID',
        'CLAZZ_LIST',
      ]),

      //fixed定位top设置
      fixedTop(name,top){
        if(global.showHead){//带头部head
          top += 2.1;
        }
        if(this.user_type_id!=2){//没有nav导航
          if(name=='list' || name=='search'){
            top -= 2.5;
          }
        }
        let styles = {
          'top':top+ 'rem'
        };
        return styles;
      },

      //获取用户基本信息 + 用户类型（1 学生 2 老师 4 家长）
      async userInfo(){
        if(this.nav_flag==2){
          this.navId = this.nav_flag;
        }
        let res = await getUserInfo('','','');
        if(res.c == 0){
          this.USER_INFO(res.d);
          this.USER_TYPE_ID(res.d.user_type_id);
          console.log(this.user_type_id);
          //this.initData();
        }else{
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          });
        }
      },

      //初始化数据
      initData(){
        this.$vux.loading.show({
          text: '加载中'
        });
        if(this.navId == 1){
          this.getContactList();
        }else{
          this.getClusterList();
        }
      },

      //获取通讯录列表信息
      async getContactList(){
        let res = await getBookContact();
        if(res.c == 0){
          this.list = [];
          if(res.d.family.length>0){
            this.list.push({
              "data": res.d.family,
              "title":'家庭',
              "name":'family',
              "number":res.d.family.length,
              "show":true
            });
          }
          if(res.d.teacher.length>0){
            let tmp = '同事';
            if(this.user_type_id==4){
              tmp = '老师';
            }
            this.list.push({
              "data": res.d.teacher,
              "title":tmp,
              "name":'teacher',
              "number":res.d.teacher.length,
              "show":true
            });
          }
          if(res.d.student.length>0){
            for(let i=0;i<res.d.student.length;i++){
              this.list.push({
                "data": res.d.student[i].students,
                "title":res.d.student[i].class_name,
                "name":'student',
                "number":res.d.student[i].students.length,
                "show":true
              });
            }
          }
          this.$vux.loading.hide();
        }else{
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          });
        }
      },

      //获取群组列表-只包括我创建的群组
      async getClusterList(){
        let res = await getBookCluster();
        if(res.c == 0){
          this.clusterList = res.d.created;
          this.CLAZZ_LIST(res.d.clazz);
          this.$vux.loading.hide();
        }else{
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          });
        }
      },

      goBack() {
        exitCurApp(this);
      },
      //搜索事件
      mySearch(){
        this.keyword = this.search.search_txt;
        this.filterFlag = true;
      },

      //前端-筛选过滤数据
      filterData(data,index){
        if(this.filterFlag){
          let returnVal = [];
          for(let i=0;i<data.length;i++){
            if(data[i].username.search(this.keyword)!=-1){
              returnVal.push(data[i]);
            }
          }
          this.list[index].number = returnVal.length;
          return returnVal;
        }else{
          return data;
        }
      },

      //详细列表-隐藏和显示
      isShow(index){
        this.list[index].show = !this.list[index].show;
      },

      //打电话操作-调用原生代码
      callPhone(){
        this.$vux.toast.show({
          type: 'text',
          text: '未存入手机号'
        });
      },

      //打开家人联系方式
      openParent(event){
        if (event || (event = window.event)) event.preventDefault();
        //获得target兼容型写法
        let cEle = (event.target || event.srcElement);
        let ele = cEle.parentNode.parentNode.nextElementSibling;
        if(cEle.className.indexOf('rotate180')!=-1){
          cEle.className='right';
          ele.style.display = "none";
        }else{
          cEle.className='right rotate180';
          ele.style.display = "block";
        }
      },

      changeNav(id){
        this.navId = id;
        this.search.search_txt = '';
        this.search.is_focus = false;
        this.initData();
      }
    }
  }
</script>

<style scoped>
  .contentBox{
    background-color: #fff;
    bottom:0;
  }
  .search{
    margin:1.5rem 0 1rem 0;
  }

  .list{
    position: fixed;
    width: 100%;
    background-color: #fff;
    /*top: 6.85rem;*/
    bottom: 0;
    z-index: 9;
    overflow-y: auto;
    -webkit-overflow-scrolling : touch;
  }

  .nav{
    width:10rem;
    text-align: center;
    margin: 1rem auto 0 auto;
    border: 1px solid #4685ff;
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

  .item .item-title{
    height: 2rem;
    line-height: 2rem;
    padding:0 0.75rem;
  }
  .item .item-title .arrow{
    display:inline-block;
    width:0;
    height:0;
    margin:0.8rem 0.5rem 0 0;
    border-style:solid;
    border-width:0.4rem;
    border-color:#a2c2ff transparent transparent transparent;
  }
  .rotate90{
    transform:rotate(-90deg);
    -ms-transform:rotate(-90deg); 	/* IE 9 */
    -moz-transform:rotate(-90deg); 	/* Firefox */
    -webkit-transform:rotate(-90deg); /* Safari 和 Chrome */
    -o-transform:rotate(-90deg); 	/* Opera */
    margin:0.6rem 0.4rem 0 0 !important;
  }
  .rotate180{
    transform:rotate(180deg);
    -ms-transform:rotate(180deg); 	/* IE 9 */
    -moz-transform:rotate(180deg); 	/* Firefox */
    -webkit-transform:rotate(180deg); /* Safari 和 Chrome */
    -o-transform:rotate(180deg); 	/* Opera */
  }
  .item .item-title .title{
    color:#444;
    font-size: 0.8rem;
  }
  .item .item-title .number{
    font-size: 0.6rem;
    color: #888;
  }
  .item .item-detail{
    margin:0 0.75rem;
    background-color: #fff;
    height:2.75rem;
    line-height:2.75rem;
    color:#444;
    font-size: 0.8rem;
    border-bottom:1px solid #eee;
  }
  .item .item-border-none{
    border-bottom: none !important;
  }
  .item-parent{
    display: none;
  }
  .item .item-detail-parent{
    background-color: #f5f5f5;
    padding: 0 0.75rem;
    margin: 0;
  }
  .item .item-detail .other-all{
    width:75%;
  }
  .item .item-detail .avatar img{
    margin-top:0.5rem;
    width:1.75rem;
    height:1.75rem;
    -webkit-border-radius: 0.9rem;
    -moz-border-radius: 0.9rem;
    -ms-border-radius: 0.9rem;
    -o-border-radius: 0.9rem;
    border-radius: 0.9rem;
  }
  .item .item-detail .phone{
    width:24%;
  }
  .item .item-detail .phone a{
    height: inherit;
    width: 100%;
    text-align: right;
    display: inline-block;
  }
  .item .item-detail .phone img{
    height:1rem;
    width:0.9rem;
    margin:0.9rem 0;
  }
  .item .item-detail span{
    display: inline-block;
    height: inherit;
  }
  .item .item-detail .username{
    font-size:0.8rem;
    color:#444;
    margin:0 0.5rem;
  }
  .item .item-detail .desc{
    font-size:0.6rem;
    color:#aaa;
  }
  .item .item-detail .parent{
    font-size:0.6rem;
    color:#aaa;
    margin-right:0.5rem;
  }
</style>

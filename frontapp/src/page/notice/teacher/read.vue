<template>
  <div>
    <head-top :head="head">
      <img slot="left" src="../../../images/icon-return.png"  @click="myback()"  />
    </head-top>
    <div class="contentBox" v-cloak >
      <div class="choose-list"  >
        <div class="nav borderRadius clb">
          <span :class="{'active':navId==item.id}" v-for="item in navItem" @click="changeNav(item.id)">
            {{ item.item }}
          </span>
        </div>

      </div>
      <div class="top-msg" v-if="false"  >
            <div class="fl" style="color: #888;font-size: 0.6rem;">总共有{{ rightlist.length }}人阅读此消息</div>
            <div   @click="allChoose()" class="fr" style="font-size: 0.6rem;color: #23d42e;">{{ checkVal }}</div>
      </div>
      <div class="readlist" style="height: 23rem;width:100%;overflow: scroll;position: fixed;left: 0;top:7.4rem;padding-bottom: 1.4rem;">
          <div v-if="navId==1" class="notread-list">
              <div class="item" v-for="(item,index) in leftlist"  @click=" toggleChoose(index)" >
                  <div class="item-img"><img  v-if="item.avatar !=''" :src="item.avatar" alt=""><img  v-if="item.avatar ==''" src="../../../images/icon-default-avatar.png" alt=""></div>
                  <div class="item-name">{{ item.username }}</div>
                  <div style="display: none;" class="item-right" :class="{ choosed : item.ischecked }"></div>
              </div>
          </div>
          <div v-if="navId==2" class="hasread-list">
              <div class="item" v-for="item in rightlist"   >
                  <div class="item-img"><img  v-if="item.avatar !=''" :src="item.avatar" alt=""><img  v-if="item.avatar ==''" src="../../../images/icon-default-avatar.png" alt=""></div>
                  <div class="item-name">{{ item.username }}</div>
              </div>
          </div>
      </div>
      <div class="fixbottom"  v-if="navId==1" @click="remindUnreadPerson()" >提醒当前未读人员</div>
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
import HeadTop from '@/components/Head.vue'
import { readList,remindUnreader } from '../../../service/getData.js'

export default {
    props:['notify_id'],
    name:'read',
    data () {
      return {
        head:{
          icon: 'return',
          title: '阅读次通知人员',
          more: false
        },
        navId:1,//导航栏ID
        navItem:[{'item':'未阅读人员','id':1},{'item':'已阅读人员','id':2}],
        classList:[],//班级数据列表
        groupList:[],//小组数据列表
        dataList:[],//数据列表
        chooseNum:0,//已选班级个数
        checkVal:'全选',//全选、取消全选文字
        showPage:false,//是否显示页面
        showList:false,//是否显示列表
        showTipNone:false,//是否显示无关联提示
        showPopup:false,//是否显示popup
        headTitle:'',//头部的title
        bulkData:'',//传递到子页的数据
        dataIndex:'',//传递到子页的数据序号
        leftlist:[],//左侧数据
        rightlist:[],//右侧数据
      }
    },
    components: {
        HeadTop,
     //   Toast
    },

    created(){
        let notify_id = this.notify_id;
        this.getReaderList(notify_id);
    },
    methods:{
      //导航栏切换
      changeNav(id){
        this.navId = id;
        this.chooseNum=0;
        this.checkVal='全选';
        this.showList = false;
      },
      async remindUnreadPerson(){
             let notify_id = this.notify_id;
             let res = await remindUnreader(notify_id);
             if(res.c==0){
                 this.$vux.toast.show({
                    text: '操作成功',
                     time:1000,
                 })
             }
        },
      allChoose(){
          if(this.checkVal=="全选"){
              this.checkVal = '取消全选'
              for(let i in this.leftlist){
                  this.leftlist[i].ischecked = true ;
              }
          }else{
              this.checkVal = '全选'
              for(let i in this.leftlist){
                  this.leftlist[i].ischecked = false ;
              }
          }


      },
      myback(){
        this.$emit("goback")
      },
      toggleChoose(index){
          for(let i in this.leftlist){
              if(i == index){
                  this.leftlist[i].ischecked = !this.leftlist[i].ischecked;
              }
          }
          this.leftlist = this.leftlist.concat([]);
      },
      async getReaderList(notify_id){
        let res = await readList(notify_id);
        this.leftlist = res.d.who_unread;
        this.rightlist = res.d.who_read;
        for(let i in this.leftlist){
            this.leftlist[i].ischecked=false;
        }
      },

    },
    watch:{
      chooseNum(val){
        if(val==this.dataList.length){
          this.checkVal = '取消全选';
        }else if(val==0){
          this.checkVal = '全选';
        }
      }
    }
  }
</script>

<style scoped>
/*  @import "./member.css"; */
.member{width:100%;text-align:left;}
.search{margin:1.5rem 0 1rem 0;}
.left{float:left;}
.right{float:right;}
.hide{display: none;}
.show{display: block;}
.clb:after{content:'';display:block;clear:both;}
.action-title{font-size:0.6rem;color:#666;}
.action-del{color:#fd5555;}
/*边框弧度-4px*/
.borderRadius{
  -webkit-border-radius: 4px;
  -moz-border-radius: 4px;
  -ms-border-radius: 4px;
  -o-border-radius: 4px;
  border-radius: 4px;
}
/*蓝色虚边阴影*/
.boxShadowBlue{
  box-shadow: 0 0 10px 1px rgba(70, 133, 255, 0.4);
  -moz-box-shadow: 0 0 10px 1px rgba(70, 133, 255, 0.4);
  -webkit-box-shadow: 0 0 10px 1px rgba(70, 133, 255, 0.4);
}
/*水平垂直居中*/
.middleCenter{
  text-align: center;
  display:flex;/*Flex布局*/
  display: -webkit-flex; /* Safari */
  justify-content: center;/*实现水平居中*/
  align-items:center; /*实现垂直居中*/
}

.contentBox{
background-color: #fff;
bottom:0;
}
.fl{float: left;}
.fr{float: right;}
.readlist{padding:0 0.75rem;}
.readlist .item{height: 2.75rem;line-height: 2.75rem;border-bottom: solid 1px #eee;}
.readlist .item .item-right{float: right;width: 1.25rem;height: 1.25rem;border-radius: 50%;overflow: hidden;margin-top: 0.75rem;background: url("../../../images/icon-not-selected.png")no-repeat;background-size: 100% 100%;}
.readlist .item .item-right.choosed{background-image: url("../../../images/icon-selected.png")}
.readlist .item .item-img{width: 1.75rem;height: 1.75rem;border-radius: 50%;overflow: hidden;float: left;margin-top: 0.5rem;margin-right: 0.5rem;}
.readlist .item .item-img img{width: 100%;}
.readlist .item .item-name{font-size: 0.8rem;color: #444;float: left;}
.top-msg{height: 2.75rem;line-height: 2.75rem;padding: 0 0.75rem;background: #fafafa;}
.fixbottom{width: 10rem;height: 2rem;text-align: center;line-height: 2rem;font-size: 0.75rem;color: #FFFFFF;background: #ff9e35;border-radius: 1rem;position: fixed;bottom: 1rem;transform: translateX(-50%);left: 50%;}

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

  .tip{
    font-size: 0.6rem;
    color:#aaa;
    margin:1.5rem 0.75rem 0.5rem 0.75rem;
  }

  .list{
    position: fixed;
    width: 100%;
    background-color: #fff;
    top: 7.4rem;
    bottom: 4rem;
    z-index: 9;
    overflow-y: auto;
    -webkit-overflow-scrolling : touch;
  }

  .list .username{
    margin-left:0.75rem !important;
  }
  .list .item-detail .number{
    font-size: 0.75rem;
    color:#aaa;
  }
  .list .item-detail .toggle img{
    height: 0.85rem;
    width: 0.85rem;
    margin: 0.95rem 0 0.95rem 0.5rem;
  }
</style>

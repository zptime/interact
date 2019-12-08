<template>
 <div>
   <head-top :head="head"></head-top>
   <div class="contentBox" v-cloak>
     <div class="headView">
       <span :style="{flex:'1'}"></span>
       <img class="headImgView" src="../../images/icon_jiaXiaoHuDong.png"/>
       <span :style="{flex:'1'}"></span>
     </div>
     <div class="content" v-for="item in showData">
       <div>
         <divider class="dividerLine" v-if="item.server_title.length > 0">{{item.server_title}}</divider>
       </div>
       <div class="modualItems">
          <div class="itemInModual" v-for="(subItem,index) in item.moduals" :style="getMargin(index)">
            <div class="itemContent">
              <span :style="{color:'#fafafa'}">空格</span>
              <img src="subItem.server_icon_url"/>
              
              <span>{{subItem.server_item_name}}</span>
            </div>
          </div>
       </div>
     </div>
   </div>

 </div>
</template>

<script>
    import {getUserInfo,serviceList} from '../../service/getData.js'
    import HeadTop from '@/components/Head.vue'
    import Divider from 'vux/src/components/divider/index.vue'

    export default {
        name: "home-page",
        components:{
          HeadTop,
          Divider,
        },

        data(){
          return {
            itemWidth:0,
            itemHeight:0,
            itemSpace:0.75,//item间距
            lineSapce:1,//item 行间距
            showData:[],
            //只判断老师 家长
             isTeacher:false,
              head:{
                icon: 'return',
                title: '互动系统',
                more: false
              },
          }
        },
        methods:{
          getMargin(index){
            let width = 5.5;//item的宽度
            let screenWidth = window.document.body.clientWidth/20;
            let marginLeft = (screenWidth - 3 *width - 2 * 0.75 - 2)/2;

            while (index - 3 >= 0){
              index -= 3;
            }
            //第几列 - 1
            let colum = index ;
            return {
              marginLeft:colum == 0 ? '0.75rem' : marginLeft + 'rem',
            }

          },

          async getUserInfo(){
            let res = await getUserInfo();
            if (res.c == 0){
              let user_type_id = res.d.user_type_id;
              if(!user_type_id) return;
              //1 学生 2 老师 4 家长
              if (2 == user_type_id){
                  this.isTeacher = true;
              }else if(4 == user_type_id){
                  this.isTeacher = false;
              }else {
                //身份不对
              }
            }
          },
          initData(){
            let arr = [];
            for(let i =0;i< 5;i++){
              let obj = {
                "server_title":"string",//所属区域 行政管理等
                "server_icon_url":"string",//图标
                "server_goPath":"string",//点击跳转的url
                "server_item_name":i,//模块的名字

                "service_code": "string",
                "service_domain": "string",
                "login_url": "string",
                "logout_url": "string",
                "service_is_heartbeat": "string",
                "service_heartbeat_url": "string",
                "service_hearbeat_interval": "string",
                "para": "string"
              };
              arr.push(obj);
            }
            let arrobj = {};
            arrobj.moduals = arr;
            arrobj.server_title = '家校互动';
            this.showData.push(arrobj);
          },
        },
        created(){
          this.initData();

        }
    }
</script>

<style scoped>
  .dividerLine {width: 60%;margin-left: 20%;font-size: 0.75rem;margin-top: 1.5rem;}
  .headView {display: flex;flex-flow:row;position: relative;margin-top:1.5rem;}
  .headImgView{width:225px;height: 60px;}
  .modualItems {top:1rem;width: 100%;display: flex;flex-flow: row wrap;}
  .modualItems .itemInModual {background-color: #fafafa;width: 5.5rem;height: 5.5rem;margin-top: 1rem;}
  .itemContent {display: flex;flex-flow: column;}
  .itemContent img{height: 2.5rem;width: 2.5rem;margin-left: 1.5rem;}
  .itemContent span {flex: 1;text-align: center;color: #444444;}
</style>


/*
{
"server_title":"string",//所属区域 行政管理等
"server_icon_url":"string",//图标
"server_goPath":"string,"//点击跳转的url
"server_item_name":"string",//模块的名字

"service_code": "string",
"service_domain": "string",
"login_url": "string",
"logout_url": "string",
"service_is_heartbeat": "string",
"service_heartbeat_url": "string",
"service_hearbeat_interval": "string",
"para": "string"
}
*/

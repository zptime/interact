<template>
  <div>
    <head-top :head="head">
        <img slot="left" src="../../../images/icon-return.png" @click="goBack"/>
    </head-top>
    <div class="contentBox" style="height: 100%;"   v-cloak >
    <div style="width: 100%;height: 2.25rem;position: fixed;top: 2.6rem;left: 0;">
        <search :search="search"  @onsearch="blursearch()"   ></search>
    </div>

    <div style="position: fixed;left: 0;top:5.85rem;width: 100%;height: 24rem;">
         <Scroll :on-refresh="onRefresh" :on-infinite="onInfinite" >
                    <div style="overflow: scroll;padding: 0 0.75rem;background: #FFFFFF;padding-bottom: 1rem;" >
                        <div v-for="item in listdata"  @click="go_detail(item.notify_id,index)" class="item"   :class="{ p2rem : showbottom }" >
                            <div v-if="showbottom" class="notselect" :class="{ hasselect : item.isselect }"  @click.stop=" item.isselect = !item.isselect; " ></div>
                            <div class="img-box" :class=" { l2rem : showbottom }"   ><img v-if="avatar !='' "   :src="avatar" alt=""><img v-if="avatar =='' "   src="../../../images/icon-default-avatar.png" alt=""></div>
                            <div class="item-content">
                                <div class="item-top"><span class="item-type">{{ item.type_desc }}</span><span v-if="false"    class="item-name">{{ item.receiver_brief.length>10 ? ( item.receiver_brief.substring(0,10)+'..') : item.receiver_brief }}</span><span class="item-time">{{ item.create_time.substring(10) }}</span></div>
                                <div class="item-txt">{{ item.content }}</div>
                            </div>
                        </div>
                        <div v-for="(item,index) in downdata"  @click="go_detail(item.notify_id)" class="item" :class="{ p2rem : showbottom }" >
                            <div v-if="showbottom" class="notselect" :class="{ hasselect : item.isselect }"  @click.stop=" item.isselect = !item.isselect; " ></div>
                            <div class="img-box" :class=" { l2rem : showbottom }"   ><img v-if="avatar !='' "   :src="avatar" alt=""><img v-if="avatar =='' "   src="../../../images/icon-default-avatar.png" alt=""></div>
                            <div class="item-content">
                                <div class="item-top"><span class="item-type">{{ item.type_desc }}</span><span v-if="false" class="item-name">{{ item.receiver_brief.length>10 ? ( item.receiver_brief.substring(0,10)+'..') : item.receiver_brief }}</span><span class="item-time">{{ item.create_time.substring(10) }}</span></div>
                                <div class="item-txt">{{ item.content }}</div>
                            </div>
                        </div>
                    </div>
         </Scroll>
    </div>
        <div class="hover-publish" v-if="index==0&&!showdialog&&!showbottom"  @click="showdialog=true;"></div>
        <div class="fix-bottom" v-if="showbottom">
            <div @click="chooseAll()">{{ chooseAllTxt }}</div>
            <div class="b-left"  @click="deleteItem()">删除所选</div>
            <div class="b-left"  @click="showbottom=false;">取消</div>
        </div>
        <div >
          <x-dialog  hide-on-blur    :dialog-style="{ 'background':'none'}"      v-model="showdialog" class="dialog-extend clb" >
              <div class="d-inner">
                    <div class="dialog-item" @click="go_send_notice('work')"  ><div class="item-txt">作业通知</div><div class="bg-zytz bg_work"></div></div>
                    <div class="dialog-item" @click="go_send_notice('class')" ><div class="item-txt"   >班级通知</div><div class="bg-zytz bg_class"></div></div>
             <!--     <div class="dialog-item"><div class="item-txt">已发通知</div><div class="bg-zytz bg_hadsend"></div></div>   -->
                    <div class="dialog-item" @click="show_bottom()" ><div class="item-txt"  >编辑</div><div class="bg-zytz bg_edit"></div></div>
              </div>
          </x-dialog>
        </div>
    </div>
  </div>
</template>
<style scoped>
    .dialog-extend{}
    .dialog-item{height: 2.25rem;width: 6rem;background: none;margin-top: 1rem;}
    .dialog-item .bg-zytz{width: 2.25rem;height: 2.25rem;border: solid 2px #4685ff;float: right;box-sizing: border-box;border-radius: 50%;background-size:100% 100%;background-repeat: no-repeat;}
    .navitems{height: 2rem;margin-bottom: 0.2rem;}
    .navitems .item-nav{width: 50%;height: 2rem;float: left;text-align: center;line-height: 2rem;position: relative;}
    .navitems .item-nav.active::after{content: "";display: block;position: absolute;left: 50%;bottom: 0;width: 40%;height: 0.2rem;background: #308ce3;transform: translateX(-50%)}
    .item{padding: 0.5rem 0;width: 100%;box-sizing: border-box;position: relative;height: 3.25rem;border-bottom: solid 1px #f1f1f1;background: #FFFFFF;}
    .item .img-box{position: absolute;left: 0rem;top: 0.5rem;width: 2.25rem;height: 2.25rem;border-radius: 50%;overflow: hidden;border: solid 1px #eeeeee;}
    .item .img-box img{display: block;width: 100%;height: 100%;border-radius: 50%;}
    .item .item-content{padding-left: 2.6rem;line-height: 1.2rem;}
    .item .item-top{position: relative;}
    .item .item-top .item-time{position: absolute;top: 0;right: 0;color: #aaa;font-size: 0.6rem;}
    .item .item-txt{font-size: 0.6rem;color: #666;width: 100%;overflow: hidden;text-overflow: ellipsis;white-space: nowrap;line-height: 0.8rem;}
    .item .item-type {color: #000;font-size: 0.8rem}
    .item .item-name{font-size: 0.8rem;color: #000;}
    .vux-center{line-height: 5rem;text-align: center;}
    .item-box{padding: 1.5rem 0.8rem;background: #FFFFFF;}
    .hover-publish{width: 3rem;height: 3rem;border-radius: 50%;overflow: hidden;position: fixed;bottom: 2rem;right: 1rem;background: url("../../../images/plus.png")no-repeat center;background-size: 100% 100%;}
    .d-inner{width: 6rem;height: auto;position: absolute;right: 0rem;bottom:-14rem;}
    .dialog-item .item-txt{float: left;width: 3rem;text-align: right;line-height: 2.25rem;color: #FFFFFF;font-size: 0.6rem;}
    .bg_work{background-image: url("../../../images/work.png"); }
    .bg_class{background-image: url("../../../images/class.png"); }
    .bg_hadsend{background-image: url("../../../images/hadsend.png"); }
    .bg_edit{background-image: url("../../../images/edit.png"); }
    .fix-bottom{height: 2.2rem;width: 100%;box-sizing: border-box;position: fixed;background: #fff;left: 0;bottom: 0;text-align: center;line-height: 2.2rem;color: #FFFFFF;font-size: 0.8rem;border-top: solid 1px #d7d7d7;}
    .fix-bottom div{float: left;width: 33%;box-sizing: border-box;color: #4685ff;}
    .b-left{border-left: solid 1px #d7d7d7;}
    .p2rem{padding-left: 2rem}
    .item .l2rem{left: 2rem;}
    .notselect{position: absolute;top: 1rem;left: 0rem;width: 1.25rem;height: 1.25rem;background: url("../../../images/notselect.png") no-repeat center center ;border-radius: 50%;background-size: 100% 100%; }
    .hasselect{position: absolute;top: 1rem;left: 0rem;width: 1.25rem;height: 1.25rem;background: url("../../../images/hasselect.png") no-repeat center center ;border-radius: 50%;background-size: 100% 100%; }
</style>
<script type="text/ecmascript-6">
  import HeadTop from '@/components/Head.vue'
  import Search from '@/components/m-search/Search.vue'
  import Scroll from '@/components/m-scroll/scroll.vue'
  import nativeCommon from '../../../config/nativeCommon.js'
  import { Tab, TabItem,Swiper, SwiperItem ,Confirm ,TransferDomDirective as TransferDom ,Actionsheet,XDialog, } from 'vux'
  import { getTeacherNoticeList , deleteNotice,getMyInfo  }  from '../../../service/getData.js'
  import {initializeEnv, exitCurApp} from "../../../components/framework/serviceMgr.js"
  export default {
    directives: {
        TransferDom
    },
    data () {
      return {
        head:{
          icon: 'return',
          title: '通知消息',
          more: false
        },
        search:{
          is_focus:false,
          search_txt:'',
          placeholder_txt:'搜索',
        },
        backNative:{},//返回原生界面
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
        avatar:'',
        showdialog:false,
        showbottom:false,
        chooseAllTxt:'全选',
          counter : 1, //默认已经显示出15条数据 count等于一是让从16条开始加载
          num : 10,  // 一次显示多少条
          pageStart : 0, // 开始页数
          pageEnd : 0, // 结束页数
          listdata: [], // 下拉更新数据存放数组
          downdata: []  // 上拉更多的数据存放数组
      }
    },
    methods:{
        clickcall(key){
            alert("you just click the "+ key);
            console.log(this.menus2[key])
        },
        goBack() {
          exitCurApp(this);
         },
        async deleteItem(){
            //do something
            let arr = [];
            let newlistarr = [];
            let newdownarr = [];
            for(let i in this.listdata){
                if(this.listdata[i].isselect){
                    arr.push(this.listdata[i].notify_id)
                }else{
                    newlistarr.push(this.listdata[i]);
                }
            }
            for(let i in this.downtdata){
                if(this.downdata[i].isselect){
                    arr.push(this.downdata[i].notify_id)
                }else{
                    newdownarr.push(this.listdata[i]);
                }
            }
            let notify_ids = arr.join(',');
            this.$vux.loading.show();
            let res = await deleteNotice(notify_ids);
            this.listdata = newlistarr;
            this.downdata = newdownarr;
            this.$vux.loading.hide();
            this.showbottom=false;
        },
        show_bottom(){
            this.showbottom= true ;
            this.showdialog=false;
        },
        chooseAll(){
            if(this.chooseAllTxt=="全选"){
                this.chooseAllTxt="全部取消"
                for(let i in this.listdata){
                    this.listdata[i].isselect = true ;
                };
                for(let i in this.downdata){
                    this.downdata[i].isselect = true ;
                }
            }else{
                this.chooseAllTxt="全选"
                for(let i in this.listdata){
                    this.listdata[i].isselect = false ;
                };
                for(let i in this.downdata){
                    this.downdata[i].isselect = false ;
                }
            }
        },
        go_send_notice(type){
            this.$router.push({ path: "/m/notice/teacher/noticeSend" , query: { type: type } });
        },
        go_detail(notify_id){
            if(this.showbottom){
                for(let i in this.listdata){
                    if(this.listdata[i].notify_id==notify_id){
                            this.listdata[i].isselect = ! this.listdata[i].isselect;
                            return;
                    }
                };
                for(let i in this.downdata){
                    if(this.downdata[i].notify_id==notify_id){
                            this.downdata[i].isselect = ! this.downdata[i].isselect;
                            return;
                    }
                }
            }
            this.$router.push({ path: "/m/notice/teacher/noticeDetail" , query: { notify_id: notify_id } });
        },
        async getList(rows){
            let res = await getTeacherNoticeList(rows,this.search.search_txt,'');
            let arr = [];
            if(res.c==0){
                arr = res.d.data_list;
                for(let i in arr){
                    arr[i].isselect = false;
                }
                this.listdata = arr;
            }
            if(arr.length<10){
                if(this.listdata.length<10){
                    this.$el.querySelector('.load-more').style.display = 'none';
                }else{
                    this.$el.querySelector('.load-more').style.display = 'flex';
                }
            }
            return res ;
        },
        async onRefresh(done){
            let res = await getTeacherNoticeList(10,this.search.search_txt,'');
            let arr = res.d.data_list ;
            for(let i in arr){
                arr[i].isselect = false;
            }
            if(res.c==0){
               this.listdata = arr;
            }
            done();//请求完成执行done
        },
        async onInfinite(done){
          let last_id='';
          if(this.downdata.length>0){
              last_id = this.downdata[this.downdata.length-1].notify_id;
          }else{
              last_id = this.listdata[this.listdata.length-1].notify_id;
          }
          let res = await getTeacherNoticeList(10,this.search.search_txt,last_id);
          let arr = res.d.data_list;
          for(let i in arr){
              arr[i].isselect = false;
          }
          this.downdata = this.downdata.concat(arr);
          done();
          if(arr.length<10){
            this.$el.querySelector('.load-more').style.display = 'none';
          }else{
            this.$el.querySelector('.load-more').style.display = 'flex';
          }
        },
        async blursearch(){
            this.downdata = [];
            let res = await getTeacherNoticeList(10,this.search.search_txt,'');
            if(res.c==0){
                  this.listdata = res.d.data_list;
                  let arr =  res.d.data_list;
                  for(let i in arr){
                     arr[i].isselect = false;
                  }
                  if(arr.length<10){
                    this.$el.querySelector('.load-more').style.display = 'none';
                  }else{
                    this.$el.querySelector('.load-more').style.display = 'flex';
                  }
            }
        },
        myTouch(){
            let self=this;
            let h = document.documentElement.clientHeight;
            let myBody = document.getElementsByTagName('body')[0];
            myBody.style.height = h + 'px';

            //滑动处理
            let startX, startY;
            myBody.addEventListener('touchstart', function (ev){
              startX = ev.touches[0].pageX;
              startY = ev.touches[0].pageY;
            }, {passive: true});

            let endX, endY;
            myBody.addEventListener('touchmove', function (ev){
              endX = ev.changedTouches[0].pageX;
              endY = ev.changedTouches[0].pageY;

              let direction = GetSlideDirection(startX, startY, endX, endY);
              let myPublish = document.getElementsByClassName('hover-publish')[0];
              switch (direction){
                case 0:
                  break;
                case 1:
                  myPublish.style.display='none';
                  break;
                case 2:
                  myPublish.style.display='block';
                  break;
                case 3:

                  break;
                case 4:
                  break;
                default:
              }
            }, {passive: true});

            //返回角度
            function GetSlideAngle(dx,dy) {
              return Math.atan2(dy,dx) * 180 / Math.PI;
            }

            //根据起点和终点返回方向 1：向上，2：向下，3：向左，4：向右,0：未滑动
            function GetSlideDirection(startX,startY, endX, endY) {
              let dy = startY - endY;
              let dx = endX - startX;
              let result = 0;
              //如果滑动距离太短
              if (Math.abs(dx) < 2 && Math.abs(dy) < 2) {
                 return result;
              }

              let angle = GetSlideAngle(dx, dy);
              if (angle >= -45 && angle < 45) {
                 result = 4;
              }else if (angle >= 45 && angle < 135) {
                 result = 1;
              }else if (angle >= -135 && angle < -45) {
                 result = 2;
              }else if ((angle >= 135 && angle <= 180) || (angle >= -180 && angle < -135)) {
                 result = 3;
              }

              return result;
            }
        }
    },
    watch:{
        index:(cur,old)=>{console.log(cur)}
    },
    async created(){
        initializeEnv(this);
        this.myTouch();
        this.getList(10);
        this.backNative = new nativeCommon();
        let res = await getMyInfo();
        if(res.c==0){
            this.avatar = res.d.avatar;
        }
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
      Scroll,
    }
  }
</script>



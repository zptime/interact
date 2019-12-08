<template>
  <div>
    <scroller lock-x ref="scroller" :height="height"
              :use-pullup="!isDetail" :pullup-config="upConfig" @on-pullup-loading="loadMore"
              :use-pulldown="!isDetail" :pulldown-config="downConfig" @on-pulldown-loading="refresh">
      <div>
        <div class="dynamic" v-for="(dynamic, index) in dynamicList" @click="goDetail(dynamic.moment_id)">
          <!--基本信息-->
          <div class="base">
            <img class="base-avatar left" :src="dynamic.avatar" alt="头像" v-if="dynamic.avatar">
            <img class="base-avatar left" src="../../images/icon-default-avatar.png" alt="头像" v-else>
            <div class="base-info left">
              <div class="base-info-main">
                {{ dynamic.username }}
                <span class="type">{{ dynamic.user_type }} /
              <span v-if="dynamic.moment_type==5">请假</span>
              <span v-else-if="dynamic.moment_type==6">评价</span>
              <span v-else>风采</span>
            </span>
              </div>
              <div class="base-info-other">
                <img class="voice left" src="../../images/icon-voice.png" alt="语音" v-if="dynamic.has_voice==1&&!isDetail">
                <span class="time">{{ dynamic.create_time_perform }}</span>
              </div>
            </div>
            <img class="base-del right" src="../../images/icon-del.png" alt="删除" @click.stop="del(dynamic.moment_id, index)" v-if="dynamic.account_id==userInfo.account_id">
          </div>
          <!--文本-->
          <div class="text">
            <!--评价对象-->
            <div class="evaluate">
              {{ dynamic.evaluate.students }}
            </div>
            {{ dynamic.content }}
          </div>
          <!--语音-->
          <div class="audio" v-if="isDetail">
            <m-audio :popupBtn="false" :removeIcon="false" :origin="dynamic.voices" url="voice_converted_url"></m-audio>
          </div>
          <!--照片-->
          <div class="image">
            <img :src="dynamic.images[0].image_thumb_url" @click.stop="onPreview(dynamic.images, 0)" v-if="dynamic.images.length===1">
            <img class="image-layout" :src="image.image_crop_url" v-for="(image, index) in dynamic.images" @click.stop="onPreview(dynamic.images, index)" v-else>
          </div>
          <!--视频-->
          <div class="video">
            <MVideo :popupBtn="false" :videoData="dynamic.videos[0]"></MVideo>
          </div>
          <!--附件-->
          <div class="file">
            <div class="file-switch right" v-if="dynamic.files.length>3&&(!isDetail)" @click.stop="onSwitchClick(dynamic)">
              <span v-if="!dynamic.isFileExpand">展开</span>
              <span v-else>收起</span>
            </div>
            <div class="file-list clear" :class="{'fixed-height': dynamic.files.length>3&&(!dynamic.isFileExpand)&&(!isDetail)}">
              <MFile :popupBtn="false" :showDelete="false" :file-data="dynamic.files"></MFile>
            </div>
          </div>
          <!--投票-->
          <div class="vote" v-if="dynamic.moment_type==3">
            <div class="vote-expire" v-if="dynamic.is_voteexpire==1">已过期</div>
            <div class="vote-deadline" v-else>截止{{ dynamic.vote.vote_deadline }}</div>
            <div class="vote-item" v-for="item in dynamic.vote.vote_items">
              <div class="vote-item-branch left">{{ item.branch }}</div>
              <div class="vote-item-count right" :class="{active : item.isvote==1}" v-if="dynamic.is_voteexpire==1||dynamic.is_vote==1">{{ item.count }}票</div>
              <div class="vote-item-btn right" v-else @click.stop="momentDynamicVote(dynamic, item)">投一票</div>
            </div>
          </div>
          <!--操作-->
          <div class="opt">
            <!--浏览、点赞、回复-->
            <div>
              <div class="vote-stat left" v-if="dynamic.moment_type==3">{{ dynamic.vote.vote_statistics }}次投票</div>
              <div class="opt-read left" v-else>浏览{{ dynamic.read_count }}次</div>
              <div class="opt-reply right">
                <div class="left">{{ dynamic.reply_count }}</div>
                <img class="left" src="../../images/icon-reply.png" alt="回复" @click="replyTo('', '')">
              </div>
              <div class="opt-like right">
                <div class="left">{{ dynamic.like_count }}</div>
                <img class="left" src="../../images/icon-like.png" alt="点赞" v-if="dynamic.is_like==0" @click.stop="momentDynamicLike(dynamic)">
                <img class="left" src="../../images/icon-like-active.png" alt="点赞" v-else>
              </div>
            </div>
            <!--点赞列表-->
            <div class="opt-like-list" v-if="dynamic.like_count>0&&isDetail">
              <span v-for="(like, index) in dynamic.like">{{ like.username }}<span v-if="index<dynamic.like.length-1">,</span></span>
              {{ dynamic.like_count }}人点赞
            </div>
            <!--回复列表-->
            <div class="opt-reply-list">
              <div v-for="reply in dynamic.reply" @click="replyTo(reply.reply_id, reply.username)">
                <span class="username">{{ reply.username }}</span><span v-if="reply.ref.username">回复<span class="username">{{ reply.ref.username }}</span></span>:
                {{ reply.content }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </scroller>

    <!--回复框-->
    <div class="reply" v-if="isDetail">
      <input class="reply-input boxShadowGray" :class="{'reply-input-foucs': isFocus}" type="text" :placeholder="'回复'+reply_name+':'" @focus="isFocus=true" @blur="onBlur" v-model="content" v-if="isDetail">
      <div class="reply-btn boxShadowBlue" @click="momentDynamicReply(dynamicList[0].moment_id)" v-if="isFocus">确定</div>
    </div>

    <!--图片预览-->
    <previewer ref="previewer" :list="previewerImages"></previewer>

    <!--模态弹出框-->
    <actionsheet v-model="showDelete" :menus="menusDelete" @on-click-menu-delete="momentDynamicDelete" show-cancel></actionsheet>
  </div>
</template>

<script type="text/ecmascript-6">
  import MAudio from '@/components/m-audio/index.vue'
  import MVideo from '@/components/m-video/index.vue'
  import MFile from '@/components/m-file/chooseFile.vue'
  import { Scroller, Actionsheet, Previewer } from 'vux'
  import { getUserInfo, momentDynamicDelete, momentDynamicVote, momentDynamicLike, momentDynamicReply } from '../../service/getData.js'

  export default {
    props: {
      circleType: '',
      clazz: {},
      isDetail: {
        type: Boolean,
        default: false
      },
      height: {
        type: String,
        default: '-86'
      },
      dynamicList: {
        type: Array,
        default: ()=> []
      }
    },
    components: {
      MAudio,
      MVideo,
      MFile,
      Scroller,
      Actionsheet,
      Previewer
    },
    data () {
      return {
        userInfo: {},
        upConfig: {
          content: '上拉加载',
          downContent: '上拉加载',
          upContent: '松开载入更多',
          loadingContent: '正在加载...',
          height:30,
          pullUpHeight: 30,
          autoRefresh: false,
          clsPrefix: 'xs-plugin-pullup-'
        },
        downConfig: {
          content: '下拉刷新',
          downContent: '下拉刷新',
          upContent: '松开刷新数据',
          loadingContent: '刷新中...',
          height:30,
          autoRefresh: false,
          clsPrefix: 'xs-plugin-pulldown-'
        },
        previewerImages: [],
        needDeleteId: '',
        needDeleteIndex: '',
        showDelete: false,
        menusDelete: {
          'title.noop': '确定吗?<br/><span style="color:#666;font-size:0.6rem;">确定删除该风采？</span>',
          delete: '<span style="color:red">删除</span>'
        },
        isFocus: false,
        reply_id: '',
        reply_name: '',
        content: ''
      }
    },
    watch: {
      dynamicList: function () {
        //特殊处理
        for (let i=0; i<this.dynamicList.length; i++) {
          this.dynamicList[i].isFileExpand = false; //附件展开收起开关
          for (let j=0; j<this.dynamicList[i].files.length; j++) {
            this.dynamicList[i].files[j].downloadState = 0; //附件下载状态
          }
          for (let k=0; k<this.dynamicList[i].images.length; k++) {
            this.dynamicList[i].images[k].src = this.dynamicList[i].images[k].image_original_url; //图片预览
          }
        }
      }
    },
    created () {
      this.getUserInfo();
    },
    mounted () {
      if(!this.isDetail) {
        this.$nextTick(() => {
          this.$refs.scroller.reset({top: 0});
          this.$refs.scroller.disablePullup();
        });
      }
    },
    methods: {
      //上拉加载
      loadMore () {
        //显示upConfig
        let text = document.getElementsByClassName('xs-plugin-pullup-container')[0];
        if(text && text.style.opacity==0){
          text.style.opacity = 1;
        }
        this.$emit('on-loadMore');
      },
      //下拉刷新
      refresh () {
        this.$emit('on-refresh');
      },
      //跳转风采详情页
      goDetail (moment_id) {
        if (!this.isDetail) {
          this.$router.replace({
            name: 'momentDetail',
            query: {
              circle_type: this.circleType,
              clazz: this.clazz,
              moment_id: moment_id
            }
          });
        }
      },
      //附件展开收起开关切换
      onSwitchClick (dynamic) {
        dynamic.isFileExpand = !dynamic.isFileExpand;
        this.$forceUpdate();
      },
      //图片预览
      onPreview (images, index) {
        this.previewerImages = images;
        setTimeout(()=>this.$refs.previewer.show(index),0);
      },
      //删除
      del (moment_id, index) {
        this.showDelete = true;
        this.needDeleteId = moment_id;
        this.needDeleteIndex = index;
      },
      //回复
      replyTo (reply_id, reply_name) {
        if (this.isDetail) {
          this.isFocus = true;
          this.reply_id = reply_id;
          this.reply_name = reply_name;
        }
      },
      //回复框失去焦点
      onBlur () {
        if (this.content == '') {
          this.isFocus = false;
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
      //删除圈子动态
      async momentDynamicDelete () {
        //详情和列表删除的响应方式不同
        if (this.isDetail) {
          this.$vux.loading.show({
            text: '删除中'
          });
          let res = await momentDynamicDelete(this.needDeleteId);
          this.$vux.loading.hide();
          if (res.c == 0) {
            //返回列表页
            this.$router.back();
          } else {
            this.$vux.toast.show({
              type: 'text',
              text: res.m
            })
          }
        } else {
          //删除即时响应
          this.dynamicList.splice(this.needDeleteIndex, 1);
          momentDynamicDelete(this.needDeleteId);
        }
      },
      //投票圈子动态
      async momentDynamicVote (dynamic, item) {
        //投票即时响应
        dynamic.is_vote = '1';
        item.isvote = '1';
        item.count++;
        momentDynamicVote(item.vote_item_id);
      },
      //点赞圈子动态
      async momentDynamicLike (dynamic) {
        //点赞即时响应
        dynamic.is_like = '1';
        dynamic.like_count++;
        dynamic.like.unshift({username: this.userInfo.name});
        momentDynamicLike(dynamic.moment_id);
      },
      //回复圈子动态
      async momentDynamicReply (moment_id) {
        this.$vux.loading.show({
          text: '加载中'
        });
        let res = await momentDynamicReply(moment_id, this.reply_id, this.content);
        this.$vux.loading.hide();
        if (res.c == 0) {
          //刷新动态
          this.refresh();
        } else {
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          })
        }

        //还原回复框
        this.isFocus = false;
        this.reply_id = '';
        this.reply_name = '';
        this.content = '';
      }
    }
  }
</script>

<style scoped>
  .dynamic {
    margin: 0 0.75rem;
    padding-top: 0.75rem;
    border-bottom: 1px solid #eee;
  }
  .dynamic:last-child {
    border: none;
  }
  .base, .image, .opt {
    overflow: hidden;
  }
  .base-avatar {
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
  }
  .base-info {
    margin-left: 0.5rem;
  }
  .base-info-main {
    font-size: 0.8rem;
    color: #111;
    line-height: 1.1rem;
  }
  .base-info-main .type {
    margin-left: 0.5rem;
    font-size: 0.7rem;
    color: #666;
  }
  .base-info-main .type span {
     color: #666;
  }
  .base-info-other {
    line-height: 0.65rem;
  }
  .base-info-other .voice {
    margin-right: 0.5rem;
    width: 0.8rem;
  }
  .base-info-other .time {
    font-size: 0.6rem;
    color: #aaa;
  }
  .base-del {
    width: 1.5rem;
  }
  .text {
    margin: 0.5rem 0;
    font-size: 0.75rem;
    color: #444;
    line-height: 1.2rem;
  }
  .evaluate {
    color: #4685ff;
  }
  .audio {
    margin: 0.5rem 0;
  }
  .image-layout {
    float: left;
    margin-right: 0.35rem;
    margin-bottom: 0.35rem;
    width: 5.5rem;
  }
  .image-layout:nth-of-type(3) {
    margin-right: 0;
  }
  .file-switch {
    margin-bottom: 0.5rem;
    font-size: 0.7rem;
  }
  .file-switch span {
    color: #4685ff;
  }
  .file-list {
    clear: both;
    overflow: hidden;
  }
  .fixed-height {
    height: 150px;
  }
  .vote-expire {
    margin-bottom: 1rem;
    width: 2rem;
    height: 0.75rem;
    text-align: center;
    line-height: 0.75rem;
    font-size: 0.55rem;
    color: #fff;
    background-color: #aaa;
    border-radius: 4px;
  }
  .vote-deadline {
    margin-bottom: 1rem;
    font-size: 0.55rem;
    color: #aaa;
  }
  .vote-item {
    margin: 0.5rem 0;
    overflow: hidden;
  }
  .vote-item-branch {
    line-height: 1.2rem;
    font-size: 0.75rem;
    color: #444;
  }
  .vote-item-count {
    line-height: 1.2rem;
    font-size: 0.6rem;
    color: #444;
  }
  .vote-item-count.active {
    color: #4685ff;
  }
  .vote-item-btn {
    width: 3rem;
    height: 1.2rem;
    text-align: center;
    line-height: 1.2rem;
    font-size: 0.6rem;
    color: #444;
    border: 1px solid #aaa;
    border-radius: 4px;
  }
  .opt>div {
    margin: 0.5rem 0;
    overflow: hidden;
  }
  .opt-read, .vote-stat {
    line-height: 1.2rem;
    font-size: 0.6rem;
    color: #aaa;
  }
  .opt-like, .opt-reply {
    margin-left: 2rem;
    line-height: 1.2rem;
    font-size: 0.6rem;
    color: #aaa;
  }
  .opt-like img, .opt-reply img {
    height: 1.2rem;
  }
  .opt-like-list {
    clear: both;
    padding: 4px;
    line-height: 1.2rem;
    font-size: 0.7rem;
    background-color: #eee;
    border-radius: 4px;
  }
  .opt-like-list span {
    color: #4685ff;
  }
  .opt-reply-list {
    line-height: 1.2rem;
    font-size: 0.7rem;
  }
  .opt-reply-list .username {
    color: #4685ff;
  }
  .reply {
    position: fixed;
    left: 0;
    bottom: 0;
    margin: 0.75rem;
    width: 17.25rem;
    height: 2.25rem;
  }
  .reply-input {
    padding: 0 4px;
    width: 100%;
    height: 100%;
    font-size: 0.75rem;
    border-radius: 4px;
    -webkit-appearance: none;
  }
  .reply-input-foucs {
    width: 80%;
  }
  .reply-btn {
    float: right;
    background: #4685ff;
    color: #FFFFFF;
    font-size: 0.6rem;
    width: 2.25rem;
    height: 2.25rem;
    line-height: 2.25rem;
    text-align: center;
    border-radius: 50%;
  }
</style>

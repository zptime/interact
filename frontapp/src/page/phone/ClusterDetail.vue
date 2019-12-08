<template>
  <div class="phone">
    <head-top :head="head">
      <img slot="left" src="../../images/icon-return.png" @click="goBack"/>
    </head-top>
    <div class="contentBox" v-cloak>
      <div class="content">
        <div class="itemTitle clb boxShadowGray">
          <span class="avatar">
            <img src="../../images/icon-default-cluster.png">
          </span>
          <span class="name">{{ group_name }}</span>
          <span class="opt del" @click="delGroup">
            <img src="../../images/icon-del.png">
          </span>
          <span class="opt edit" @click="editGroup">
            <img src="../../images/icon-edit.png">
          </span>
        </div>
      </div>
      <group-member :origin="group_list" :showTotal="true"></group-member>
      <actionsheet v-model="showDelAction" :menus="menus" @on-click-menu-delete="clickDelMenu" show-cancel></actionsheet>
    </div>
  </div>
</template>

<script type="es6">
  import HeadTop from '@/components/Head.vue'
  import Actionsheet from 'vux/src/components/actionsheet/index.vue'
  import GroupMember from '@/components/m-member/groupMember.vue'
  import { mapState,mapMutations } from 'vuex'
  import { contactGroupUserList,contactGroupDissolve,contactGroupDetail } from '../../service/getData'
  export default {
    data(){
      return {
        head:{
          icon: 'return',
          title: '小组详情',
          more: false
        },
//        group_id:'',//群组id
        group_name:'',//群组名称
        group_list:[],//群组列表
        showDelAction:false,//是否显示删除弹框
        menus: {//actionSheet的菜单项列表
          'title.noop': '<span class="action-title">确定删除该小组？</span>',
          delete: '<span class="action-del">删除</span>'
        },
      }
    },
    components: {
      HeadTop,
      Actionsheet,
      GroupMember,
    },
    created(){
      this.initData();
    },
    computed:{
      ...mapState([
        'group_id',
      ])
    },
    methods:{
      ...mapMutations([
        'NAV_FLAG',
        'GROUP_ID',
      ]),

      goBack(){
        this.NAV_FLAG(2);
        this.$router.back();
      },

      async initData(){
        this.groupInfo();
        this.groupList();
      },

      //获取小组基本信息
      async groupInfo(){
        let res;
        res = await contactGroupDetail(this.group_id);
        if(res.c == 0){
          this.group_name = res.d[0].group_name;
        }else{
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          });
        }
      },

      //获取小组列表
      async groupList(){
        let res;
        res = await contactGroupUserList(this.group_id);
        if(res.c == 0){
          this.group_list.push({
            "data": res.d,
            "title":'群组成员',
            "number":res.d.length,
            "show":true
          });
        }else{
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          });
        }
      },

      //编辑小组
      editGroup(){
        this.GROUP_ID(this.group_id);
        this.$router.push('phoneClusterEdit');
      },

      //打开删除小组弹框
      delGroup(){
        this.showDelAction = true;
      },

      //删除小组
      async clickDelMenu(){
        let res = await contactGroupDissolve(this.group_id);
        if(res.c==0){
          this.$vux.toast.show({
            type: 'text',
            text: '删除成功'
          });
          this.$router.back();
        }else{
          this.$vux.toast.show({
            type: 'text',
            text: res.m
          })
        }
      },
    }
  }
</script>

<style scoped>
  body {
    transform: translate(0, 0);
  }
  .contentBox{
    bottom: 0;
    overflow: hidden;
  }
  .content{
    position: fixed;
    width: 100%;
    top:2.1rem;
    height: 5rem;
    z-index:9;
  }
  .itemTitle{
    height: 2.5rem;
    margin:1.5rem 0.75rem 1rem 0.75rem;
    background-color: #fff;
    -webkit-border-radius: 1.25rem;
    -moz-border-radius: 1.25rem;
    -ms-border-radius: 1.25rem;
    -o-border-radius: 1.25rem;
    border-radius: 1.25rem;
  }
  .itemTitle span{
    display: inline-block;
    height: 2.5rem;
    line-height: 2.5rem;
    float: left;
  }
  .itemTitle .avatar img{
    width:2.5rem;
    height:2.5rem;
    -webkit-border-radius: 1.25rem;
    -moz-border-radius: 1.25rem;
    -ms-border-radius: 1.25rem;
    -o-border-radius: 1.25rem;
    border-radius: 1.25rem;
  }
  .itemTitle .name{
    font-size: 0.75rem;
    margin-left:0.5rem;
    color:#444;
  }
  .itemTitle .opt{
    float:right;
  }
  .itemTitle .opt img{
    width:1.2rem;
    height:1.2rem;
    margin-top:0.65rem;
  }
  .itemTitle .del{
    margin:0 0.8rem 0 1rem;
  }
</style>

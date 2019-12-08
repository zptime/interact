<template>
  <div class="phone">
    <head-top :head="head"></head-top>
    <div class="contentBox" v-cloak>
      <div class="content edit">
        <div class="name">
          <x-input :max="10" @on-change="change" v-model="group_name" :show-clear="false"></x-input>
        </div>
        <div class="btnCommon longButton" @click="goChoose">添加小组成员</div>
      </div>
      <group-member :groupId="group_id" :origin="group_list" :removeBtn="true"
                    @on-init="initData" :setMemberStyle="setMemberStyle">
      </group-member>
      <div class="btnOpt">
        <div class="btnCommon btnBottomOpt boxShadowGray clb">
          <span class="btn_cancel left" @click="optClick('cancel')">取消</span>
          <span class="btn_divide"></span>
          <span class="btn_sure right" @click="optClick('sure')">确定</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script type="es6">
  import HeadTop from '@/components/Head.vue'
  import XInput from 'vux/src/components/x-input/index.vue'
  import GroupMember from '@/components/m-member/groupMember.vue'
  import { mapState } from 'vuex'
  import { contactGroupUserList,contactGroupDetail,contactGroupEdit } from '../../service/getData'
  export default {
    data(){
      return {
        head:{
          icon: 'return',
          title: '编辑小组',
          more: false
        },
//        group_id:'',//群组id
        group_name:'',//群组名称
        group_info:{},//群组基本信息
        group_list:[],//群组列表
        setMemberStyle:{
          'top':'9.1rem',
          'bottom':'4rem'
        }
      }
    },
    components: {
      HeadTop,
      XInput,
      GroupMember,
    },
    computed:{
      ...mapState([
        'group_id',
      ])
    },
    created(){
      this.initData();
    },
    methods:{
      async initData(){
        this.groupInfo();
        this.groupList();
      },

      //获取小组基本信息
      async groupInfo(){
        let res;
        res = await contactGroupDetail(this.group_id);
        if(res.c == 0){
          this.group_info = res.d[0];
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
          this.group_list = [];
          this.group_list.push({
            "id":this.group_id,
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

      change(){
        console.log(this.group_name);
      },

      //进入选择人员界面
      goChoose(){
        this.$router.push({
          name:'choosePerson',
          query:{
            groupId:this.group_id
          }
        });
      },

      //操作按钮事件（取消、确定）
      async optClick(opt){
        if(opt=='cancel'){//取消
          this.$router.back();
        }else{//确定
          let res = await contactGroupEdit(this.group_id,this.group_name);
          if(res.c==0){
            this.$vux.toast.show({
              type: 'text',
              text: '操作成功'
            });
            let _this = this;
            setTimeout(function () {
              _this.$router.back();
            }, 10);
          }else{
            this.$vux.toast.show({
              type: 'text',
              text: res.m
            });
          }
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
    padding:0 0.75rem;
    position: fixed;
    width:100%;
    top:2.1rem;
    height:7rem;
    z-index:9;
  }
  .name{
    /*border-bottom: 2px solid #eee;*/
    margin:1.5rem 0 1rem 0;
  }
</style>

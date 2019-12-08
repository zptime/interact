<template>
  <div class="phone">
    <div class="content fixed" v-show="showCluster" :style="fixedTopB(4.1,5)">
      <div v-for="item in clusterList" @click="goDetail(item)">
        <div class="item boxShadowGray">
        <span class="avatar">
          <img src="../../images/icon-default-cluster.png">
        </span>
          <span class="name">{{ item.grp_name }}</span>
        </div>
      </div>
    </div>
    <div class="btnOpt">
      <div class="btnCommon bottomButton boxShadowBlue" @click="addCluster">+ 创建小组</div>
    </div>
  </div>
</template>

<script type="es6">
  import global from '@/components/Global.vue'
  import { mapMutations } from 'vuex'
  export default {
    props:['clusterList'],
    data(){
      return {
        showCluster:true,
      }
    },
    methods:{
      ...mapMutations([
        'GROUP_ID',
      ]),

      //fixed定位top、bottom设置
      fixedTopB(top,bottom){
        if(global.showHead){//带头部head
          top += 2.1;
        }
        let styles = {
          'top':top+ 'rem',
          'bottom':bottom + 'rem'
        };
        return styles;

      },

      //进入创建小组页面
      addCluster(){
        this.$router.push('phoneClusterAdd');
      },

      //进入小组详情页面
      goDetail(item){
        this.$router.push('phoneClusterDetail');
        this.GROUP_ID(item.grp_id);
      }
    },
  }
</script>

<style scoped>
  .content{
    padding:0.2rem 0.75rem 0 0.75rem;
    overflow-y: auto;
    -webkit-overflow-scrolling : touch;
  }
  .btnOpt .bottomButton{
    margin:2.5rem auto 1rem auto;
  }
  .item{
    height: 2.5rem;
    /*padding:0.25rem;*/
    margin-bottom:1rem;
    background-color: #fff;
    -webkit-border-radius: 1.25rem;
    -moz-border-radius: 1.25rem;
    -ms-border-radius: 1.25rem;
    -o-border-radius: 1.25rem;
    border-radius: 1.25rem;
  }
  .item span{
    display: inline-block;
    height: 2.5rem;
    line-height: 2.5rem;
    float: left;
  }
  .item img{
    width:2.5rem;
    height:2.5rem;
    -webkit-border-radius: 1.25rem;
    -moz-border-radius: 1.25rem;
    -ms-border-radius: 1.25rem;
    -o-border-radius: 1.25rem;
    border-radius: 1.25rem;
  }
  .item .name{
    font-size: 0.75rem;
    margin-left:0.5rem;
    color:#444;
  }
</style>

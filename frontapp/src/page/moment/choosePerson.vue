<template>
  <div>
    <head-top :head="head">
      <img slot="left" src="../../images/icon-return.png" @click="optCancel"/>
    </head-top>
    <choose-target :title="title" @on-cancel="optCancel" @on-sure="optSure"></choose-target>
  </div>
</template>

<script type="text/ecmascript-6">
  import ChooseTarget from '../../components/m-member/ChooseTarget.vue'
  import HeadTop from '@/components/Head.vue'
  import { mapState,mapMutations } from 'vuex'
  export default {
    data () {
      return {
        head:{
          icon: 'return',
          title: '选择评价对象',
          more: false
        },
        title:'评价',
        dataList:[],//返回数据列表
      }
    },
    computed:{
      ...mapState([
        'choosed_person',
      ])
    },
    components: {
      ChooseTarget,
      HeadTop,
    },
    methods:{
      ...mapMutations([
        'CHOOSED_PERSON',
      ]),
      //取消回调事件
      optCancel(){
        this.$emit('backPopup',[]);
      },
      //确定回调事件
      optSure(data){
        this.dataList = data;
        this.$emit('backPopup',data);
      },
    },
  }
</script>

<style scoped>

</style>

<template>
  <div>
    <head-top :head="head"></head-top>
    <choose-target   @backUrl=""     :title="title" @on-cancel="optCancel"  @on-sure="optSure"></choose-target>
  </div>
</template>

<script type="es6">
  import ChooseTarget from '../../../components/m-member/ChooseTarget.vue'
  import HeadTop from '@/components/Head.vue'
  import { mapState,mapMutations } from 'vuex'
  export default {
    data () {
      return {
        head:{
          icon: 'return',
          title: '选择通知对象',
          more: false
        },
        title:'通知',
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
        //alert('确定回调事件');
        this.dataList = data;
    //    this.CHOOSED_PERSON(data);
        this.$emit('backPopup',data);
      },
    },
  }
</script>

<style scoped>

</style>

<template>
  <div>
    <head-top :head="head"></head-top>
    <div style="padding: 3.6rem 0.75rem 0;">
        <p>胡洁的家庭邀请码，扫码二维码成为家庭成员。</p>
        <p>从此关心胡洁的学校生活。</p>
        <div style="line-height: 10rem;text-align: center;border: solid 1px #eee;width: 10rem;margin: 2rem auto;">这里放二维码</div>
    </div>
  </div>
</template>

<script type="es6">
  import HeadTop from '@/components/Head.vue'
  import { TransferDomDirective as TransferDom  } from 'vux'
  export default {
    directives: {
        TransferDom
    },
    data () {
      return {
        head:{
          icon: 'return',
          title: '互动系统-个人中心',
          more: false
        },
      }
   },
   methods:{

   },
    components: {
      HeadTop,
    },
  }

</script>

<style scoped>

</style>

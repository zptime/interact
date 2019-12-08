<template>
  <div>
    <img class="publish-btn" src="../../images/icon-publish.png" v-if="!showDialog" @click="showDialog=true">
    <x-dialog v-model="showDialog" :dialog-style="{position: 'fixed', width: '5.4rem', left: 'auto', top: 'auto', right: '1rem', bottom: '3.25rem', 'background-color': 'transparent'}" hide-on-blur>
      <div class="dialog-item">
        <router-link :to="{name: 'momentPublishCommon', query: {circle_type: circleType, clazz: clazz, publish_type: 1}}" replace>
          <div class="item-icon icon-moment"></div>
        </router-link>
        <div class="item-text">风采</div>
      </div>
      <!--教师-->
      <div class="dialog-item" v-if="userInfo.user_type_id==2">
        <router-link :to="{name: 'momentPublishEvaluate', query: {circle_type: circleType, clazz: clazz}}" replace>
          <div class="item-icon icon-evaluate"></div>
        </router-link>
        <div class="item-text">评价</div>
      </div>
      <!--家长-->
      <div class="dialog-item" v-if="userInfo.user_type_id==4">
        <router-link :to="{name: 'momentPublishCommon', query: {circle_type: circleType, clazz: clazz, publish_type: 2}}" replace>
          <div class="item-icon icon-dayoff"></div>
        </router-link>
        <div class="item-text">请假</div>
      </div>
    </x-dialog>
  </div>
</template>

<script type="text/ecmascript-6">
  import { XDialog } from 'vux'
  import { getUserInfo } from '../../service/getData.js'

  export default {
    props: {
      circleType: '',
      clazz: {}
    },
    components: {
      XDialog
    },
    data () {
      return {
        showDialog: false,
        userInfo: {}
      }
    },
    created () {
      this.getUserInfo();
    },
    methods: {
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
      }
    }
  }
</script>

<style scoped>
  .publish-btn {
    position: fixed;
    right: 1rem;
    bottom: 3.25rem;
    width: 3rem;
    height: 3rem;
  }
  .dialog-item {
    margin-top: 1rem;
    overflow: hidden;
  }
  .item-text {
    float: right;
    margin-right: 0.75rem;
    line-height: 2.5rem;
    font-size: 0.7rem;
    color: #fff;
  }
  .item-icon {
    float: right;
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
  }
  .icon-moment {
    background: #fff url('../../images/icon-moment.png') no-repeat center / 50%;
    border: solid 4px #f16f6f;
  }
  .icon-evaluate {
    background: #fff url('../../images/icon-evaluate.png') no-repeat center / 50%;
    border: solid 4px #f8b62d;
  }
  .icon-dayoff {
    background: #fff url('../../images/icon-dayoff.png') no-repeat center / 50%;
    border: solid 4px #4685ff;
  }
</style>

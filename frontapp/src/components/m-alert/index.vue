<!--提示框，有复制功能-->
<template>
  <div v-transfer-dom>
    <confirm v-model="show"
             title="请复制地址去浏览器下载或查看"
             @on-cancel="onCancel"
             @on-confirm="onConfirm"
    >
      <p id="pasedTarget" style="text-align:center;">{{needPasedTxt}}</p>
    </confirm>
    <button ref="copyButton" v-show="false" id="copyBtn" data-clipboard-action="copy" data-clipboard-target="#pasedTarget" @click="copyPolicyNo">复制</button>
  </div>
</template>

<script>
  import Confirm from  'vux/src/components/confirm/index.vue'
  import { TransferDom } from 'vux'
  import Clipboard from 'clipboard'
  import {showTextToast} from '../../components/framework/toastViewMgr.js'

  export default {
    props:{
      parentContext:{
        type:Object,
        default:()=> undefined
      }
    },
    components: {
      Confirm,
      Clipboard,
    },
    directives:{
      TransferDom
    },
    data(){
      return {
        clipboard:undefined,
        show:false,//外界赋值这个控制弹窗的显影
        needPasedTxt: '这是文件的url，需要设置',//外界赋值文案，用于显示的文案
      }
    },

    methods: {
      onCancel(){

      },
      onConfirm(){
        //确认事件 使copybutton执行事件
        this.$refs.copyButton.click();
      },
      copyPolicyNo(){
        if (!this.clipboard){
          this.clipboard = new Clipboard('#copyBtn');
        }
        var _parent = undefined;
        if (this.parentContext){
          _parent = this.parentContext;
        }else{
          _parent = this;
        }
        this.clipboard.on('success', function(e) {
          showTextToast(_parent,'复制成功');
          e.clearSelection();
        });
      },
    },
    mounted(){
      this.$nextTick(function () {
        //weui-dialog__btn weui-dialog__btn_primary
        //确定按钮修改文案
        let obj = document.getElementsByClassName('weui-dialog__btn weui-dialog__btn_primary')[0];
        obj.innerHTML = '复制';
      })
    },
    created(){

    }
  }

</script>

<style>
</style>

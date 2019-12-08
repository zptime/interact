<template>
  <div>
    <div class="hover-publish" v-if="show" @click="optClick" :style="btnSecStyle">
      <slot name="image">
        <img src="./icon.png" :style="imgSecStyle">
      </slot>
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
  import { Touch,GetSlideDirection } from './touch.js'
  export default {
    props: {
      show:{
        type: Boolean,
        default: true
      },
      scroll:{
        type: Boolean,
        default: true
      },
      btnSecStyle: {
        type: Object,
        default : () => {}
      },
      imgSecStyle: {
        type: Object,
        default : () => {}
      },
    },
    data () {
      return {
        direction:0,
      }
    },
    created(){
      //Touch(this.scroll,'hover-publish');
      this.myTouch('hover-publish');
    },
    methods: {
      optClick(){
        this.$emit('on-click');
      },
      onChange(){
//        console.log(this.direction);
        this.$emit('on-change',this.direction);
      },
      setShow(){
        let myPublish = document.getElementsByClassName('hover-publish')[0];
        myPublish.style.display='block';
      },
      setHide(){
        let myPublish = document.getElementsByClassName('hover-publish')[0];
        myPublish.style.display='none';
      },
      myTouch(hoverEle){
        let _this = this;
        let myBody = document.getElementsByTagName('body')[0];

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
          _this.direction = direction;
          _this.onChange();
          let myPublish = document.getElementsByClassName(hoverEle)[0];
          switch (direction){
            case 0:
              break;
            case 1:
              if(_this.scroll && myPublish){
                myPublish.style.display='none';
              }
              break;
            case 2:
              if(_this.scroll && myPublish){
                myPublish.style.display='block';
              }
              break;
            case 3:
              break;
            case 4:
              break;
            default:
          }
        }, {passive: true});
      }
    },
  }
</script>

<style scoped>
  .hover-publish{
    position: absolute;
    bottom:3.25rem;
    right:1rem;
    z-index:99;
    opacity: 1;
  }
  .hover-publish img{
    width:3rem;
    height: 3rem;
  }
</style>


/**
 * Created by yulu on 2018/6/15.
 */

function nativeWindows (context, opt) {
  var _self = this;
  this.options  = opt || {}
  this.closeWindows = function () {
    window._win_nativeWindows = this;
    //todo  这里添加代码，调用native拉起图片选择器
    if ((typeof goBackActivity) != 'undefined'){
      goBackActivity(this.options);
    }
  }

}

export default nativeWindows = nativeWindows


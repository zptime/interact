/**
 * Created by yulu on 2018/6/15.
 */

function nativeWindows (context, opt) {
  var _self = this;
  this.options  = opt || {}
  this.closeWindows = function () {
    window._win_nativeWindows = this;
    //todo  ������Ӵ��룬����native����ͼƬѡ����
    if ((typeof goBackActivity) != 'undefined'){
      goBackActivity(this.options);
    }
  }

}

export default nativeWindows = nativeWindows


/**
 * Created by jie on 2018/3/14.
 */


function nativeCommon (opt){
  var _self = this;
  this.options  = opt || {}
  this.init = function () {
    window._win_nativeCommon = _self;
    //todo  这里添加代码，调用native拉起图片选择器
    if ((typeof goBackActivity) != 'undefined'){
      goBackActivity(this.options);
    }
  },
    //obj {barColor:barColor,textColor:textColor}
  this.setNativeComponentColor = function (obj) {
    if((typeof callNativeSetColor) != 'undefined'){
      callNativeSetColor(JSON.stringify(obj));
    }
  },
  this.recoverNavComponentColor = function (obj) {
    if((typeof callNativeRecoverColor) != 'undefined'){
      callNativeRecoverColor(obj);
    }
  },
    //调用原生拨号界面
    //obj电话号码字符串
  this.callPhone = function (obj) {
    window._win_nativeCommon = _self;
    let phoneObj = {};
    phoneObj.phone = obj;
    callNativeCallPhone(JSON.stringify(phoneObj));
  }
}


export default nativeCommon = nativeCommon


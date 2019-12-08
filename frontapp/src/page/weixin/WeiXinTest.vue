<template>
  <div>
    <div style="width: 6rem;height: 2rem;margin: 1rem 1rem 0 1rem;border: 1px solid blue;text-align: center;font-size: 0.9rem;" @click="configWeiXin">启动微信配置</div>
    <div style="width: 6rem;height: 2rem;margin: 1rem 0 0 0;text-align: center;font-size: 0.9rem;">图片接口</div>
    <div style="overflow: hidden;width: 100%;margin: 0 0rem 0rem 1rem;">
      <div class="test-target-item" @click="goClick('chooseImage')">图片选择</div>
      <div class="test-target-item" @click="goClick('uploadImage')">图片上传</div>
      <div class="test-target-item" @click="goClick('downloadImage')">图片下载</div>
      <div class="test-target-item" @click="goClick('showImage')">图片展示</div>
      <img style="width: 6rem;height: 6rem;margin-top: 0.5rem" :src="mImage.mBase64Data"/>
    </div>

    <div style="width: 6rem;height: 2rem;margin: 1rem 0 0 0;text-align: center;font-size: 0.9rem;">扫描接口</div>
    <div style="overflow: hidden;width: 100%;margin: 0 0rem 0rem 1rem;">
      <div class="test-target-item" @click="goClick('scan')">图片扫描</div>
      <div style="width: 100%;font-size: 0.7rem">{{mQScanCode}}</div>
    </div>

    <div style="width: 6rem;height: 2rem;margin: 1rem 0 0 0;text-align: center;font-size: 0.9rem;">定位接口</div>
    <div style="overflow: hidden;width: 100%;margin: 0 0rem 0rem 1rem;">
      <div class="test-target-item" @click="goClick('location')">地理定位</div>
      <div class="test-target-item" @click="goClick('map')">地理地图</div>
    </div>

    <div style="width: 6rem;height: 2rem;margin: 1rem 0 0 0;text-align: center;font-size: 0.9rem;">声音接口</div>
    <div style="overflow: hidden;width: 100%;margin: 0 0rem 0rem 1rem;">
      <div class="test-target-item" @click="goClick('startRecord')">开始录音</div>
      <div class="test-target-item" @click="goClick('stopRecord')">停止录音</div>
      <div class="test-target-item" @click="goClick('startVoice')">开始播放</div>
      <div class="test-target-item" @click="goClick('pauseVoice')">暂停播放</div>
      <div class="test-target-item" @click="goClick('stopVoice')">停止播放</div>
      <div class="test-target-item" @click="goClick('uploadVoice')">上传语音</div>
      <div class="test-target-item" @click="goClick('downloadVoice')">下载语音</div>
    </div>
    <div style="width: 10rem;height: 2rem;margin: 1rem 0 0 0;text-align: center;font-size: 0.9rem;">文件接口(仅安卓使用)</div>
    <div style="position: relative;margin: 0 0 1rem 1rem;width: 1.5rem;height: 1.5rem;">
      <img style="width: inherit;height: inherit" src="../../images/icon-add.png"/>
      <input ref="uFile" type="file" style="position: absolute;left:0;top:0;opacity:0;width: inherit;height: inherit" @change="onSelFiles()"/>
    </div>

    <div style="height: 10rem;width: 100%"/>
  </div>

</template>


<script type="es6">
  import {query_WeiXin_metaData,uploadBlobImage, uploadFile} from '../../service/getData.js'
  import wx from 'weixin-js-sdk'
  import {createFileMgr} from './FileMgrFactory.js'
  export default {
    data () {
      return {
        hasValid:"0",
        mWXConfig: {},
        mImage:{
          mLocalId:'',
          mServiceId:'',
          mDownLoadId:'',
          mBase64Data:'',
        },
        mVoice:{
          mLocalId:'',
          mMediaId:'',
        },
        mQScanCode:'',
        mLocationInfo:{},
      }
    },
    created(){
      let fileMgr = createFileMgr('1');
      fileMgr.fun1();
      this.initWeiXinJs();
      this.initData();
    },
    methods: {
      onSelFiles() {
        //alert(this.$refs.uFile.files[0]);
        this.asyncUpload();
      },
      async asyncUpload() {
        let res = await uploadFile(this.$refs.uFile.files[0]);
        if (res.c == 0 ) {
          alert(res.d.file_url);
          return;
        }

        alert('文件上传失败');
      },
      async initData() {
        //let res = await query_WeiXin_metaData('2','http://yulu.ngrok1.hbeducloud.com/m/weixin');
        let res = await query_WeiXin_metaData('1','http://interact-test.hbeducloud.com/m/weixin');
        //let res = await query_WeiXin_metaData('1','http://repair-test.hbeducloud.com/m/weixin');
        if (res.c == 0 ) {
           this.mWXConfig = res.d;
          alert("app_id" + this.mWXConfig.appid + ",singture=" + this.mWXConfig.signature + ",");
          return;
        }

        alert('获取服务器配置失败');
      },
      async uploadImageToServer() {
        let res = await uploadBlobImage(window._weixin_.mImage.mBase64Data);
        if (res.c == 0) {
          alert(res.d.original_image_url);
          alert(res.d.image_crop_url);
          return;
        }

        alert("上传服务器图片失败");
      },
      initWeiXinJs() {
        window._weixin_ = this;
      },
      configWeiXin() {
        // 这里的appid是余璐的测试公众号，timestamp是生成签名时候的时间戳，要用秒
        // nonceStr是一个UUID, signature是微信定义的一个签名策略，我们可以通过网站生成
        // 参见http://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=jsapisign
        // 注意这个只能保存两个小时的有效性，而且每天access code只有2000次，过多调用将不允许。
        /*wx.config({
          debug: true, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
          appId: 'wxc12306f89eeb8027', // 必填，公众号的唯一标识
          timestamp: '1528783668', // 必填，生成签名的时间戳
          nonceStr: 'XoqX0u1suviYN1a', // 必填，生成签名的随机串
          signature: 'b57a7594a3c092e1494914318dbe8929887f27c7',// 必填，签名，见附录1
          jsApiList: ['checkJsApi',
            'onMenuShareTimeline','onMenuShareQQ','onMenuShareWeibo','onMenuShareQZone', // 分享微博，QQ空间
            'chooseImage','previewImage', // 选选图片，预览图片,successfully
            'uploadImage','downloadImage','getLocalImgData', // 上传图片。下载图片，获取图片数据,successfully
            'startRecord', 'stopRecord','onVoiceRecordEnd', //开始录制，停止录制，录制结束接口,successfully
            'playVoice','pauseVoice','stopVoice','onVoicePlayEnd', // 播放声音，暂停声音，停止声音，声音停止回调,successfully
            'uploadVoice','downloadVoice', // 上传声音， 下载声音
            'openLocation','getLocation', // 打开定位，获取定位,successfully
            'scanQRCode'] // 二维码扫描 ,successfully
        });*/
        wx.config({
          debug: true, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
          appId: _weixin_.mWXConfig.appid, // 必填，公众号的唯一标识
          timestamp: _weixin_.mWXConfig.timestamp, // 必填，生成签名的时间戳
          nonceStr: _weixin_.mWXConfig.noncestr, // 必填，生成签名的随机串
          signature: _weixin_.mWXConfig.signature,// 必填，签名，见附录1
          jsApiList: ['checkJsApi',
            'onMenuShareTimeline','onMenuShareQQ','onMenuShareWeibo','onMenuShareQZone', // 分享微博，QQ空间
            'chooseImage','previewImage', // 选选图片，预览图片,successfully
            'uploadImage','downloadImage','getLocalImgData', // 上传图片。下载图片，获取图片数据,successfully
            'startRecord', 'stopRecord','onVoiceRecordEnd', //开始录制，停止录制，录制结束接口,successfully
            'playVoice','pauseVoice','stopVoice','onVoicePlayEnd', // 播放声音，暂停声音，停止声音，声音停止回调,successfully
            'uploadVoice','downloadVoice', // 上传声音， 下载声音
            'openLocation','getLocation', // 打开定位，获取定位,successfully
            'scanQRCode'] // 二维码扫描 ,successfully
        });

        wx.ready(function(){
          // config信息验证后会执行ready方法，所有接口调用都必须在config接口获得结果之后，
          // config是一个客户端的异步操作，所以如果需要在页面加载时就调用相关接口，
          // 则须把相关接口放在ready函数中调用来确保正确执行。对于用户触发时才调用的接口，
          // 则可以直接调用，不需要放在ready函数中。
          alert("WX 配置加载完毕");
        });
      },
      goClick(feature) {
        if (feature == 'chooseImage') {
          this.chooseImage();
          return;
        }

        if (feature == 'uploadImage') {
          this.uploadImage(window._weixin_.mImage.mLocalId.toString());
          return;
        }

        if (feature == 'downloadImage') {
          this.downloadImage(window._weixin_.mImage.mServiceId.toString());
          return;
        }

        if (feature == 'showImage') {
          this.queryImageById(window._weixin_.mImage.mDownLoadId.toString());
	  //this.queryImageById(window._weixin_.mImage.mLocalId.toString());
        }
        if (feature == 'record') {
          return;
        }

        if (feature == 'share') {
          this.share('测试标题','测试描述','http://test-usercenter.hbeducloud.com:8088/api/','');
          return;
        }

        if (feature == 'location') {
          this.queryLocation();
          return;
        }

        if (feature == 'map') {
          this.openMap(window._weixin_.mLocationInfo.latitude,window._weixin_.mLocationInfo.longitude);
          return;
        }

        if (feature == 'scan') {
          this.scanQRCode();
          return;
        }

        if (feature == 'startRecord') {
          this.startRecord();
          return;
        }

        if (feature == 'stopRecord') {
          this.stopRecord();
          return;
        }

        if (feature == 'startVoice') {
          this.startVoice();
          return;
        }

        if (feature == 'pauseVoice') {
          this.pauseVoice();
          return;
        }

        if (feature == 'stopVoice') {
          this.stopVoice();
          return;
        }

        if (feature == 'uploadVoice') {
          this.uploadVoice();
          return;
        }

        if (feature == 'downloadVoice') {
          this.downloadVoice();
          return;
        }
      },

      scanQRCode() {
        wx.scanQRCode({
          needResult: 1, // 默认为0，扫描结果由微信处理，1则直接返回扫描结果，
          scanType: ["qrCode","barCode"], // 可以指定扫二维码还是一维码，默认二者都有
          success: function (res) {
            var result = res.resultStr; // 当needResult 为 1 时，扫码返回的结果
            window._weixin_.mQScanCode = result;
          }
        });
      },
      share(_title, _desc,_link,_imgUrl) {
      },
      chooseImage() {
        wx.chooseImage({
          count: 1, // 默认9
          sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
          sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
          success: function (res) {
            var localIds = res.localIds; // 返回选定照片的本地ID列表，localId可以作为img标签的src属性显示图片
            window._weixin_.mImage.mLocalId = localIds;
          }
        });
      },
      uploadImage(localId) {
        wx.uploadImage({
          localId: localId, // 需要上传的图片的本地ID，由chooseImage接口获得
          isShowProgressTips: 1, // 默认为1，显示进度提示
          success: function (res) {
            var serverId = res.serverId; // 返回图片的服务器端ID
            window._weixin_.mImage.mServiceId = serverId;
          }
        });
      },
      downloadImage(serviceId) {
        wx.downloadImage({
          serverId: serviceId, // 需要下载的图片的服务器端ID，由uploadImage接口获得
          isShowProgressTips: 1, // 默认为1，显示进度提示
          success: function (res) {
            var localId = res.localId; // 返回图片下载后的本地ID
            window._weixin_.mImage.mDownLoadId = localId;
          }
        });
      },
      queryImageById(localId) {
        wx.getLocalImgData({
          localId: localId, // 图片的localID
          success: function (res) {
            var localData = res.localData; // localData是图片的base64数据，可以用img标签显示
            let base64Str = localData.toString();
            // android do not need to add prefix, ios has include prefix base64
            /*if (base64Str.indexOf('base64') == -1) {
              base64Str = 'data:image/jpeg;base64,' + base64Str;
            }*/

            if (base64Str.indexOf('base64,') != -1) {
              base64Str = base64Str.substring(base64Str.indexOf('base64,') +7)
              //alert(base64Str);
            }

            window._weixin_.mImage.mBase64Data = base64Str;
            window._weixin_.uploadImageToServer();
          }
        });
      },
      queryLocation() {
        wx.getLocation({
          type: 'wgs84', // 默认为wgs84的gps坐标，如果要返回直接给openLocation用的火星坐标，可传入'gcj02'
          success: function (res) {
            var latitude = res.latitude; // 纬度，浮点数，范围为90 ~ -90
            var longitude = res.longitude; // 经度，浮点数，范围为180 ~ -180。
            var speed = res.speed; // 速度，以米/每秒计
            var accuracy = res.accuracy; // 位置精度
            window._weixin_.mLocationInfo = {latitude,longitude};
          }
        });
      },

      openMap(_latitude, _longitude) {
        wx.openLocation({
          latitude: _latitude, // 纬度，浮点数，范围为90 ~ -90
          longitude: _longitude, // 经度，浮点数，范围为180 ~ -180。
          name: '', // 位置名
          address: '', // 地址详情说明
          scale: 14, // 地图缩放级别,整形值,范围从1~28。默认为最大
          infoUrl: '' // 在查看位置界面底部显示的超链接,可点击跳转
        });
      },

      startRecord() {
        wx.startRecord();
      },
      stopRecord() {
        wx.stopRecord({
          success: function (res) {
            var localId = res.localId;
            window._weixin_.mVoice.mLocalId = localId;
          }
        });
      },
      startVoice() {
        wx.playVoice({
          localId: window._weixin_.mVoice.mLocalId // 需要播放的音频的本地ID，由stopRecord接口获得
        });
      },
      pauseVoice() {
        wx.pauseVoice({
          localId: window._weixin_.mVoice.mLocalId // 需要暂停的音频的本地ID，由stopRecord接口获得
        });
      },
      stopVoice() {
        wx.stopVoice({
          localId: window._weixin_.mVoice.mLocalId  // 需要停止的音频的本地ID，由stopRecord接口获得
        });
      },
      uploadVoice() {
        wx.uploadVoice({
          localId: window._weixin_.mVoice.mLocalId, // 需要上传的音频的本地ID，由stopRecord接口获得
          isShowProgressTips: 1, // 默认为1，显示进度提示
          success: function (res) {
            var serverId = res.serverId; // 返回音频的服务器端ID
            window._weixin_.mVoice.mMediaId = serverId;
          }
        });
      },
      downloadVoice() {
        wx.downloadVoice({
          serverId: window._weixin_.mVoice.mMediaId, // 需要下载的音频的服务器端ID，由uploadVoice接口获得
          isShowProgressTips: 1, // 默认为1，显示进度提示
          success: function (res) {
            var localId = res.localId; // 返回音频的本地ID
          }
        });
      },
    },
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style type="text/css" scoped>
  .test-target-item {
    float: left;width: 6rem;height: 2rem;border: 1px solid blue;margin-top: 0.5rem;margin-right: 0.5rem;text-align: center;
  }
</style>

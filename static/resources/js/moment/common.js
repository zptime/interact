/**
 * Created by ZSJ on 2017/3/31.
 */
$(function() {
    // 获取二维码
    myajax({
        url: '/api/mobile/qrcode/info',
        type: 'get'
    },function(data){
        if (data.c == 0){
            $("#qrcode").attr("src", data.d.qrcode);
        }
    });

    // 悬浮工具
    $(".aside-qrcode-btn").hover(function() {
        $(".popover").show();
    }, function() {
        $(".popover").hide();
    });

    // 左侧导航初始化及滚动控制
    resizeLeftSideBar();
    $(window).scroll(function() {
        resizeLeftSideBar();
    });

    function resizeLeftSideBar() {
        if ($(window).scrollTop() >= 326) {
            $(".left-sidebar").css("position", "fixed");
            $(".left-sidebar").css("top", "-226px");
            $(".aside-up-to-top").show();
        }else{
            $(".left-sidebar").css("position", "static");
            $(".aside-up-to-top").hide();
        }
    }
});
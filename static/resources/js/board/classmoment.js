/**
 * Created by ZSJ on 2017/5/13.
 */
$(function() {
    var SIZE_PER_PAGE = 10; // 每页动态数量

    new Vue({
        el: '#main',
        data: {
            class_id: $("#class_id").text(),
            page: '1',
            max_page: '1',
            dynamic_list: []
        },
        ready: function () {
			var self = this;

            // 圈子内容默认加载第一页
            self.queryDynamicList();

            // 圈子内容滚动加载
            $(window).scroll(function(){
                if($(document).scrollTop()>=$(document).height()-$(window).height()-500){
                    if(self.max_page != 0 && $(".load-more").css("display") == "none") {
                        if(self.page < self.max_page) {
                            // 加载更多
                            self.page++;
                            self.queryDynamicList();
                        } else {
                            // 已加载全部内容
                            $(".load-all").show();
                        }
                    }
                }
            })
        },
        methods: {
            queryDynamicList: function() {
                var self = this;

                if(self.class_id !== '') {
                    $(".load-more").show();
                    myajax({
                        url: '/api/moment/dynamics/showlist?class_id='+self.class_id
                            + '&page='+self.page
                            + '&size='+SIZE_PER_PAGE,
                        type: 'get'
                    },function(data){
                        $(".load-more").hide();

                        if (data.c == 0){
                            if(data.d.total == 0) {
                                $(".load-empty").show();
                            }

                            // 记录总页数
                            self.max_page = data.d.max_page;

                            // 追加更多内容
                            $.each(data.d.list, function(i, dynamic) {
                                dynamic.content = dynamic.content.replace(/\n/g, '<br>').replace(/\s/g, '&nbsp;');

                                $.each(dynamic.files, function(j, file) {
                                    file.file_size = convertFileSize(file.file_size);
                                });
                            });
                            self.dynamic_list = self.dynamic_list.concat(data.d.list);
                        }
                    });
                }
            },
            showImg: function(index) {
                var imgGroup = 'a[rel=group' + index + ']';
                $(imgGroup).fancybox({
                    'transitionIn'	: 'elastic',
		            'transitionOut'	: 'elastic',
                    'titlePosition' : 'over',
                    'cyclic'        : true
                });
            },
            showVideo: function(src, width, height) {
                // 视频最小宽高450,300
                if(width < 450 || height < 300) {
                    var scale = Math.min(width/450, height/300);
                    width = width/scale;
                    height = height/scale;
                }
                // 视频最大宽高720,480
                if(width > 720 || height > 480) {
                    var scale = Math.max(width/720, height/480);
                    width = width/scale;
                    height = height/scale;
                }

                layer.open({
                    type: 1,
                    area: [Number(width)+20+'px', Number(height)+20+'px'], //宽高
                    title: false,
                    content: '<video src="'+src+'" width="'+width+'" height="'+height+'" autoplay="autoplay" controls="controls"></video>'
                });
            }
        }
    })
});
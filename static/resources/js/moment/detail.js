/**
 * Created by ZSJ on 2017/3/28.
 */
$(function() {
    var moment_id = $("#moment_id").text();

    new Vue({
        el: '#main',
        data: {
            userInfo: {
                school: {}
            },
            dynamic: {}
        },
        ready: function () {
            var self = this;
            self.dynamicRead(moment_id);

            // 个人信息
            myajax({
                url: '/api/common/user/info'
            },function(data){
                if (data.c == 0){
                    self.userInfo = data.d;
                }
            });

            // 动态详情
            myajax({
                url: '/api/moment/dynamics/detail?moment_id='+moment_id,
                type: 'get'
            }, function (data) {
                if (data.c == 0) {
                    // 文本换行空格
                    data.d.content = data.d.content.replace(/\n/g, '<br>').replace(/\s/g, '&nbsp;');

                    // 文件大小
                    $.each(data.d.files, function(j, file) {
                        file.file_size = convertFileSize(file.file_size);
                    });
                    self.dynamic = data.d;
                }
            });
        },
        watch: {
            dynamic: function() {
                // 动态操作按钮hover
                $(".dynamic-del-btn").hover(function(e) {
                    $(e.target).attr("src", "/static/resources/images/icon-del-hover.png");
                }, function(e) {
                    $(e.target).attr("src", "/static/resources/images/icon-del.png");
                });
                $(".dynamic-like-btn").hover(function(e) {
                    $(e.target).attr("src", "/static/resources/images/icon-praise-hover.png");
                }, function(e) {
                    if(!$(e.target).hasClass("like")) {
                        $(e.target).attr("src", "/static/resources/images/icon-praise.png");
                    }
                });
                $(".dynamic-reply-btn").hover(function(e) {
                    $(e.target).attr("src", "/static/resources/images/icon-reply-hover.png");
                }, function(e) {
                    $(e.target).attr("src", "/static/resources/images/icon-reply.png");
                });
                $(".dynamic-reply-block").hover(function(e) {
                    $(e.target).find(".dynamic-reply-reply").show();
                }, function(e) {
                    $(e.target).find(".dynamic-reply-reply").hide();
                });
            }
        },
        methods: {
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
                    area: [width+'px', height+'px'], //宽高
                    title: false,
                    content: '<div id="container"></div>',
                    success: function(layero) {
                        // hack处理layer层中video播放器全屏样式错乱问题
                        setTimeout(function () {
                            $(layero).removeClass('layui-anim');
                        }, 0);
                    }
                });

                jwplayer("container").setup({
                    file: src,
                    width: width+"px",
                    height: height+"px",
                    autostart:true,
                    events: {}
                });
            },
            dynamicDel: function(moment_id) {
                layer.confirm(' 确认要删除这条动态吗？', {
                    icon: 3,
                    title: '提示',
                    btn: ['确定','取消']
                }, function(index){
                    layer.close(index);

                    // 删除成功处理
                    $(".dynamic#"+moment_id).hide();

                    myajax({
                        url: '/api/moment/dynamics/delete',
                        data: {
                            'moment_id': moment_id
                        }
                    });
                }, function(index){
                    layer.close(index);
                });
            },
            downloadFile: function(moment_id, file_url) {
                var self = this;
                self.dynamicRead(moment_id);

                var elemIF = document.createElement("iframe");
                elemIF.src = file_url;
                elemIF.style.display = "none";
                document.body.appendChild(elemIF);
            },
            dynamicVote: function(moment_id, vote_item_id) {
                var self = this;
                self.dynamicRead(moment_id);

                layer.confirm(' 确认投票吗？', {
                    icon: 3,
                    title: '提示',
                    btn: ['确定','取消']
                }, function(index){
                    layer.close(index);

                    // 投票成功处理
                    self.dynamic.is_vote = '1';
                    $.each(self.dynamic.vote.vote_items, function(j, vote_item) {
                        if(vote_item.vote_item_id == vote_item_id) {
                            vote_item.isvote = '1';
                            vote_item.count = Number(vote_item.count) + 1;
                        }
                    });

                    myajax({
                        url: '/api/moment/dynamics/vote',
                        data: {
                            'vote_item_id': vote_item_id
                        }
                    });
                }, function(index){
                    layer.close(index);
                });
            },
            dynamicLike: function(moment_id) {
                var self = this;
                self.dynamicRead(moment_id);

                // 对未点赞的进行点赞操作
                var $obj = $(".dynamic#"+moment_id).find(".dynamic-like-btn");
                if(!$obj.hasClass("like")) {
                    // 点赞成功处理
                    $obj.addClass("like");
                    $obj.attr("src", "/static/resources/images/icon-praise-hover.png");
                    $obj.next().text(Number($obj.next().text())+1);

                    myajax({
                        url: '/api/moment/dynamics/like',
                        data: {
                            'moment_id': moment_id
                        }
                    });
                }
            },
            dynamicReplyShow: function(e, moment_id, reply_id, reply_username) {
                var self = this;
                $obj = $(".dynamic#"+moment_id);
                $obj.find(".dynamic-reply-quick").hide();
                $obj.find(".dynamic-reply-publish").show();
                $obj.find(".dynamic-reply-publish-content").focus();
                if(reply_id != undefined) {
                    $obj.find(".dynamic-reply-publish-content").attr("id", 'ref'+reply_id).attr("placeholder", "回复"+reply_username+":");
                }

                $(document).click(function() {
                    var content = $obj.find(".dynamic-reply-publish-content").text();
                    if($.trim(content) === '') {
                        $obj.find(".dynamic-reply-publish-content").removeAttr("id").removeAttr("placeholder");
                        $obj.find(".dynamic-reply-publish-content").text("");
                        $obj.find(".dynamic-reply-quick").show();
                        $obj.find(".dynamic-reply-publish").hide();
                    }
                });

                e.stopPropagation();
            },
            dynamicReplyEdit: function(e) {
                e.stopPropagation();
            },
            dynamicReply: function(moment_id) {
                var self = this;
                self.dynamicRead(moment_id);

                $obj = $(".dynamic#"+moment_id);
                var content = $obj.find(".dynamic-reply-publish-content").text();
                var id = $obj.find(".dynamic-reply-publish-content").attr("id");
                var placeholder = $obj.find(".dynamic-reply-publish-content").attr("placeholder");
                var ref_id = '';
                var ref_name = '';
                if(id != undefined) {
                    ref_id = id.substring(3);
                    ref_name = placeholder.substring(2, placeholder.length-1);
                }

                if($.trim(content) === '') {
                    layer.msg('请输入回复内容！');
                } else {
                    // 回复成功处理
                    $obj.find(".dynamic-reply-publish-content").removeAttr("id").removeAttr("placeholder");
                    $obj.find(".dynamic-reply-publish-content").text("");
                    $obj.find(".dynamic-reply-quick").show();
                    $obj.find(".dynamic-reply-publish").hide();
                    self.dynamic.reply.push({
                        'avatar': self.userInfo.avatar,
                        'username': self.userInfo.name,
                        'ref': {'username': ref_name},
                        'content': content,
                           'create_time': '刚刚'
                    });
                    self.dynamic.reply_count = Number(self.dynamic.reply_count) + 1;

                    myajax({
                        url: '/api/moment/dynamics/reply',
                        data: {
                            'moment_id': moment_id,
                            'ref_id': ref_id,
                            'content': content
                        }
                    });
                }
            },
            dynamicRead: function(moment_id) {
                 myajax({
                    url: '/api/moment/dynamics/read',
                    data: {
                        'moment_id': moment_id
                    }
                });
            }
        }
    })
});
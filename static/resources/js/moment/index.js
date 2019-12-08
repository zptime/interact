/**
 * Created by ZSJ on 2017/3/14.
 */
$(function() {
    var MAXNUM_FOR_IMAGES = 9; // 上传照片个数限制
    var MAXNUM_FOR_VIDEOS = 1; // 上传视频个数限制
    var MAXNUM_FOR_FILES = 6; // 上传附件个数限制
    var SIZE_PER_PAGE = 10; // 每页动态数量

    // 发布动态快捷入口，默认文本
    $(".tips").click(function() {
        $('.tips').show();
        $(".vote_title").hide();
        $(".publish-text").show();
        $(".publish-vote").hide();
        $(".publish-content").slideDown();
        $(".publish-textarea").focus();
    });

    // 分享范围显示与隐藏
    $(".share-to").click(function(e) {
        $(".share-box").show();

        $(document).click(function(){
            $(".share-box").hide();
        });

        e.stopPropagation();
    });
    $(".share-box").click(function(e){
        e.stopPropagation();
    });

    new Vue({
        el: '#main',
        data: {
            userInfo: {
                clazz: []
            },
            myclass_id: '',
            tempImages: [],
            tempVideos: [],
            tempFiles: [],
            branches: [{"branch":"", "sort":1},{"branch":"", "sort":2}],
            shareToClassIds: [],
            publish: {
                content: '',
                moment_type: '0',
                image_ids: '',
                voice_ids: '',
                file_ids: '',
                vote_title: '',
                vote_num: '',
                vote_deadline: '',
                branches: '',
                is_publish_to_school: '',
                class_ids: ''
            },
            cur_circle_type: '0', //'0'表示最新动态，'1'表示学校圈，'2'表示班级圈，'3'表示个人动态
            cur_class_id: '',
            cur_moment_type: '', //空表示查询全部，'0'表示照片互动，'1'表示视频互动，'2'表示附件互动，'3'表示投票互动
            page: '1',
            max_page: '1',
            dynamic_list: []
        },
        ready: function () {
			var self = this;

            // 个人信息
            myajax({
                url: '/api/common/user/info'
            },function(data){
                if (data.c == 0){
                    self.userInfo = data.d;

                    // 查询用户类型
                    self.userInfo.user_type = getUserType(self.userInfo.user_type_id);

                    // 若是老师，则查询我是班主任的班级id
                    if(self.userInfo.user_type_id == '2') {
                        myajax({
                            url: '/api/common/myclass/list',
                            type: 'get'
                        },function(data){
                            if (data.c == 0){
                                var arr = data.d.filter(function(n) {
                                    return n.is_mentor == '1';
                                });
                                if(arr.length !== 0) {
                                    self.myclass_id = arr[0].class_id;
                                }
                            }
                        });
                    }
                }
            });

            // 上传控件初始化
            self.initUploader('uploader-image', '/api/common/upload/image', '10mb', 'image', [
                {title : "Image files", extensions : "jpg,gif,png,bmp,jpeg"}], MAXNUM_FOR_IMAGES);
            self.initUploader('uploader-video', '/api/common/upload/video', '50mb', 'video', [
                {title : "Video files", extensions : "mp4,mov"}], MAXNUM_FOR_VIDEOS);
            self.initUploader('uploader-file', '/api/common/upload/file', '50mb', 'file', [], MAXNUM_FOR_FILES);

            // 投票结束时间
            $("#finishTime").hover(function() {
                $(".finish-time").css("color", "#308ce3");
            }, function() {
                $(".finish-time").css("color", "#000");
            });

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
        watch: {
            userInfo: function() {
                // 左侧导航高度根据浏览器窗口可视区域高度自适应
                // “常用圈子”固定，“任教班级圈子”滚动
                // 无任教班级时调整常用圈子高度，有任教班级时调整任教班级圈子高度
                var self = this;
                if(self.userInfo.user_type_id !='2' || self.userInfo.clazz.length === 0) {
                    $(".common-moment").css("height", $(window).height()-120);
                } else {
                    $(".other-moment").css("height", $(window).height()-200);
                    $(".other-moment").mCustomScrollbar();
                }

                // 同时设置圈子内容高度
                $(".dynamic-area").css("min-height", $(window).height()+90);
            },
            dynamic_list: function() {
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
            initUploader: function(uploader_id, url, max_file_size, file_data_name, filters, maxnum) {
                var self = this;
                $("#"+uploader_id).plupload({
                    runtimes : 'html5,flash,silverlight,html4',
                    url : url,
                    max_file_size : max_file_size,
                    file_data_name: file_data_name,
                    filters : filters,
                    dragdrop: true,
                    views: {
                        list: true,
                        thumbs: true, // Show thumbs
                        active: 'list'
                    },
                    flash_swf_url : '/static/pub/jquery.ui.plupload/js/Moxie.swf', // Flash settings
                    silverlight_xap_url : '/static/pub/jquery.ui.plupload/js/Moxie.xap', // Silverlight settings
                    init: {
                        FilesAdded: function(up, file) {
                            // 上传文件个数限制
                            if(up.files.length > maxnum) {
                                layer.msg('文件个数超过限制！');
                                up.splice(maxnum, 999);
                                return;
                            }
                        },
                        FileUploaded: function(up, file, result) {
                            var res = JSON.parse(result.response);
                            if(uploader_id === 'uploader-image') {
                                self.tempImages.push(res.d);
                            } else if(uploader_id === 'uploader-video') {
                                // 文件大小
                                res.d.video_size = convertFileSize(res.d.video_size);
                                self.tempVideos.push(res.d);
                            } else if(uploader_id === 'uploader-file') {
                                // 文件大小
                                res.d.file_size = convertFileSize(res.d.file_size);
                                self.tempFiles.push(res.d);
                            }
                        },
                        UploadComplete: function(up, file) {
                            up.splice();
                            layer.closeAll();
                        },
                        Error: function(up, err) {
                            // 报错
                            layer.msg(err.message);
                        }
                    }
                });

                // 界面上传文件格式大小说明
                var type_tips = filters.length === 0 ? '' : '支持上传'+filters[0].extensions+'格式，';
                var size_tips = '大小不得超过'+max_file_size+'<br>';
                $("#"+uploader_id+" .plupload_droptext").prepend(type_tips + size_tips);
            },
            selectFiles: function(type) {
                var self = this;

                // 设置发布动态类型
                self.publish.moment_type = type;
                $('.tips').show();
                $(".vote_title").hide();
                $(".publish-text").show();
                $(".publish-vote").hide();
                $(".publish-content").slideDown();

                var title = '';
                if(type === '0') {
                    title = '上传照片';
                    self.tempVideos = [];
                    self.tempFiles = [];
                    $("#modal-upload>div").hide();
                    $("#uploader-image").show();
                } else if(type === '1') {
                    title = '上传视频';
                    self.tempImages = [];
                    self.tempFiles = [];
                    $("#modal-upload>div").hide();
                    $("#uploader-video").show();
                } else if(type === '2') {
                    title = '上传附件';
                    self.tempImages = [];
                    self.tempVideos = [];
                    $("#modal-upload>div").hide();
                    $("#uploader-file").show();
                }

                layer.open({
                    type: 1,
                    area: ['1100px', '504px'], //宽高
                    title: title,
                    content: $("#modal-upload")
                });
            },
            delTempFile: function(e) {
                var self = this;
                if(self.publish.moment_type === '0') {
                    $.each(self.tempImages, function(index, tempImage){
                        if(tempImage.image_id === $(e.target).attr("id")) {
                            self.tempImages.splice(index, 1);
                        }
                    });
                } else if(self.publish.moment_type === '1') {
                    self.tempVideos = [];
                } else if(self.publish.moment_type === '2') {
                    $.each(self.tempFiles, function(index, tempFile){
                        if(tempFile.file_id === $(e.target).attr("id")) {
                            self.tempFiles.splice(index, 1);
                        }
                    });
                }
            },
            showVote: function() {
                var self = this;
                self.tempImages = [];
                self.tempVideos = [];
                self.tempFiles = [];

                // 设置发布动态类型
                self.publish.moment_type = '3';
                self.publish.vote_deadline = $.nowDate(7).substring(0,16);
                $('.tips').hide();
                $(".vote_title").show();
                $(".publish-text").hide();
                $(".publish-vote").show();
                $(".publish-content").slideDown();

                // 设置默认时间为7天后
                $("#finishTime").jeDate({
                    format: 'YYYY-MM-DD hh:mm',
                    isinitVal: true,
                    initAddVal: [7],
                    choosefun: function(elem, val) {
                        self.publish.vote_deadline = val;
                    },
                    clearfun: function(elem, val) {
                        self.publish.vote_deadline = '';
                    },
                    okfun: function(elem, val) {
                        self.publish.vote_deadline = val;
                    }
                });
            },
            addVoteBranch: function() {
                var self = this;
                if(self.branches.length < 10) {
                    self.branches.push({
                        branch: '',
                        sort: self.branches.length+1
                    });
                }
            },
            delVoteBranch: function(e) {
                var self = this;
                self.branches.splice(Number($(e.target).parent().attr("id").substring(4)), 1);

                // 重新调整sort字段，与input placeholder对应
                $.each(self.branches, function(index, branch){
                    branch.sort = index+1;
                })
            },
            defaultShare: function() {
                // 分享范围默认选中当前圈子
                var self = this;
                if(self.cur_circle_type == '0' || self.cur_circle_type == '3') {
                    self.shareToClassIds = []; // 最新动态，个人动态
                } else if(self.cur_circle_type == '1') {
                    self.shareToClassIds = ['-1']; // 学校圈
                } else if(self.cur_circle_type == '2') {
                    self.shareToClassIds = [self.cur_class_id]; // 班级圈
                }
            },
            selectShare: function(class_id) {
                var self = this;
                var index = self.shareToClassIds.indexOf(class_id);
                // 添加或删除
                if(index >= 0) {
                    self.shareToClassIds.splice(index, 1);
                } else {
                    self.shareToClassIds.push(class_id);
                }
            },
            delShare: function(class_id) {
                var self = this;
                var index = self.shareToClassIds.indexOf(class_id);
                self.shareToClassIds.splice(index, 1);
            },
            publishDynamic: function() {
                var self = this;

                // 文本
                self.publish.content = $(".publish-textarea").html().replace(/<div>/g, '\n').replace(/<\/div>/g, '').replace(/&nbsp;/g, ' ');
                // 照片
                $.each(self.tempImages, function(index, tempImage){
                    self.publish.image_ids += tempImage.image_id + ',';
                });
                self.publish.image_ids = self.publish.image_ids.substring(0, self.publish.image_ids.length-1);
                // 视频
                self.publish.video_ids = self.tempVideos.length===0 ? '' : self.tempVideos[0].video_id;
                // 附件
                $.each(self.tempFiles, function(index, tempFile){
                    self.publish.file_ids += tempFile.file_id + ',';
                });
                self.publish.file_ids = self.publish.file_ids.substring(0, self.publish.file_ids.length-1);
                // 投票
                var publishBranches = [];
                $.each(self.branches, function(index, branch){
                    if(branch.branch.trim() !== '') {
                        publishBranches.push(branch);
                    }
                });
                self.publish.vote_num = publishBranches.length;
                self.publish.branches = JSON.stringify(publishBranches);
                // 分享范围
                self.publish.is_publish_to_school = self.shareToClassIds.indexOf('-1')>=0 ? '1' : '0';
                $.each(self.shareToClassIds, function(index, shareToClassId){
                    if(shareToClassId !== '-1') {
                        self.publish.class_ids += shareToClassId + ',';
                    }
                });
                self.publish.class_ids = self.publish.class_ids.substring(0, self.publish.class_ids.length-1);

                // 发布为空校验
                if(self.publish.moment_type === '0' && self.publish.content.trim() === '' && self.publish.image_ids === ''
                    || self.publish.moment_type === '1' && self.publish.content.trim() === '' && self.publish.video_ids === ''
                    || self.publish.moment_type === '2' && self.publish.content.trim() === '' && self.publish.file_ids === ''
                ) {
                    layer.msg('发布内容不能为空！');
                } else if(self.publish.moment_type === '3' && self.publish.vote_title.trim() === '') {
                    layer.msg('投票主题不能为空！');
                } else if(self.publish.moment_type === '3' && self.publish.vote_num < 2) {
                    layer.msg('投票选项不能少于2个！');
                } else if(self.publish.moment_type === '3' && self.publish.vote_deadline === '') {
                    layer.msg('投票结束时间不能为空！');
                } else {
                    var index = layer.load(2, {shade: [0.3, '#000']});
                    myajax({
                        url: '/api/moment/dynamics/publish',
                        data: self.publish
                    },function(data){
                        layer.close(index);

                        if (data.c == 0){
                            // 清空发布框内容并隐藏
                            $('.tips').show();
                            $(".vote_title").val("").hide();
                            $(".publish-textarea").html("");
                            $(".publish-content").slideUp();

                            // 重置变量
                            self.tempImages = [];
                            self.tempVideos = [];
                            self.tempFiles = [];
                            self.branches = [{"branch":"", "sort":1},{"branch":"", "sort":2}];
                            self.defaultShare();
                            self.publish = {
                                content: '',
                                moment_type: '0',
                                image_ids: '',
                                voice_ids: '',
                                file_ids: '',
                                vote_title: '',
                                vote_num: '',
                                vote_deadline: '',
                                branches: '',
                                is_publish_to_school: '',
                                class_ids: ''
                            };

                            // 发布成功，刷新圈子（默认显示全部类型）
                            layer.msg('发布成功');
                            self.cur_moment_type = '';
                            self.freshDynamicList();
                        }
                    });
                }
            },
            switchCircleType: function(e, circle_type, class_id) {
                var self = this;
                $(".moment-list li").removeClass("active");
                $(e.target).addClass("active");
                self.cur_circle_type = circle_type;
                self.cur_class_id = (class_id===undefined ? '' : class_id);
                self.defaultShare();

                // 切换圈子类型，刷新圈子（默认显示全部类型）
                self.cur_moment_type = '';
                self.freshDynamicList();
            },
            switchMomentType: function(moment_type) {
                var self = this;
                self.cur_moment_type = moment_type;

                // 切换动态类型，刷新圈子
                self.freshDynamicList();
            },
            freshDynamicList: function() {
                var self = this;
                $(".load-empty").hide();
                $(".load-all").hide();
                self.page = '1';
                self.max_page = '1';
                self.dynamic_list = [];
                self.queryDynamicList();
            },
            queryDynamicList: function() {
                var self = this;
                var param_moment_type = (self.cur_moment_type==='') ? '' : '&moment_type='+self.cur_moment_type;
                var param_class_id = (self.cur_class_id==='') ? '' : '&class_id='+self.cur_class_id;

                $(".load-more").show();
                myajax({
                    url: '/api/moment/dynamics/list?circle_type='+self.cur_circle_type
                        + param_moment_type
                        + param_class_id
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
                    width = parseInt(width/scale);
                    height = parseInt(height/scale);
                }
                // 视频最大宽高720,480
                if(width > 720 || height > 480) {
                    var scale = Math.max(width/720, height/480);
                    width = parseInt(width/scale);
                    height = parseInt(height/scale);
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
                    $.each(self.dynamic_list, function(index, dynamic) {
                       if(dynamic.moment_id == moment_id) {
                           dynamic.is_vote = '1';
                           $.each(dynamic.vote.vote_items, function(j, vote_item) {
                               if(vote_item.vote_item_id == vote_item_id) {
                                   vote_item.isvote = '1';
                                   vote_item.count = Number(vote_item.count) + 1;
                               }
                           })
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
                    $.each(self.dynamic_list, function(index, dynamic) {
                       if(dynamic.moment_id == moment_id) {
                           dynamic.reply.push({
                               'avatar': self.userInfo.avatar,
                               'username': self.userInfo.name,
                               'ref': {'username': ref_name},
                               'content': content,
                               'create_time': '刚刚'
                           });
                           dynamic.reply_count = Number(dynamic.reply_count) + 1;
                       }
                    });

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
import fetch from '../config/fetch'
import {uploadBlobImageInner,uploadFileInner} from './utils'

//const USER_CENTER = 'http://test-usercenter.hbeducloud.com:8088';
const USER_CENTER =  window.location.host.indexOf("test")!=-1? 'http://usercenter-test.hbeducloud.com':'http://usercenter.hbeducloud.com';
/**
 *测试登录
**/
export const testLogin = (username,password) => fetch('/user_center/api/login',{
  username: username,
	password: password,
},'POST');


/**
 *获取用户基本信息（不传参数则查询自身信息）
 * 用户类型（1 学生 2 老师 4 家长）
 **/
export const getUserInfo = (account_id,user_type_id,school_id) => fetch('/api/common/user/info',{
  account_id:account_id,
  user_type_id:user_type_id,
  school_id:school_id,
},'POST');


/**
 *获取当前登录用户的通讯录列表
 **/
export const getBookContact = () => fetch('/api/contacts/book/person',{
},'GET');


/**
 *获取当前登录用户的群组列表
 **/
export const getBookCluster = () => fetch('/api/contacts/book/group',{
},'GET');


/**
 *获取群组的基本信息
 **/
export const contactGroupDetail = (group_ids) => fetch('/api/contacts/group/detail',{
  group_ids:group_ids,
},'POST');


/**
 *创建群组
 **/
export const contactGroupCreate = (group_name,invite_users) => fetch('/api/contacts/group/create',{
  group_name:group_name,
  invite_users:invite_users,
},'POST');


/**
 *修改群组名称
 **/
export const contactGroupEdit = (group_id,group_name) => fetch('/api/contacts/group/edit',{
  group_id:group_id,
  group_name:group_name,
},'POST');


/**
 *邀请用户加入群组
 **/
export const contactGroupUserInvite = (group_id,invite_users) => fetch('/api/contacts/group/user/invite',{
  group_id:group_id,
  invite_users:invite_users,
},'POST');


/**
 *某群组尚可邀请的用户（新）
 **/
export const contactGroupInviteAgain = (group_id) => fetch('/api/v2/contacts/group/user/invite/available',{
  group_id:group_id
},'GET');


/**
 *获取某班级现有用户列表(包含自己)
 **/
export const contactClassUserList = (class_id) => fetch('/api/contacts/class/user/list',{
  class_id:class_id
},'POST');



/**
 *获取某群组现有用户列表(包含自己)
 **/
export const contactGroupUserList = (group_id) => fetch('/api/contacts/group/user/list',{
  group_id:group_id
},'POST');


/**
 *从群组中删除多个用户
 **/
export const contactGroupUserDel = (group_id,delete_users) => fetch('/api/contacts/group/user/delete',{
  group_id:group_id,
  delete_users:delete_users //格式：1,1,1;2,2,2;3,3,3;
},'POST');


/**
 *解散群组
 **/
export const contactGroupDissolve = (group_id) => fetch('/api/contacts/group/dissolve',{
  group_id:group_id
},'POST');


/**
 *获取一个班级的所有学生（含家长信息）
 **/
export const commonClassStudentList = (class_id) => fetch('/api/common/class/student/list',{
  class_id:class_id
},'POST');


/**
 *获取家长端收件箱
 **/
export const getNoticeList = (rows,keyword) => fetch('/api/notification/inbox',{
  rows:rows,
  read_classify:'1,2',
  type_classify:'1,2',
  keyword:keyword
},'GET');

/**
 *教师端发件箱
 **/
export const getTeacherNoticeList = (rows,keyword,last_id) => fetch('/api/notification/outbox',{
  rows:rows,
  type_classify:'1,2',
  keyword:keyword,
  last_id:last_id
},'GET');

/**
 *获取通知详情
 **/
export const getNoticeDetail= (notify_id) => fetch('/api/notification/detail',{
  notify_id:notify_id,
},'GET');


/**
 *教师端删除某个通知消息
 **/
export const deleteNotice = (notify_ids) => fetch('/api/notification/outbox/delete',{
  notify_ids:notify_ids,
},'POST');


/**
 *家长端收件箱
 **/
export const getReceiverList = (rows,keyword,last_id) => fetch('/api/notification/inbox',{
  rows:rows,
  keyword:keyword,
  last_id:last_id,
  read_classify:'0,1',
  type_classify:'1,2',
},'GET');

/**
 *删除所选，或者清空
 **/
export const deleteReceiverNotice = (notify_ids,is_clean_all) => fetch('/api/notification/inbox/delete',{
  notify_ids:notify_ids,
  is_clean_all:is_clean_all,
},'POST');


/**
 *标记已读
 **/
export const setReaded = (notify_ids) => fetch('/api/notification/read',{
  notify_ids:notify_ids
},'POST');

/**
 *标记未读
 **/
export const setUnread = (notify_ids) => fetch('/api/notification/unread',{
  notify_ids:notify_ids
},'POST');



/**
 *获取某个通知具体发送给了哪些人
 **/
export const getNoticeSendList = (notify_id) => fetch('/api/notification/receiver/detail',{
  notify_id:notify_id,
},'GET');


/**
 *获取某个通知具体发送给了哪些人
 **/
export const sendNotice = (content,voice_ids,file_ids,type,receivers) => fetch('/api/notification/publish',{
  content:content,
  file_ids:file_ids,
  type:type,
  voice_ids:voice_ids,
  receivers:receivers
},'POST');


/**
 *获取人员阅读情况
 **/
export const readList = (notify_id) => fetch('/api/notification/read/list',{
  notify_id:notify_id,
},'GET');

/**
 *提醒未读人员
 **/
export const remindUnreader = (notify_id) => fetch('/api/notification/remind',{
  notify_id:notify_id,
},'POST');




/**
 *获取本人所关联班级（该接口针对老师、学生、家长均有效）
 **/
export const getClassList = () => fetch('/api/common/user/class/list',{
},'GET');


/**
 *风采 获取圈子动态列表
 **/
export const momentDynamicList = (circle_type, class_id, last_id, rows, time_scope, keyword, moment_type) => fetch('/api/moment/dynamics/list',{
  circle_type: circle_type,
  class_id: class_id,
  last_id: last_id,
  rows: rows,
  time_scope: time_scope,
  keyword: keyword,
  moment_type: moment_type
},'GET');

/**
 *风采 获取圈子动态详情
 **/
export const momentDynamicDetail = (moment_id) => fetch('/api/moment/dynamics/detail',{
  moment_id: moment_id
},'GET');

/**
 *风采 删除圈子动态
 **/
export const momentDynamicDelete = (moment_id) => fetch('/api/moment/dynamics/delete',{
  moment_id: moment_id
},'POST');

/**
 *风采 投票圈子动态
 **/
export const momentDynamicVote = (vote_item_id) => fetch('/api/moment/dynamics/vote',{
  vote_item_id: vote_item_id
},'POST');

/**
 *风采 点赞圈子动态
 **/
export const momentDynamicLike = (moment_id) => fetch('/api/moment/dynamics/like',{
  moment_id: moment_id
},'POST');

/**
 *风采 回复圈子动态
 **/
export const momentDynamicReply = (moment_id, ref_id, content) => fetch('/api/moment/dynamics/reply',{
  moment_id: moment_id,
  ref_id: ref_id,
  content: content
},'POST');

/**
 *风采 阅读圈子动态
 **/
export const momentDynamicRead = (moment_id) => fetch('/api/moment/dynamics/read',{
  moment_id: moment_id
},'POST');

/**
 *风采 发布图片、视频、附件3类基础互动
 **/
export const publish_basic = (content,moment_type,voice_ids,image_ids,video_ids,file_ids,is_publish_to_school,class_ids) => fetch('/api/moment/dynamics/publish/basic',{
  content:content,
  moment_type:moment_type,
  voice_ids:voice_ids,
  image_ids:image_ids,
  video_ids:video_ids,
  file_ids:file_ids,
  is_publish_to_school:is_publish_to_school,
  class_ids:class_ids,
},'POST');

/**
 *风采 发布请假互动
 **/
export const publish_dayoff = (content,voice_ids,image_ids,is_visible_for_teacher,class_ids) => fetch('/api/moment/dynamics/publish/dayoff',{
  content:content,
  voice_ids:voice_ids,
  image_ids:image_ids,
  is_visible_for_teacher:is_visible_for_teacher,
  class_ids:class_ids,
},'POST');

/**
 *风采 发布评价互动
 **/
export const publish_evaluate = (content,voice_ids,image_ids,evaluate_type,evaluate_user_triples,evaluate_group_ids,evaluate_class_ids,is_visible_for_parent_related,class_ids) => fetch('/api/moment/dynamics/publish/evaluate',{
  content:content,
  voice_ids:voice_ids,
  image_ids:image_ids,
  evaluate_type:evaluate_type,
  evaluate_user_triples:evaluate_user_triples,
  evaluate_group_ids:evaluate_group_ids,
  evaluate_class_ids:evaluate_class_ids,
  is_visible_for_parent_related:is_visible_for_parent_related,
  class_ids:class_ids,
},'POST');

/**
 *风采 发布投票互动
 **/
export const publish_vote = (content,vote_title,vote_deadline,branches,is_publish_to_school,class_ids) => fetch('/api/moment/dynamics/publish/vote',{
  content:content,
  vote_title:vote_title,
  vote_deadline:vote_deadline,
  branches:branches,
  is_publish_to_school:is_publish_to_school,
  class_ids:class_ids,
},'POST');

/**
 *风采 发布投票互动
 **/
export const query_WeiXin_metaData = (sid,url) => fetch(USER_CENTER + '/wx/get/jsconfig',{
  sid:sid,
  url:url,
},'POST');

/**
 * 上传二进制文件
 */
export const uploadBlobImage = (base64Str) => uploadBlobImageInner('/api/common/upload/image','image',base64Str,'POST');

/**
 * 上传文件流
 */
export const uploadFile = (fileObj) => uploadFileInner('/api/common/upload/file','file',fileObj,'POST');

/*
* 上传音频
* */

export const uploadVoice = (media_id,duration) => fetch('/api/common/wx/voice/fetch', {
  media_id:media_id,
  duration:duration,
},'POST');

/*
* 上传视频
* */
export const uploadVideo = (videoObj) => uploadFileInner('/api/common/upload/video','video',videoObj,'POST');

/*
* 获取个人信息
* */

export const getMyInfo = () => fetch('/api/common/user/info', {

},'POST');

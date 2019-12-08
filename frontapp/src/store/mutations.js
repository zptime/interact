import {setStore, getStore} from '../config/mUtils'

import {baseUrl, imgBaseUrl} from '../config/env'

import {
  ACCOUNT,
  USER_INFO,
  USER_TYPE_ID,
  CLAZZ_LIST,
  CLASS_TARGET,
  GROUP_TARGET,
  NAV_FLAG,
  GROUP_ID,
} from './mutation-types.js'

export default {
  //登录用户
  [ACCOUNT](state, account){
    state.account = account
  },

  //用户基本信息
  [USER_INFO](state, user_info){
    state.user_info = user_info
  },

  //用户类型ID  1 学生 2 老师 4 家长
  [USER_TYPE_ID](state, user_type_id){
    state.user_type_id = user_type_id
  },

  //班级列表
  [CLAZZ_LIST](state, clazz_list){
    state.clazz_list = clazz_list
  },

  //班级-通知（评价）对象列表
  [CLASS_TARGET](state, class_target){
    state.class_target = class_target
  },

  //小组-通知（评价）对象列表
  [GROUP_TARGET](state, group_target){
    state.group_target = group_target
  },

  //首页-导航ID，1-联系人，2-小组
  [NAV_FLAG](state, nav_flag){
    state.nav_flag = nav_flag
  },

  //小组ID
  [GROUP_ID](state, group_id){
    state.group_id = group_id
  },

}

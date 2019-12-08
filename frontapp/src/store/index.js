import Vue from 'vue'
import Vuex from 'vuex'
import mutations from './mutations'
import actions from './action'
import getters from './getters'

Vue.use(Vuex)

const state = {
  account:{}, //登录用户
  user_info:{},//用户基本信息
  user_type_id:'',//用户类型
  clazz_list:[],//当前登录用户的班级列表
  class_target:[],//班级-通知（评价）对象列表
  group_target:[],//小组-通知（评价）对象列表
  nav_flag:1,//通讯录首页-导航Id，1-联系人，2-小组
  group_id:'',//小组ID
  env : {
    os : '',
    process: '',
    signUrl:'',
    sid:'',
  },
}

export default new Vuex.Store({
	state,
	getters,
	actions,
	mutations,
})
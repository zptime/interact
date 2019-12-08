const home = r => require.ensure([], () => r(require('../page/Home')), 'home')

/*首页*/
const homePage = r => require.ensure([], () => r(require('../page/home/HomePage')), 'homePage')

/*通讯录*/
const phoneList = r => require.ensure([], () => r(require('../page/phone/List')), 'phoneList')
const phoneClusterAdd = r => require.ensure([], () => r(require('../page/phone/ClusterAdd')), 'phoneClusterAdd')
const phoneClusterDetail = r => require.ensure([], () => r(require('../page/phone/ClusterDetail')), 'phoneClusterDetail')
const phoneClusterEdit = r => require.ensure([], () => r(require('../page/phone/ClusterEdit')), 'phoneClusterEdit')
const choosePerson = r => require.ensure([], () => r(require('../page/phone/ChoosePerson.vue')), 'choosePerson')
const choosePersonTest = r => require.ensure([], () => r(require('../components/m-member/others/ChoosePersonTest.vue')), 'choosePersonTest')
const chooseTargetTest = r => require.ensure([], () => r(require('../components/m-member/others/ChooseTargetTest.vue')), 'chooseTargetTest')

/*消息通知*/
const noticeList = r => require.ensure([], () => r(require('../page/notice/parent/List')), 'noticeList')
const teachernoticeList = r => require.ensure([], () => r(require('../page/notice/teacher/List')), 'teachernoticeList')
const noticeDetail = r => require.ensure([], () => r(require('../page/notice/parent/Detail')), 'noticeDetail')
const teachernoticeDetail = r => require.ensure([], () => r(require('../page/notice/teacher/Detail')), 'teachernoticeDetail')
const teachernoticeSend = r => require.ensure([], () => r(require('../page/notice/teacher/Send')), 'teachernoticeSend')
const teachernoticeHasSend = r => require.ensure([], () => r(require('../page/notice/teacher/HasSend')), 'teachernoticeHasSend')
const noticePersonSelect = r => require.ensure([], () => r(require('../page/notice/teacher/choosePerson')), 'noticePersonSelect')
const noticeRead = r => require.ensure([], () => r(require('../page/notice/teacher/read')), 'noticeRead')

/*圈子*/
const momentList = r => require.ensure([], () => r(require('../page/moment/List')), 'momentList')
const momentClassList = r => require.ensure([], () => r(require('../page/moment/ClassList')), 'momentClassList')
const momentMyList = r => require.ensure([], () => r(require('../page/moment/MyList')), 'momentMyList')
const momentDetail = r => require.ensure([], () => r(require('../page/moment/Detail')), 'momentDetail')
const momentPublishCommon = r => require.ensure([], () => r(require('../page/moment/PublishCommon')), 'momentPublishCommon')
const momentPublishEvaluate = r => require.ensure([], () => r(require('../page/moment/PublishEvaluate')), 'momentPublishEvaluate')

/*个人中心*/
const personalHome = r => require.ensure([], () => r(require('../page/personal/parent/home')), 'personaHome')
const personalSwitch = r => require.ensure([], () => r(require('../page/personal/parent/switch')), 'personalSwitch')
const personalFamily = r => require.ensure([], () => r(require('../page/personal/parent/family')), 'personalFamily')
const personalInvite = r => require.ensure([], () => r(require('../page/personal/parent/invite')), 'personalInvite')
const personalInformation = r => require.ensure([], () => r(require('../page/personal/parent/information')), 'personalInformation')

const testLogin = r => require.ensure([], () => r(require('../test/TestLogin')), 'testLogin')
/* Wei Xin test*/
const weixinTest = r => require.ensure([], () => r(require('../page/weixin/WeiXinTest')), 'weixinTest')

const defaultPath = () =>  process.env.NODE_ENV == 'development'? 'homePage': 'home'

const m = {
  template: `<div>
        <keep-alive>
            <router-view v-if="$route.meta.keepAlive">
            </router-view>
        </keep-alive>
        <router-view v-if="!$route.meta.keepAlive"></router-view>
    </div>`
}

export default [
    {
        path: '',
        redirect:  '/m'
    },
    {
        path: '/m',
        component: m,
        children: [
            //地址为空时跳转home页面
            {
                path: '',
                redirect: defaultPath
            },
            //home页
            {
                name: 'homePage',
                path: 'homePage',
                component: homePage
            },
            //通讯录
            {
              path: 'phone',
              component: m,
              children: [
                {
                  path: '',
                  redirect: 'phoneList'
                },
                {//列表页
                  name:'phoneList',
                  path: 'phoneList',
                  component: phoneList
                },
                {//创建小组页
                  name:'phoneClusterAdd',
                  path: 'phoneClusterAdd',
                  component: phoneClusterAdd
                },
                {//小组详情页
                  name:'phoneClusterDetail',
                  path: 'phoneClusterDetail',
                  component: phoneClusterDetail
                },
                {//小组编辑页
                  name:'phoneClusterEdit',
                  path: 'phoneClusterEdit',
                  component: phoneClusterEdit
                },
                {//通讯录-选择人员页
                  name:'choosePerson',
                  path: 'choosePerson',
                  component: choosePerson
                },
                {//通讯录-选择人员-测试页
                  name:'choosePersonTest',
                  path: 'choosePersonTest',
                  component: choosePersonTest
                },
                {//选择通知（评价）对象-测试页
                  name:'chooseTargetTest',
                  path: 'chooseTargetTest',
                  component: chooseTargetTest
                },
              ]
            },
            //通知教师端（班级通知）
            {
              path: 'notice',
              component: m,
              children: [
                {
                  path: '',
                  redirect: 'teacher/noticeList'
                },
                {//列表页
                  name:'noticeList',
                  path: 'parent/noticeList',
                  component: noticeList
                },
                {//详情页
                  name:'noticeDetail',
                  path: 'parent/noticeDetail',
                  component: noticeDetail
                },
                {//教师端列表页
                  name:'teachernoticeList',
                  path: 'teacher/noticeList',
                  component: teachernoticeList
                },
                {//教师端详情页
                  name:'teachernoticeDetail',
                  path: 'teacher/noticeDetail',
                  component: teachernoticeDetail
                },
                {//教师端发通知
                  name:'teachernoticeSend',
                  path: 'teacher/noticeSend',
                  component: teachernoticeSend
                },
                {//教师端已发通知
                  name:'teachernoticeHasSend',
                  path: 'teacher/HasSend',
                  component: teachernoticeHasSend
                },
                {//教师端接受通知的人
                  name:'noticePersonSelect',
                  path: 'teacher/person_select',
                  component: noticePersonSelect
                },
                {//查看阅读人员情况
                  name:'noticeRead',
                  path: 'teacher/read',
                  component: noticeRead
                },

              ]
            },
            //通知教师端（班级通知）
            {
              path: 'notice_parent',
              redirect: 'notice/parent/noticeList',
            },
            //圈子（空间）
            {
              path: 'moment',
              component: m,
              children: [
                {
                  path: '',
                  redirect: 'momentList'
                },
                {//风采列表页
                  name:'momentList',
                  path: 'momentList',
                  component: momentList
                },
                {//班级风采列表页
                  name:'momentClassList',
                  path: 'momentClassList',
                  component: momentClassList
                },
                {//个人风采列表页
                  name:'momentMyList',
                  path: 'momentMyList',
                  component: momentMyList
                },
                {//风采详情页
                  name:'momentDetail',
                  path: 'momentDetail',
                  component: momentDetail
                },
                {//发风采、请假
                  name:'momentPublishCommon',
                  path: 'momentPublishCommon',
                  component: momentPublishCommon
                },
                {//发评价
                  name:'momentPublishEvaluate',
                  path: 'momentPublishEvaluate',
                  component: momentPublishEvaluate
                },
              ]
            },
            //个人中心
            {
              path: 'personal',
              component: m,
              children: [
                {
                  path: '',
                  redirect: 'parent/home'
                },
                {//主页
                  name:'personalHome',
                  path: 'parent/home',
                  component: personalHome
                },
                {//选择角色
                  name:'personalSwitch',
                  path: 'parent/switch',
                  component: personalSwitch
                },
                {//选择角色
                  name:'personalFamily',
                  path: 'parent/family',
                  component: personalFamily
                },
                {//邀请家庭成员
                  name:'personalInvite',
                  path: 'parent/invite',
                  component: personalInvite
                },
                {//邀请家庭成员
                  name:'personalInformation',
                  path: 'parent/information',
                  component: personalInformation
                },
              ]
            },
            //登录测试地址
            {
                path: 'test',
                component: m,
                children: [
                    {
                        path: '',
                        redirect: 'testLogin'
                    },
                    {
                        path: 'testLogin',
                        component: testLogin
                    }
                ]
            },
          {
            path: 'weixin',
            component: weixinTest,
          }
        ]
    }
]

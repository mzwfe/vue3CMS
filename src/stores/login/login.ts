import { defineStore } from 'pinia'
import { accountLogin, getUserInfoById, getUserMenuByRoleId } from '@/service/login/login'
import type { IAccount } from '@/views/LoginView/types'
import { localCache } from '@/utils/cache'
import router from '@/router'
import { LOGIN_TOKEN } from '@/global/constance'
import { mapMenuListToPermissions, mapMenusToRoutes } from '@/utils/map-menus'
import useHomeStore from '../home/home'

interface ILoginState {
  token: string
  userInfo: any
  userMenus: any
  permissions: string[]
}

const useLoginStore = defineStore('login', {
  state: (): ILoginState => ({
    token: '',
    userInfo: {},
    userMenus: [],
    permissions: []
  }),
  actions: {
    async accountLoginAction(account: IAccount) {
      // 1.登陆账号, 获取token
      const loginRes: any = await accountLogin(account)
      const id = loginRes.data.id
      const name = loginRes.data.name
      this.token = loginRes.data.token
      // 此处先存储token, 否则下文无法获取token
      localCache.setCache(LOGIN_TOKEN, this.token)

      // 2.获取用户详细信息
      const userInfoRes: any = await getUserInfoById(id)
      this.userInfo = userInfoRes.data
      // 3.获取用户菜单
      const userMenuRes: any = await getUserMenuByRoleId(this.userInfo.role.id)
      this.userMenus = userMenuRes.data

      // 4.本地缓存
      localCache.setCache('userInfo', this.userInfo)
      localCache.setCache('userMenus', this.userMenus)

      // 5.请求所有roles和departments
      const homeStore = useHomeStore()
      homeStore.getEntireDataAction()

      // 获取登录用户的所有按钮的权限
      const permissions: string[] = mapMenuListToPermissions(this.userMenus)
      this.permissions = permissions

      // 6.根据菜单映射路由
      const routes = mapMenusToRoutes(this.userMenus)
      routes.forEach((route) => router.addRoute('main', route))

      // 7.跳转首页
      router.push('/main')
    },
    loadLocalCacheAction() {
      // 用户刷新默认加载数据操作
      const token = localCache.getCache(LOGIN_TOKEN)
      const userInfo = localCache.getCache('userInfo')
      const userMenus = localCache.getCache('userMenus')
      if (token && userInfo && userMenus) {
        this.token = token
        this.userInfo = userInfo
        this.userMenus = userMenus

        // 请求所有roles和departments
        const homeStore = useHomeStore()
        homeStore.getEntireDataAction()

        // 获取按钮权限
        const permissions: string[] = mapMenuListToPermissions(this.userMenus)
        this.permissions = permissions

        // 动态添加路由
        const routes = mapMenusToRoutes(this.userMenus)
        routes.forEach((route) => router.addRoute('main', route))
      }
    }
  }
})

export default useLoginStore

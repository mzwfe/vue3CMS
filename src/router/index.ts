import { LOGIN_TOKEN } from '@/global/constance'
import { localCache } from '@/utils/cache'
import { firstMenu } from '@/utils/map-menus'
import { createRouter, createWebHashHistory } from 'vue-router'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      redirect: '/main'
    },
    {
      path: '/:pathMatch(.*)',
      component: () => import('../views/NotFound/NotFound.vue')
    },
    {
      path: '/login',
      component: () => import('../views/LoginView/LoginView.vue')
    },
    {
      path: '/main',
      name: 'main',
      component: () => import('../views/HomeView/HomeView.vue')
    }
  ]
})
// 1.动态获取所有路由

// 2.动态添加路由

// 导航守卫
router.beforeEach((to, from) => {
  const token = localCache.getCache(LOGIN_TOKEN)
  if (to.path !== '/login' && !token) return '/login'
  if (to.path === '/main' && token) return firstMenu.url
})

export default router

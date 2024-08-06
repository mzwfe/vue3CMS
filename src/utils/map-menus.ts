import type { RouteRecordRaw } from 'vue-router'

/**
 * 获取本地所有路由
 */
function loadLocalRoutes() {
  // 5.动态添加路由
  // 1.1.读取所有路由
  const localRoutes: RouteRecordRaw[] = []
  const files: Record<string, any> = import.meta.glob('@/router/home/**/*.ts', {
    eager: true
  })
  for (const key in files) {
    const module = files[key]
    localRoutes.push(module.default)
  }

  return localRoutes
}

export let firstMenu: any = null
// firstMenu.url
/**
 * 根据菜单匹配路由
 * @param userMenus 根据id拿到的所有菜单
 * @returns 路由对象数组
 */
export function mapMenusToRoutes(userMenus: any[]) {
  // 1.加载本地路由
  const localRoutes = loadLocalRoutes()
  // 根据菜单映射路由
  const routes: RouteRecordRaw[] = []
  for (const menu of userMenus) {
    for (const submenu of menu.children) {
      const route = localRoutes.find((item) => item.path === submenu.url)
      if (route) {
        // 1.给顶层菜单实现重定向功能
        if (!routes.find((item) => item.path === menu.url)) {
          routes.push({ path: menu.url, redirect: route.path })
        }
        routes.push(route)
      }
      // 记录第一个被匹配到的菜单
      if (!firstMenu && route) firstMenu = submenu
    }
  }
  return routes
}
/**
 * 根据路径匹配需要显示的菜单
 * @param path 需要匹配的路径
 * @param userMenus 所有菜单
 */
export function mapPathToMenu(path: string, userMenus: any[]) {
  for (const menu of userMenus) {
    for (const submenu of menu.children) {
      if (submenu.url === path) {
        return submenu
      }
    }
  }

  return undefined
}

interface breadcrumbs {
  name: string
  path: string
}
/**
 * 根据路径匹配到面包屑所需要的菜单对象
 * @param path 需要匹配的路径
 * @param userMenus 所有菜单
 */
export function mapPathToBreadcrumbs(path: string, userMenus: any[]) {
  // 定义面包屑
  const breadcrumbs: breadcrumbs[] = []

  // 遍历菜单获取数据
  for (const menu of userMenus) {
    for (const submenu of menu.children) {
      if (submenu.url === path) {
        breadcrumbs.push({ name: menu.name, path: menu.url })
        breadcrumbs.push({ name: submenu.name, path: submenu.url })
      }
    }
  }
  return breadcrumbs
}

/**
 * 将菜单映射成id列表
 * @param menuList 菜单列表
 * @return id列表
 */
export function mapMenusToIds(menuList: any[]) {
  const ids: number[] = []
  function recurseGetId(menus: any[]) {
    for (const menu of menus) {
      if (menu.children) {
        recurseGetId(menu.children)
      } else {
        ids.push(menu.id)
      }
    }
  }
  recurseGetId(menuList)

  return ids
}

/**
 * 将菜单映射成权限列表
 * @param menuList 菜单列表
 * @return 权限数组(字符串数组)
 */
export function mapMenuListToPermissions(menuList: any[]) {
  const permissions: string[] = []

  function recurseGetPermission(menus: any[]) {
    for (const menu of menus) {
      if (menu.type === 3) {
        permissions.push(menu.permission)
      } else {
        recurseGetPermission(menu.children ?? [])
      }
    }
  }

  recurseGetPermission(menuList)

  return permissions
}

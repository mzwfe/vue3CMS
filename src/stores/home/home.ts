import { defineStore } from 'pinia'
import type { HomeState } from './type'
import { getEntireDepartments, getEntireMenus, getEntireRoles } from '@/service/home/home'

const useHomeStore = defineStore('home', {
  state: (): HomeState => ({
    entireRoles: [],
    entireDepartments: [],
    entireMenus: []
  }),
  actions: {
    async getEntireDataAction() {
      const roles: any = await getEntireRoles()
      const departments: any = await getEntireDepartments()
      const menus: any = await getEntireMenus()
      this.entireRoles = roles.data.list
      this.entireDepartments = departments.data.list
      this.entireMenus = menus.data.list
    }
  }
})

export default useHomeStore

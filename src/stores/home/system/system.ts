import {
  deletePageDataById,
  deleteUser,
  editPageData,
  editUserData,
  newPageData,
  newUserData,
  postPageListData,
  postUsersList
} from '@/service/home/system/system'
import { defineStore } from 'pinia'
import type { ISystemState } from './type'
import useHomeStore from '../home'

const useSystemStore = defineStore('system', {
  state: (): ISystemState => ({
    usersList: [],
    totalCount: 0,
    pageList: [],
    pageTotalCount: 0
  }),
  actions: {
    async postUsersListAction(queryInfo: any) {
      const usersList: any = await postUsersList(queryInfo)
      this.usersList = usersList?.data?.list
      this.totalCount = usersList?.data?.totalCount
    },
    async deleteUserByIdAction(id: number) {
      const res = await deleteUser(id)
    },

    async newUserDataAction(userInfo: any) {
      const res = await newUserData(userInfo)
      this.postUsersListAction({ offset: 0, size: 10 })
    },
    async editUserDataAction(id: number, userInfo: any) {
      const res = await editUserData(id, userInfo)
      this.postUsersListAction({ offset: 0, size: 10 })
    },

    /** 针对页面数据: 增删改查 */
    async postPageListAction(pageName: string, queryInfo: any) {
      const pageListRes: any = await postPageListData(pageName, queryInfo)
      const { totalCount, list } = pageListRes.data
      this.pageList = list
      this.pageTotalCount = totalCount
    },
    async deletePageDataByIdAction(pageName: string, id: number) {
      const deleteRes = await deletePageDataById(pageName, id)
      // 获取完整数据
      const homeStore = useHomeStore()
      homeStore.getEntireDataAction()
    },
    async newPageDataAction(pageName: string, newData: any) {
      const newRes = await newPageData(pageName, newData)
      this.postPageListAction(pageName, { offset: 0, size: 10 })
      // 获取完整数据
      const homeStore = useHomeStore()
      homeStore.getEntireDataAction()
    },
    async editPageDataAction(pageName: string, id: number, pageInfo: any) {
      const editRes = await editPageData(pageName, id, pageInfo)
      this.postPageListAction(pageName, { offset: 0, size: 10 })

      // 获取完整数据
      const homeStore = useHomeStore()
      homeStore.getEntireDataAction()
    }
  }
})

export default useSystemStore

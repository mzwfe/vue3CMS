import { zwRequest2 } from '@/service'

// 用户的网络请求
export function postUsersList(queryInfo: any) {
  return zwRequest2.post({
    url: '/users/list',
    data: queryInfo
  })
}

export function deleteUser(id: number) {
  return zwRequest2.delete({
    url: `/users/${id}`
  })
}

export function newUserData(userInfo: any) {
  return zwRequest2.post({
    url: '/users',
    data: userInfo
  })
}

export function editUserData(id: number, userInfo: any) {
  return zwRequest2.patch({
    url: `/users/${id}`,
    data: userInfo
  })
}

/** 针对页面的网络请求: 增删改查 */
export function postPageListData(pageName: string, queryInfo: any) {
  return zwRequest2.post({
    url: `/${pageName}/list`,
    data: queryInfo
  })
}

export function deletePageDataById(pageName: string, id: number) {
  return zwRequest2.delete({
    url: `/${pageName}/${id}`
  })
}

export function newPageData(pageName: string, newData: any) {
  return zwRequest2.post({
    url: `/${pageName}`,
    data: newData
  })
}

export function editPageData(pageName: string, id: number, editData: any) {
  return zwRequest2.patch({
    url: `/${pageName}/${id}`,
    data: editData
  })
}

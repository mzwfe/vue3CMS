import type { IAccount } from '@/views/LoginView/types'
import { zwRequest, zwRequest2 } from '@/service'
export function accountLogin(account: IAccount) {
  return zwRequest.post({
    url: 'login',
    data: {
      name: account.name,
      password: account.password
    }
  })
}

export function getUserInfoById(id: number) {
  return zwRequest2.get({
    url: `/users/${id}`
  })
}

export function getUserMenuByRoleId(id: number) {
  return zwRequest2.get({
    url: `/role/${id}/menu`
  })
}

import { zwRequest2 } from '..'

export function getEntireRoles() {
  return zwRequest2.post({
    url: '/role/list'
  })
}

export function getEntireDepartments() {
  return zwRequest2.post({
    url: '/department/list'
  })
}

export function getEntireMenus() {
  return zwRequest2.post({
    url: '/menu/list'
  })
}

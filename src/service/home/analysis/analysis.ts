import { zwRequest2 } from '@/service'

export function getAmountListData() {
  return zwRequest2.get({
    url: '/goods/amount/list'
  })
}

export function getGoodsCategoryCount() {
  return zwRequest2.get({
    url: '/goods/category/count'
  })
}

export function getGoodsSaleCount() {
  return zwRequest2.get({
    url: '/goods/category/sale'
  })
}

export function getGoodsFavorCount() {
  return zwRequest2.get({
    url: '/goods/category/favor'
  })
}

export function getGoodsAddressCount() {
  return zwRequest2.get({
    url: '/goods/address/sale'
  })
}

import {
  getAmountListData,
  getGoodsAddressCount,
  getGoodsCategoryCount,
  getGoodsFavorCount,
  getGoodsSaleCount
} from '@/service/home/analysis/analysis'
import { defineStore } from 'pinia'

interface IAnalysisState {
  amountList: any[]
  goodsCategoryCount: any[]
  goodsSaleCount: any[]
  goodsFavorCount: any
  goodsAddressCount: any[]
}
const useAnalysisStore = defineStore('analysis', {
  state: (): IAnalysisState => ({
    amountList: [],
    goodsCategoryCount: [],
    goodsSaleCount: [],
    goodsFavorCount: [],
    goodsAddressCount: []
  }),
  actions: {
    async fetchAnalysisDataAction() {
      const amount: any = await getAmountListData()
      const goodsCategoryCount: any = await getGoodsCategoryCount()
      const goodsSaleCount: any = await getGoodsSaleCount()
      const goodsFavorCount: any = await getGoodsFavorCount()
      const goodsAddressCount: any = await getGoodsAddressCount()
      this.amountList = amount.data
      this.goodsCategoryCount = goodsCategoryCount.data
      this.goodsSaleCount = goodsSaleCount.data
      this.goodsFavorCount = goodsFavorCount.data
      this.goodsAddressCount = goodsAddressCount.data
    }
  }
})

export default useAnalysisStore

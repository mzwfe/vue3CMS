<script setup lang="ts">
import useAnalysisStore from '@/stores/home/analysis/analysis'
import CountCard from './c-cpns/CountCard.vue'
import ChartCard from './c-cpns/ChartCard.vue'
import { storeToRefs } from 'pinia'

import PieEchart from '@/components/PageEchart/src/PieEchart.vue'
import LineEchart from '@/components/PageEchart/src/LineEchart.vue'
import RoseEchart from '@/components/PageEchart/src/RoseEchart.vue'
import BarEchart from '@/components/PageEchart/src/BarEchart.vue'
import MapEchart from '@/components/PageEchart/src/MapEchart.vue'

import { computed } from 'vue'

// 发起请求
const analysisStore = useAnalysisStore()
analysisStore.fetchAnalysisDataAction()

// 从store获取数据
const { amountList, goodsCategoryCount, goodsSaleCount, goodsFavorCount, goodsAddressCount } =
  storeToRefs(analysisStore)

const showGoodsCategoryCount = computed(() => {
  return goodsCategoryCount.value.map((item: any) => ({
    name: item.name,
    value: item.goodsCount
  }))
})

const showGoodsSaleCount = computed(() => {
  const values = goodsSaleCount.value.map((item: any) => item.goodsCount)
  const labels = goodsSaleCount.value.map((item: any) => item.name)
  return {
    labels,
    values
  }
})

const showGoodsFavorCount = computed(() => {
  const values = goodsFavorCount.value.map((item: any) => item.goodsFavor)
  const labels = goodsFavorCount.value.map((item: any) => item.name)
  return {
    labels,
    values
  }
})

const showGoodsAddressCount = computed(() => {
  return goodsAddressCount.value.map((item: any) => ({
    name: item.address,
    value: item.count
  }))
})
</script>

<template>
  <div class="dashboard">
    <el-row :gutter="10">
      <template v-for="item in amountList" :key="item">
        <el-col :span="6" :xs="24" :sm="12" :md="6">
          <count-card v-bind="item"></count-card>
        </el-col>
      </template>
    </el-row>
    <el-row :gutter="10">
      <el-col :span="7">
        <chart-card :header="'分类产品数量'">
          <pie-echart :data="showGoodsCategoryCount"></pie-echart>
        </chart-card>
      </el-col>
      <el-col :span="10">
        <chart-card :header="'不同城市销量'">
          <map-echart :map-data="showGoodsAddressCount"></map-echart>
        </chart-card>
      </el-col>
      <el-col :span="7">
        <chart-card :header="'分类产品数量(玫瑰图)'">
          <rose-echart :data="showGoodsCategoryCount"></rose-echart>
        </chart-card>
      </el-col>
    </el-row>
    <el-row :gutter="10">
      <el-col :span="12">
        <chart-card :header="'产品销售数量'">
          <line-echart v-bind="showGoodsSaleCount"></line-echart>
        </chart-card>
      </el-col>
      <el-col :span="12">
        <chart-card :header="'产品收藏数量'">
          <bar-echart v-bind="showGoodsFavorCount"></bar-echart>
        </chart-card>
      </el-col>
    </el-row>
  </div>
</template>

<style lang="less" scoped>
.el-row {
  margin-bottom: 10px;
}
</style>

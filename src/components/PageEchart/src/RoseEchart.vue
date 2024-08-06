<script setup lang="ts">
import { computed } from 'vue'
import BaseEchart from './BaseEchart.vue'
import type { EChartsOption } from 'echarts'

interface IProps {
  data: { name: string; value: number }[]
}

const props = defineProps<IProps>()
const option = computed<EChartsOption>(() => {
  return {
    legend: {
      show: false
    },
    tooltip: {
      trigger: 'item'
    },
    toolbox: {
      show: true,
      feature: {
        mark: { show: true },
        dataView: { show: true, readOnly: false },
        restore: { show: true },
        saveAsImage: { show: true }
      }
    },
    series: [
      {
        name: '类别 销量',
        type: 'pie',
        radius: [10, 150],
        center: ['50%', '50%'],
        roseType: 'area',
        itemStyle: {
          borderRadius: 8
        },
        data: props.data
      }
    ]
  }
})
</script>

<template>
  <div class="rose-echart">
    <base-echart :option="option"></base-echart>
  </div>
</template>

<style lang="less" scoped></style>

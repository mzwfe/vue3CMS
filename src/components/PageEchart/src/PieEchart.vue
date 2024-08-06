<script setup lang="ts">
import { computed, ref } from 'vue'
import BaseEchart from './BaseEchart.vue'
import type { EChartsOption } from 'echarts'

interface IProps {
  data: { name: string; value: number }[]
}

const props = defineProps<IProps>()
const option = computed<EChartsOption>(() => {
  return {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'horizontal',
      left: 'left'
    },
    series: [
      {
        name: '类别 数量',
        type: 'pie',
        radius: '60%',
        data: props.data,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
})
</script>

<template>
  <div class="pie-echart">
    <base-echart :option="option"></base-echart>
  </div>
</template>

<style lang="less" scoped></style>

<script setup lang="ts">
import BaseEchart from '@/components/PageEchart/src/BaseEchart.vue'
import type { EChartsOption } from 'echarts'

const data = {
  name: 'vueCMS',
  children: [
    { name: 'vue3' },
    { name: 'pinia' },
    { name: 'vue router' },
    { name: 'TypeScript' },
    { name: 'Element Plus' },
    { name: 'ECharts' },
    { name: 'wangEditor5' },
    { name: 'Dayjs' },
    { name: 'vite' },
    { name: 'prettier' },
    { name: 'ESlint' }
  ]
}
const option: EChartsOption = {
  tooltip: {
    trigger: 'item',
    triggerOn: 'mousemove'
  },
  series: [
    {
      type: 'tree',
      id: 0,
      name: 'tree1',
      data: [data],
      top: '0%',
      left: '25%',
      bottom: '0%',
      right: '65%',
      height: '100%',
      symbolSize: 18,
      edgeShape: 'polyline',
      edgeForkPosition: '63%',
      initialTreeDepth: 3,
      lineStyle: {
        width: 6,
        color: 'gray'
      },
      label: {
        position: 'left',
        verticalAlign: 'middle',
        align: 'right',
        fontSize: 16,
        textBorderWidth: 1,
        textBorderColor: '#000',
        padding: 4
      },
      leaves: {
        label: {
          position: 'right',
          verticalAlign: 'middle',
          align: 'left'
        }
      },
      emphasis: {
        focus: 'descendant'
      }
    }
  ]
}
</script>

<template>
  <div class="tree-echart">
    <base-echart :option="option"></base-echart>
  </div>
</template>

<style lang="less" scoped>
.tree-echart {
  box-sizing: border-box;
  padding-top: 15vh;
  height: 100%;
  :deep(.base-echart) {
    height: 100%;
  }
}
</style>

<script setup lang="ts">
import * as echarts from 'echarts'
import { onMounted, onUnmounted, ref, watchEffect } from 'vue'
import type { EChartsOption } from 'echarts'
import ChinaJson from '@/components/PageEchart/data/china.json'
import type { GeoJSONSourceInput } from 'echarts/types/src/coord/geo/geoTypes.js'

interface IProps {
  option: EChartsOption
}
const props = defineProps<IProps>()

// 注册地图
echarts.registerMap('china', ChinaJson as GeoJSONSourceInput)

const echartRef = ref<HTMLElement>()
onMounted(() => {
  const myChart = echarts.init(echartRef.value, 'light', { renderer: 'canvas' })

  // 2.第一次进行setOption
  // watchEffect监听option变化, 重新执行
  // watchEffect: 立即运行一个函数，同时响应式地追踪其依赖，并在依赖更改时重新执行
  watchEffect(() => myChart.setOption(props.option))

  // 3.监听window缩放
  window.addEventListener('resize', () => {
    myChart.resize()
  })
})
</script>

<template>
  <div class="base-echart">
    <div class="echart" ref="echartRef"></div>
  </div>
</template>

<style lang="less" scoped>
.echart {
  height: 400px;
  // background-color: #fff;
}
</style>

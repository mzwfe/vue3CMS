<script setup lang="ts">
import { CountUp } from 'countup.js'
import { onMounted, ref } from 'vue'
interface IProps {
  title: string
  tips: string
  number1: number
  number2: number
  amount: string
  subtitle: string
}

const props = withDefaults(defineProps<IProps>(), {
  title: '这是销量',
  tips: '你好',
  number1: 100,
  number2: 100,
  amount: '',
  subtitle: ''
})

// 创建CountUp实例
const countRef1 = ref<HTMLSpanElement>()
const countRef2 = ref<HTMLSpanElement>()
const countOption = {
  prefix: props.amount === 'saleroom' ? '￥' : '',
  duration: 0.8
}
onMounted(() => {
  const countUp1 = new CountUp(countRef1.value!, props.number1, countOption)
  countUp1.start()

  const countUp2 = new CountUp(countRef2.value!, props.number2, countOption)
  countUp2.start()
})
</script>

<template>
  <div class="count-card">
    <div class="header">
      <span class="title">{{ title }}</span>
      <el-tooltip :content="tips" placement="top" effect="light">
        <el-icon>
          <Warning />
        </el-icon>
      </el-tooltip>
    </div>
    <div class="content">
      <span ref="countRef1" class="count1">{{ number1 }}</span>
    </div>
    <div class="footer">
      <span>{{ subtitle }}: </span>
      <span ref="countRef2" class="count2">{{ number2 }}</span>
    </div>
  </div>
</template>

<style lang="less" scoped>
.count-card {
  display: flex;
  height: 120px;
  flex-direction: column;
  align-items: center;
  border-radius: 16px;
  background-color: #fff;
  padding: 10px 40px 10px 40px;

  .header {
    display: flex;
    justify-content: space-between;
    width: 100%;
    height: 30px;
    color: gray;
    padding-top: 14px;
  }

  .content {
    box-sizing: border-box;
    width: 100%;
    font-size: 30px;
    margin-bottom: 14px;
  }
  .footer {
    width: 100%;
    color: gray;
  }
}
</style>

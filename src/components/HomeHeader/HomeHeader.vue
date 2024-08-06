<script setup lang="ts">
import { ref } from 'vue'
import HeaderInfo from './c-cpns/HeaderInfo.vue'
import HeaderCrumb from './c-cpns/HeaderCrumb.vue'
// 0.内部自定义事件
const emit = defineEmits(['foldChange'])
const isFold = ref(false)
function foldBtnClick() {
  // 1.内部改变状态
  isFold.value = !isFold.value
  // 2.发送事件
  emit('foldChange', isFold.value)
}
</script>

<template>
  <div class="home-header">
    <div class="menu-icon" @click="foldBtnClick">
      <el-icon size="28px">
        <component :is="isFold ? 'Expand' : 'Fold'" />
      </el-icon>
    </div>
    <div class="content">
      <header-crumb></header-crumb>
      <header-info></header-info>
    </div>
  </div>
</template>

<style lang="less" scoped>
.home-header {
  display: flex;
  align-items: center;
  flex: 1;
  height: 100%;

  .menu-icon {
    display: flex;
    align-items: center;
    cursor: pointer;
  }

  .content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex: 1;
    padding: 0 18px;
  }
}
</style>

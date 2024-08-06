<script setup lang="ts">
import { zhCn } from 'element-plus/es/locales.mjs'
</script>

<template>
  <div class="app">
    <el-config-provider :locale="zhCn">
      <router-view />
    </el-config-provider>
  </div>
</template>

<style lang="less" scoped>
.app {
  height: 100vh;
  width: 100vw;
}
</style>

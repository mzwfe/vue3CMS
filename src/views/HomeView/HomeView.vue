<script setup lang="ts">
import HomeMenu from '@/components/HomeMenu/HomeMenu.vue'
import HomeHeader from '@/components/HomeHeader/HomeHeader.vue'
import HomeMain from '@/components/HomeMain/HomeMain.vue'
import { ref } from 'vue'
// 处理子组件折叠变化事件
const isFold = ref(false)
function handleFoldChange(flag: boolean) {
  isFold.value = flag
}
</script>

<template>
  <div class="home">
    <el-container class="home-content">
      <el-aside class="content-aside" :width="isFold ? '60px' : '210px'">
        <home-menu :is-fold="isFold"></home-menu>
      </el-aside>
      <el-container>
        <el-header class="content-header" height="50px">
          <home-header @fold-change="handleFoldChange"></home-header>
        </el-header>
        <el-main class="content-main">
          <home-main></home-main>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style lang="less" scoped>
.home {
  height: 100%;

  .home-content {
    height: 100%;
  }

  .content-aside {
    overflow-x: hidden;
    overflow-y: auto;
    line-height: 200px;
    text-align: left;
    cursor: pointer;
    background-color: #001529;
    transition: width 0.3s linear;
    scrollbar-width: none;
    -ms-overflow-style: none;

    &::-webkit-scrollbar {
      display: none;
    }
  }

  // .content-header {
  //   background-color: #fff;
  // }

  .content-main {
    background-color: #f2f3f4;
  }
}
</style>

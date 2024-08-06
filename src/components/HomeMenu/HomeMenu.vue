<script setup lang="ts">
import router from '@/router'
import useLoginStore from '@/stores/login/login'
import { localCache } from '@/utils/cache'
import { firstMenu, mapPathToMenu } from '@/utils/map-menus'
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
// 接受父组件带来的参数
defineProps({
  isFold: {
    type: Boolean,
    default: false
  }
})
// 获取用户菜单, 用于搭建界面
const loginStore = useLoginStore()
const userMenus = loginStore.userMenus

// 监听菜单按钮点击
function handleRouter(item: any) {
  router.push(item.url)
}

// el-menu的默认菜单
const route = useRoute()
const defaultActive = computed(() => {
  return mapPathToMenu(route.path, userMenus).id + ''
})
</script>

<template>
  <div class="home-menu">
    <div class="logo">
      <img src="@/assets/img/logo.svg" alt="logo~" />
      <div class="title">后台管理系统</div>
    </div>
    <div class="menu">
      <el-menu
        :collapse="isFold"
        active-text-color="#fff"
        text-color="#b7bdc3"
        background-color="#001529"
        :default-active="defaultActive"
      >
        <!-- 遍历整个菜单 -->
        <template v-for="item in userMenus" :key="item.id">
          <el-sub-menu :index="item.id + ''">
            <template #title>
              <el-icon>
                <component :is="item.icon.split('-icon-')[1]" />
              </el-icon>
              <span>{{ item.name }}</span>
            </template>
            <template v-for="subItem in item.children" :key="subItem.id">
              <el-menu-item :index="subItem.id + ''" @click="handleRouter(subItem)">
                {{ subItem.name }}
              </el-menu-item>
            </template>
          </el-sub-menu>
        </template>
      </el-menu>
    </div>
  </div>
</template>

<style lang="less" scoped>
.home-menu {
  height: 100%;
  background-color: #001529;
}

.logo {
  display: flex;
  height: 30px;
  padding: 12px 10px 8px 10px;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  overflow: hidden;

  img {
    height: 100%;
    margin: 0 10px;
  }

  .title {
    font-size: 16px;
    font-weight: 700;
    color: white;
    white-space: nowrap;
  }
}

.el-menu {
  border-right: none;
  user-select: none;
}

.el-sub-menu {
  .el-menu-item {
    padding-left: 50px !important;
    background-color: #0c2135;
  }

  .el-menu-item:hover {
    color: #fff;
  }

  .el-menu-item.is-active {
    background-color: #0a60bd;
  }
}
</style>

<script setup lang="ts">
import { LOGIN_TOKEN } from '@/global/constance'
import router from '@/router'
import { localCache } from '@/utils/cache'

function logout() {
  localCache.deleteCache(LOGIN_TOKEN)
  localCache.deleteCache('userInfo')
  localCache.deleteCache('userMenus')
  router.push('/login')
}
</script>

<template>
  <div class="header-info">
    <!-- 三个图标 -->
    <div class="operation">
      <span>
        <el-icon>
          <Message />
        </el-icon>
      </span>
      <span>
        <el-icon>
          <span class="dot"></span>
          <ChatDotRound />
        </el-icon>
      </span>
      <span>
        <el-icon>
          <Search />
        </el-icon>
      </span>
    </div>
    <!-- 个人信息 -->
    <div class="info">
      <el-dropdown>
        <span class="user-info">
          <el-avatar
            :size="30"
            src="https://tse2-mm.cn.bing.net/th/id/OIP-C.xNqQD-GKRcG9eaoVTNrobwHaHa?w=162&h=180&c=7&r=0&o=5&pid=1.7"
          />
          <span class="name">{{ localCache.getCache('userInfo').name }}</span>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="logout">
              <el-icon>
                <CircleClose />
              </el-icon>
              <span class="text">退出登录</span>
            </el-dropdown-item>
            <el-dropdown-item divided>
              <el-icon>
                <InfoFilled />
              </el-icon>
              <span class="text">个人信息</span>
            </el-dropdown-item>
            <el-dropdown-item>
              <el-icon>
                <Lock />
              </el-icon>
              <span class="text">修改密码</span>
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<style lang="less" scoped>
.header-info {
  display: flex;
  align-items: center;
}

.operation {
  display: inline-flex;
  margin-right: 20px;

  span {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 35px;

    &:hover {
      background: #f2f2f2;
    }

    i {
      font-size: 20px;
    }

    .dot {
      position: absolute;
      top: -4px;
      right: -5px;
      z-index: 10;
      width: 6px;
      height: 6px;
      background: red;
      border-radius: 100%;
    }
  }
}

.info {
  width: 100px;

  .user-info {
    display: flex;
    align-items: center;
    cursor: pointer;

    &:focus-visible {
      outline: none;
    }
  }

  .name {
    margin-left: 8px;
  }
}
</style>

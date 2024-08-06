<script setup lang="ts">
import { ref, watch } from 'vue'
import PanelAccount from './PanelAccount.vue'
import PanelPhone from './PanelPhone.vue'
import { localCache } from '@/utils/cache'

const rememberPSW = ref<boolean>(localCache.getCache('rememberPSW') ?? false)
watch(rememberPSW, (newVal) => {
  localCache.deleteCache('rememberPSW')
  localCache.setCache('rememberPSW', newVal)
})
const activeName = ref('account')
const accountRef = ref<InstanceType<typeof PanelAccount>>()
const phoneRef = ref(null)

const handleLoginBtnClick = () => {
  if (activeName.value === 'account') {
    accountRef.value?.loginAction()
  } else if (activeName.value === 'phone') {
    console.log('phone')
  }
}
</script>

<template>
  <div class="login-panel">
    <!-- 标题 -->
    <h1 class="title">后台管理系统</h1>

    <!-- 中间tabs -->
    <div class="tabs">
      <el-tabs v-model="activeName" type="border-card" stretch>
        <!-- 账号登录 -->
        <el-tab-pane name="account">
          <template #label>
            <div class="label">
              <el-icon>
                <UserFilled />
              </el-icon>
              <span class="text">帐号登录</span>
            </div>
          </template>
          <div class="accont">
            <panel-account :rememberPSW="rememberPSW" ref="accountRef"></panel-account>
          </div>
        </el-tab-pane>
        <!-- 手机登录 -->
        <el-tab-pane name="phone">
          <template #label>
            <div class="label">
              <el-icon>
                <Iphone />
              </el-icon>
              <span class="text">手机登录</span>
            </div>
          </template>
          <panel-phone></panel-phone>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 底部区域 -->
    <div class="controls">
      <el-checkbox v-model="rememberPSW" label="记住密码" size="large" />
      <el-link type="primary">忘记密码</el-link>
    </div>
    <el-button @click="handleLoginBtnClick" type="primary" class="login-btn" size="large">
      立即登录
    </el-button>
  </div>
</template>

<style lang="less" scoped>
.login-panel {
  width: 20.625rem;
  background-color: #fff;

  .title {
    text-align: center;
    margin-bottom: 0.9375rem;
    font-weight: 700;
  }

  .label {
    display: flex;
    align-items: center;
    justify-content: center;

    .text {
      margin-left: 0.3125rem;
    }
  }

  .controls {
    margin-top: 0.75rem;
    display: flex;

    justify-content: space-between;
  }

  .login-btn {
    margin-top: 10px;
    width: 100%;
    // --el-button-size: 50px;
  }
}
</style>

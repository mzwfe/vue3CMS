<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import type { ElForm, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import useLoginStore from '@/stores/login/login'
import type { IAccount } from '../types'
import { localCache } from '@/utils/cache'
const loginStore = useLoginStore()
// 定义account数据
const account = reactive<IAccount>({
  name: localCache.getCache('name') ?? '',
  password: localCache.getCache('password') ?? ''
})
// 接收父组件数据
const props = defineProps({
  rememberPSW: {
    type: Boolean,
    default: false
  }
})

// 定义校验规则
const rules: FormRules = {
  name: [
    {
      required: true,
      message: '必须输入用户名',
      trigger: 'blur'
    },
    {
      pattern: /^[a-z0-9]{6,20}$/,
      message: '帐号必须为6-20位数字或字母组成',
      trigger: 'blur'
    }
  ],
  password: [
    {
      required: true,
      message: '请输入密码',
      trigger: 'blur'
    },
    {
      pattern: /^[a-z0-9]{6,20}$/,
      message: '密码必须为6-20位数字或字母组成',
      trigger: 'blur'
    }
  ]
}
// 键盘Enter / NumpadEnter实现登录操作
onMounted(() => {
  document.addEventListener('keydown', (e) => {
    if (e.code === 'Enter' || e.code === 'NumpadEnter') {
      loginAction()
    }
  })
})
// 执行登陆操作
const formRef = ref<InstanceType<typeof ElForm>>()
function loginAction() {
  formRef.value?.validate((valid) => {
    if (valid) {
      // 获取用户名和密码
      const name = account.name
      const password = account.password
      loginStore.accountLoginAction({ name, password }).then(() => {
        // 判断是否需要记住密码
        if (props.rememberPSW) {
          localCache.setCache('name', name)
          localCache.setCache('password', password)
        } else {
          localCache.deleteCache('name')
          localCache.deleteCache('password')
        }
      })
    } else {
      ElMessage({
        showClose: true,
        message: '帐号或密码格式错误',
        type: 'error'
      })
    }
  })
}

defineExpose({
  loginAction
})
</script>

<template>
  <div class="pan-account">
    <el-form
      ref="formRef"
      :model="account"
      label-width="60px"
      size="large"
      :rules="rules"
      status-icon
    >
      <el-form-item label="帐号" prop="name">
        <el-input v-model="account.name" />
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="account.password" type="password" />
      </el-form-item>
    </el-form>
  </div>
</template>

<style lang="less" scoped>
.pan-account {
  margin-top: 10px;
  margin-bottom: -5px;
}
</style>

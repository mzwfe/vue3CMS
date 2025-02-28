<script setup lang="ts">
import { reactive } from 'vue'
import type { FormData } from './type'
// 自定义事件
const emit = defineEmits(['queryClick', 'resetClick'])

// 定义form数据
const searchForm: FormData = reactive({
  name: '',
  realname: '',
  cellphone: '',
  enable: 1,
  createAt: ''
})

// 重置按钮点击
function hadleResetClick() {
  for (const key in searchForm) {
    if (key === 'enable') {
      searchForm[key] = 1
    } else {
      searchForm[key] = ''
    }
  }
  emit('resetClick')
}

// 查询按钮点击
function handleSearchClick() {
  emit('queryClick', searchForm)
}
</script>

<template>
  <div class="search-form">
    <!-- 1.搜索表单 -->
    <el-form :model="searchForm" label-width="80px" size="large">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="用户名">
            <el-input v-model="searchForm.name" placeholder="请输入用户名"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="真实姓名">
            <el-input v-model="searchForm.realname" placeholder="请输入真实姓名"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="电话号码">
            <el-input v-model="searchForm.cellphone" placeholder="请输入电话号码"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="状态">
            <el-select v-model="searchForm.enable" placeholder="请选择状态" style="width: 100%">
              <el-option label="启用" :value="1" />
              <el-option label="禁用" :value="0" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="选择时间">
            <el-date-picker
              v-model="searchForm.createAt"
              type="daterange"
              range-separator="-"
              start-placeholder="开始时间"
              end-placeholder="结束时间"
            />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="操作">
            <div class="btns">
              <el-button size="large" icon="Refresh" @click="hadleResetClick">重置</el-button>
              <el-button size="large" type="primary" icon="Search" @click="handleSearchClick"
                >查询</el-button
              >
            </div>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>

<style lang="less" scoped>
.search-form {
  background-color: #fff;
  padding: 20px;
  height: 20vh;
  box-sizing: border-box;
}

.el-form-item {
  padding: 10px 20px;
  margin-bottom: 0;
}

.btns {
  text-align: justify;
  padding: 5px 20px;
}
</style>

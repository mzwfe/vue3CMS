<script setup lang="ts">
import { reactive } from 'vue'
// 自定义事件
const emit = defineEmits(['queryClick', 'resetClick'])

// 定义form数据
const searchForm = reactive<any>({
  name: '',
  leader: '',
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
          <el-form-item label="部门名称">
            <el-input v-model="searchForm.name" placeholder="请输入部门名称"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="部门领导">
            <el-input v-model="searchForm.realname" placeholder="请输入部门领导"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="创建时间">
            <el-date-picker
              v-model="searchForm.createAt"
              type="daterange"
              range-separator="-"
              start-placeholder="开始时间"
              end-placeholder="结束时间"
            />
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <!-- 2.搜索按钮 -->
    <div class="btns">
      <el-button size="large" icon="Refresh" @click="hadleResetClick">重置</el-button>
      <el-button size="large" type="primary" icon="Search" @click="handleSearchClick">
        查询
      </el-button>
    </div>
  </div>
</template>

<style lang="less" scoped>
.search-form {
  background-color: #fff;
  padding: 20px;
}

.el-form-item {
  padding: 20px;
  margin-bottom: 0;
}

.btns {
  text-align: right;
  padding: 5px 20px;
}
</style>

<script setup lang="ts">
import { reactive } from 'vue'
// 自定义事件/接受的属性
interface IProps {
  searchConfig: {
    formItems: any[]
  }
}
const emit = defineEmits(['queryClick', 'resetClick'])
const props = defineProps<IProps>()

// 定义form数据
const initialForm: any = {}
for (const item of props.searchConfig.formItems) {
  initialForm[item.prop] = ''
}
const searchForm = reactive(initialForm)

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
        <template v-for="item in searchConfig.formItems" :key="item.prop">
          <el-col :span="8">
            <el-form-item :label="item.label" :prop="item.prop">
              <template v-if="item.type === 'input'">
                <el-input
                  v-model="searchForm[item.prop]"
                  :placeholder="item.placeholder"
                ></el-input>
              </template>
              <template v-if="item.type === 'date-picker'">
                <el-date-picker
                  v-model="searchForm[item.prop]"
                  type="daterange"
                  range-separator="-"
                  start-placeholder="开始时间"
                  end-placeholder="结束时间"
                />
              </template>
              <template v-if="item.type === 'select'">
                <el-select
                  v-model="searchForm[item.prop]"
                  :placeholder="item.placeholder"
                  style="width: 100%"
                >
                  <template v-for="option in item.options" :key="option.label">
                    <el-option :label="option.label" :value="option.value"></el-option>
                  </template>
                </el-select>
              </template>
            </el-form-item>
          </el-col>
        </template>
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

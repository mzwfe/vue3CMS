<script setup lang="ts">
import { reactive, ref } from 'vue'
import useHomeStore from '@/stores/home/home'
import { storeToRefs } from 'pinia'
import useSystemStore from '@/stores/home/system/system'

// 定义内部数据
const isNewRef = ref(true)
const id = ref(-1)
const centerDialogVisible = ref(false)
const formData = reactive<any>({
  name: '',
  leader: '',
  parentId: ''
})

// 导入所有角色和部门
const { entireDepartments } = storeToRefs(useHomeStore())
const systemStore = useSystemStore()
// 不暴露属性, 而是暴露方法, 便于属性可控
function setModalVisible(isNew: boolean = true, row?: any) {
  centerDialogVisible.value = true
  isNewRef.value = isNew
  id.value = row?.id
  if (!isNew && row) {
    for (const key in formData) {
      formData[key] = row[key]
    }
  } else {
    for (const key in formData) {
      formData[key] = ''
    }
    id.value = -1
  }
}
// 点击确定提交数据创建用户
function commitFormData() {
  centerDialogVisible.value = false
  if (isNewRef.value) {
    systemStore.newPageDataAction('department', formData)
  } else {
    systemStore.editPageDataAction('department', id.value, formData)
  }
}

defineExpose({ setModalVisible })
</script>

<template>
  <div class="modal">
    <el-dialog
      v-model="centerDialogVisible"
      :title="isNewRef ? '新建部门' : '编辑部门'"
      width="30%"
      center
    >
      <div class="form">
        <el-form :model="formData" label-width="80px" size="large">
          <el-form-item label="部门名称" prop="name">
            <el-input v-model="formData.name" placeholder="请输入部门名称" />
          </el-form-item>
          <el-form-item label="部门领导" prop="leader">
            <el-input v-model="formData.leader" placeholder="请输入部门领导" />
          </el-form-item>
          <el-form-item label="选择上级部门" prop="parentId">
            <el-select v-model="formData.parentId" placeholder="请选择部门">
              <template v-for="item in entireDepartments" :key="item.id">
                <el-option :label="item.name" :value="item.id"></el-option>
              </template>
            </el-select>
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="centerDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="commitFormData">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style lang="less" scoped></style>

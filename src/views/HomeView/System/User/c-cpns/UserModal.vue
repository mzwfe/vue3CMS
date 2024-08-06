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
  realname: '',
  password: '',
  cellphone: '',
  departmentId: -1,
  roleId: -1
})

// 导入所有角色和部门
const { entireRoles, entireDepartments } = storeToRefs(useHomeStore())
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
  }
}
// 点击确定提交数据创建用户
function commitFormData() {
  centerDialogVisible.value = false
  if (isNewRef.value) {
    systemStore.newUserDataAction(formData).then()
  } else {
    systemStore.editUserDataAction(id.value, formData)
  }
}

defineExpose({ setModalVisible })
</script>

<template>
  <div class="modal">
    <el-dialog
      v-model="centerDialogVisible"
      :title="isNewRef ? '新建用户' : '编辑用户'"
      width="30%"
      center
    >
      <div class="form">
        <el-form :model="formData" label-width="80px" size="large">
          <el-form-item label="用户名" prop="name">
            <el-input v-model="formData.name" placeholder="请输入用户名" />
          </el-form-item>
          <el-form-item label="真实姓名" prop="realname">
            <el-input v-model="formData.realname" placeholder="请输入真实姓名" />
          </el-form-item>
          <el-form-item v-if="isNewRef" label="密码" prop="password">
            <el-input v-model="formData.password" placeholder="请输入密码" show-password />
          </el-form-item>
          <el-form-item label="电话号码" prop="cellphone">
            <el-input v-model="formData.cellphone" placeholder="请输入电话号码" />
          </el-form-item>
          <el-form-item label="选择角色" prop="cellphone">
            <el-select v-model="formData.roleId" placeholder="请选择角色">
              <template v-for="item in entireRoles" :key="item.id">
                <el-option :label="item.name" :value="item.id"></el-option>
              </template>
            </el-select>
          </el-form-item>
          <el-form-item label="选择部门" prop="cellphone">
            <el-select v-model="formData.departmentId" placeholder="请选择部门">
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

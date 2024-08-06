<script setup lang="ts">
import { reactive, ref } from 'vue'
import useSystemStore from '@/stores/home/system/system'

interface IProps {
  modalConfig: {
    pageName: string
    header: {
      newTitle: string
      editTitle: string
    }
    formItems: any[]
  }
  otherInfo?: any
}
const props = defineProps<IProps>()

// 定义内部数据
const isNewRef = ref(true)
const id = ref(-1)
const centerDialogVisible = ref(false)
const initialData: any = {}
for (const item of props.modalConfig.formItems) {
  initialData[item.prop] = item.initialValue ?? ''
}
const formData = reactive<any>(initialData)

// 导入所有角色和部门
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
      // 新建数据设置初始化值
      formData[key] = ''
    }
    id.value = -1
  }
}
// 点击确定提交数据创建用户
function commitFormData() {
  centerDialogVisible.value = false
  let infoData = { ...formData }
  if (props.otherInfo) {
    infoData = { ...infoData, ...props.otherInfo }
  }
  if (isNewRef.value) {
    systemStore.newPageDataAction(props.modalConfig.pageName, infoData)
  } else {
    systemStore.editPageDataAction(props.modalConfig.pageName, id.value, infoData)
  }
}

defineExpose({ setModalVisible })
</script>

<template>
  <div class="modal">
    <el-dialog
      v-model="centerDialogVisible"
      :title="isNewRef ? modalConfig.header.newTitle : modalConfig.header.editTitle"
      width="30%"
      center
    >
      <div class="form">
        <el-form :model="formData" label-width="80px" size="large">
          <template v-for="item in modalConfig.formItems" :key="item.prop">
            <el-form-item :label="item.label" :prop="item.prop">
              <template v-if="item.type === 'input'">
                <el-input v-model="formData[item.prop]" :placeholder="item.placeholder"></el-input>
              </template>
              <template v-if="item.type === 'date-picker'">
                <el-date-picker
                  v-model="formData[item.prop]"
                  type="daterange"
                  range-separator="-"
                  start-placeholder="开始时间"
                  end-placeholder="结束时间"
                />
              </template>
              <template v-if="item.type === 'select'">
                <el-select
                  v-model="formData[item.prop]"
                  :placeholder="item.placeholder"
                  style="width: 100%"
                >
                  <template v-for="option in item.options" :key="option.label">
                    <el-option :label="option.label" :value="option.value"></el-option>
                  </template>
                </el-select>
              </template>
              <template v-if="item.type === 'custom'">
                <slot :name="item.slotName"></slot>
              </template>
            </el-form-item>
          </template>
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

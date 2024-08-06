<script setup lang="ts">
import SearchForm from './c-cpns/SearchForm.vue'
import FormContent from './c-cpns/FormContent.vue'
import UserModal from './c-cpns/UserModal.vue'
import { ref } from 'vue'
const contentRef = ref<InstanceType<typeof FormContent>>()
const modalRef = ref<InstanceType<typeof UserModal>>()
function handleQueryClick(formData: any) {
  contentRef.value!.fetchUsersList(formData)
}

function handleResetClick() {
  contentRef.value!.fetchUsersList()
}

function handleNewClick() {
  modalRef.value!.setModalVisible()
}

function handleEditClick(row: any) {
  modalRef.value!.setModalVisible(false, row)
}
</script>

<template>
  <div class="user">
    <search-form @query-click="handleQueryClick" @reset-click="handleResetClick"></search-form>
    <form-content
      ref="contentRef"
      @new-click="handleNewClick"
      @edit-click="handleEditClick"
    ></form-content>
    <user-modal ref="modalRef"></user-modal>
  </div>
</template>

<style lang="less" scoped></style>

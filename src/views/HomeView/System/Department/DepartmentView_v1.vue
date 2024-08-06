<script setup lang="ts">
import PageSearch from './c-cpns/PageSearch.vue'
import PageContent from './c-cpns/PageContent.vue'
import PageModal from './c-cpns/PageModal.vue'
import { ref } from 'vue'

// 点击search, content的操作
const contentRef = ref<any>()
function handleQueryClick(queryInfo: any) {
  contentRef.value.fetchPageList(queryInfo)
}
function handleResetClick() {
  contentRef.value.fetchPageList()
}

// 点击content, modal的操作
const modalRef = ref<any>()
function handleNewClick(itemData: any) {
  modalRef.value.setModalVisible()
}
function handleEditClick(row: any) {
  modalRef.value.setModalVisible(false, row)
}
</script>

<template>
  <div class="department">
    <page-search @query-click="handleQueryClick" @reset-click="handleResetClick"></page-search>
    <page-content
      ref="contentRef"
      @new-click="handleNewClick"
      @edit-click="handleEditClick"
    ></page-content>
    <page-modal ref="modalRef"></page-modal>
  </div>
</template>

<style lang="less" scoped></style>

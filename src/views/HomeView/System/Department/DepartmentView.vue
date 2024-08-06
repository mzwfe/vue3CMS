<script setup lang="ts">
import PageSearch from '@/components/PageSearch/PageSearch.vue'
import PageContent from '@/components/PageContent/PageContent.vue'
import PageModal from '@/components/PageModal/PageModal.vue'
import { computed } from 'vue'

import searchConfig from './config/search.config'
import contentConfig from './config/content.config'
import modalConfig from './config/modal.config'
import useHomeStore from '@/stores/home/home'
import { usePageContent } from '@/hooks/usePageContent'
import { usePageModal } from '@/hooks/usePageModal'

const modalConfigRef = computed(() => {
  const homeStore = useHomeStore()
  const deparments = homeStore.entireDepartments.map((item) => {
    return { label: item.name, value: item.id }
  })
  modalConfig.formItems.forEach((item) => {
    if (item.prop === 'parentId') {
      item.options?.push(...deparments)
    }
  })
  return modalConfig
})

// setup中相同逻辑抽取: hooks
// 点击search, content的操作
const { contentRef, handleQueryClick, handleResetClick } = usePageContent()

// 点击content, modal的操作
const { modalRef, handleNewClick, handleEditClick } = usePageModal()
</script>

<template>
  <div class="department">
    <page-search
      :search-config="searchConfig"
      @query-click="handleQueryClick"
      @reset-click="handleResetClick"
    ></page-search>
    <page-content
      :content-config="contentConfig"
      ref="contentRef"
      @new-click="handleNewClick"
      @edit-click="handleEditClick"
    >
      <template #leaaa="scope">
        <span style="color: blue">{{ scope.row.leader }}</span>
      </template>
    </page-content>
    <page-modal :modal-config="modalConfigRef" ref="modalRef"></page-modal>
  </div>
</template>

<style lang="less" scoped></style>

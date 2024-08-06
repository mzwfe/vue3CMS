<script setup lang="ts">
import PageSearch from '@/components/PageSearch/PageSearch.vue'
import PageContent from '@/components/PageContent/PageContent.vue'
import PageModal from '@/components/PageModal/PageModal.vue'

import contentConfig from './config/content.config'
import modalConfigRef from './config/modal.config'
import searchConfig from './config/search.config'

import { usePageContent } from '@/hooks/usePageContent'
import { usePageModal } from '@/hooks/usePageModal'

// 点击search, content的操作
const { contentRef, handleQueryClick, handleResetClick } = usePageContent()

// 点击content, modal的操作
const { modalRef, handleNewClick, handleEditClick } = usePageModal()
</script>

<template>
  <div class="category">
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
    </page-content>
    <page-modal :modal-config="modalConfigRef" ref="modalRef"></page-modal>
  </div>
</template>

<style lang="less" scoped></style>

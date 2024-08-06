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
  <div class="goods">
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
      <template #name="scope">
        <span class="fold">{{ scope.row.name }}</span>
      </template>
      <template #desc="scope">
        <span class="fold">{{ scope.row.desc }}</span>
      </template>
      <template #oldPrice="scope">
        <span style="text-decoration: line-through">{{ scope.row.oldPrice }}</span>
      </template>
      <template #newPrice="scope">
        <span style="color: red; font-size: 18px">{{ scope.row.newPrice }}</span>
      </template>
      <template #imgUrl="scope">
        <img class="image" :src="scope.row.imgUrl" alt="" />
      </template>
    </page-content>
    <page-modal :modal-config="modalConfigRef" ref="modalRef"></page-modal>
  </div>
</template>

<style lang="less" scoped>
.fold {
  overflow: hidden; /*超出部分隐藏*/
  white-space: nowrap; /*禁止换行*/
  text-overflow: ellipsis; /*省略号*/
}

.fold:hover {
  white-space: wrap;
}

.image {
  height: 50px;
  width: 50px;
}
</style>

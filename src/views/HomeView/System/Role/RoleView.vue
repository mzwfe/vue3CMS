<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { nextTick, ref } from 'vue'
import type { ElTree } from 'element-plus'

import PageSearch from '@/components/PageSearch/PageSearch.vue'
import PageContent from '@/components/PageContent/PageContent.vue'
import PageModal from '@/components/PageModal/PageModal.vue'

import searchConfig from './config/search.config'
import contentConfig from './config/content.config'
import modalConfig from './config/modal.config'
import { usePageContent } from '@/hooks/usePageContent'
import { usePageModal } from '@/hooks/usePageModal'
import useHomeStore from '@/stores/home/home'
import { mapMenusToIds } from '@/utils/map-menus'

// 逻辑
const { contentRef, handleQueryClick, handleResetClick } = usePageContent()
const { modalRef, handleEditClick, handleNewClick } = usePageModal(editCallBack, newCallBack)

// 获取完整菜单
const homeStore = useHomeStore()
const { entireMenus } = storeToRefs(homeStore)
const otherInfo = ref({})

function handleElTreeCheck(data1: any, data2: any) {
  const menuList = [...data2.checkedKeys, ...data2.halfCheckedKeys]
  console.log(menuList)
  otherInfo.value = { menuList }
}

const treeRef = ref<InstanceType<typeof ElTree>>()
function newCallBack() {
  nextTick(() => {
    treeRef.value?.setCheckedKeys([])
  })
}
function editCallBack(itemData: any) {
  nextTick(() => {
    const ids = mapMenusToIds(itemData.menuList)
    treeRef.value?.setCheckedKeys(ids)
  })
}
</script>

<template>
  <div class="role">
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
    ></page-content>
    <page-modal :modal-config="modalConfig" :other-info="otherInfo" ref="modalRef">
      <template #menuList>
        <el-tree
          ref="treeRef"
          style="max-width: 600px"
          :data="entireMenus"
          show-checkbox
          node-key="id"
          :props="{ children: 'children', label: 'name' }"
          @check="handleElTreeCheck"
        />
      </template>
    </page-modal>
  </div>
</template>

<style lang="less" scoped></style>

<script setup lang="ts">
import ListPageContent from '@/components/PageContent/ListPageContent.vue'

import contentConfig from './config/content.config'
</script>

<template>
  <div class="list">
    <list-page-content :content-config="contentConfig"></list-page-content>
  </div>
</template>

<style lang="less" scoped></style>

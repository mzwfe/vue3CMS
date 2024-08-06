<script setup lang="ts">
import PageContent from '@/components/PageContent/PageContent.vue'
import contentConfig from './config/content.config'
</script>

<template>
  <div class="menu">
    <page-content :content-config="contentConfig"></page-content>
  </div>
</template>

<style lang="less" scoped></style>

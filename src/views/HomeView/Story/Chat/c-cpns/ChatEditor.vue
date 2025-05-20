<script setup lang="ts">
import '@wangeditor/editor/dist/css/style.css' // 引入 css

import { onBeforeUnmount, ref, shallowRef } from 'vue'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import { createStory } from '@/service/home/analysis/analysis'
// 编辑器实例，必须用 shallowRef
const editorRef = shallowRef()

// 内容 HTML
const valueHtml = ref()

const toolbarConfig = {}
const editorConfig = { placeholder: '请输入内容...' }

// 组件销毁时，也及时销毁编辑器
onBeforeUnmount(() => {
  const editor = editorRef.value
  if (editor == null) return
  editor.destroy()
})

const handleCreated = (editor: any) => {
  editorRef.value = editor // 记录 editor 实例，重要！
}

function sendText() {
  createStory(extractChineseText(valueHtml.value))
}

function extractChineseText(htmlString: string): { title: string; content: string } {
  // 使用 DOMParser 解析传入的 HTML 字符串
  const parser = new DOMParser()
  const doc = parser.parseFromString(htmlString, 'text/html')

  // 提取所有 <p> 标签的文本内容
  const paragraphs = Array.from(doc.querySelectorAll('p')).map((p) => p.textContent || '')

  // 假设第一个 <p> 是标题 "我的奋斗"
  const title = paragraphs[0] || ''

  // 其余的 <p> 标签为内容部分
  const content = paragraphs.slice(1).join('\n')

  return { title, content }
}
</script>

<template>
  <div style="border: 1px solid #ccc">
    <Toolbar
      style="border-bottom: 1px solid #ccc"
      :editor="editorRef"
      :defaultConfig="toolbarConfig"
      :mode="mode"
    />
    <Editor
      style="height: 500px; overflow-y: hidden"
      v-model="valueHtml"
      :defaultConfig="editorConfig"
      :mode="mode"
      @onCreated="handleCreated"
    />
    <div class="send">
      <el-button type="primary" @click="sendText">发送</el-button>
    </div>
  </div>
</template>

<style></style>

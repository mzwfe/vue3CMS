import { ref } from 'vue'
export function usePageContent() {
  // 点击search, content的操作
  const contentRef = ref<any>()
  function handleQueryClick(queryInfo: any) {
    contentRef.value.fetchPageList(queryInfo)
  }
  function handleResetClick() {
    contentRef.value.fetchPageList()
  }

  return {
    contentRef,
    handleQueryClick,
    handleResetClick
  }
}

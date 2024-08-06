import { ref } from 'vue'
export function usePageModal(editCB?: (data: any) => void, newCB?: (data: any) => void) {
  const modalRef = ref<any>()
  function handleNewClick(itemData: any) {
    modalRef.value.setModalVisible()
    if (newCB) {
      newCB(itemData)
    }
  }
  function handleEditClick(row: any) {
    modalRef.value.setModalVisible(false, row)
    if (editCB) {
      editCB(row)
    }
  }

  return {
    modalRef,
    handleNewClick,
    handleEditClick
  }
}

const modalConfig = {
  pageName: 'goods',
  header: {
    newTitle: '',
    editTitle: '商品'
  },
  formItems: [
    {
      type: 'input',
      label: '商品名称',
      prop: 'name',
      placeholder: '请输入商品名称'
    },
    { type: 'input', label: '原价', prop: 'oldPrice' },
    { type: 'input', label: '现价', prop: 'newPrice' },
    { type: 'input', label: '描述', prop: 'desc' },
    { type: 'input', label: '图片路径', prop: 'imgUrl' },
    { type: 'input', label: '收藏', prop: 'favorCount' },
    { type: 'input', label: '销量', prop: 'saleCount' },
    {
      type: 'select',
      label: '状态',
      prop: 'status',
      options: [
        { label: '上架', value: 1 },
        { label: '下架', value: 0 }
      ]
    },
    { type: 'input', label: '库存', prop: 'inventoryCount' },
    { type: 'input', label: '地址', prop: 'address' }
  ]
}

export default modalConfig

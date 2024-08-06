const contentConfig = {
  pageName: 'goods',
  header: {
    title: '商品列表',
    btnTitle: '新增商品'
  },
  propsList: [
    { type: 'selection', label: '选择', width: '50px' },
    { type: 'index', label: '序号', width: '60px' },

    {
      type: 'custom',
      label: '商品名称',
      prop: 'name',
      slotName: 'name',
      width: '100px'
    },
    { type: 'custom', label: '原价', prop: 'oldPrice', width: '80px', slotName: 'oldPrice' },
    { type: 'custom', label: '现价', prop: 'newPrice', width: '80px', slotName: 'newPrice' },
    { type: 'custom', label: '描述', prop: 'desc', slotName: 'desc', width: '100px' },
    { type: 'normal', label: '状态', prop: 'status', width: '100px' },
    { type: 'custom', label: '商品图片', prop: 'imgUrl', slotName: 'imgUrl', width: '120px' },
    { type: 'normal', label: '库存', prop: 'inventoryCount', width: '100px' },
    { type: 'normal', label: '销量', prop: 'saleCount', width: '100px' },
    { type: 'normal', label: '收藏', prop: 'favorCount', width: '100px' },
    { type: 'normal', label: '地址', prop: 'address', width: '100px' },

    { type: 'timer', label: '创建时间', prop: 'createAt' },
    { type: 'timer', label: '更新时间', prop: 'updateAt' },

    { type: 'handler', label: '操作', width: '160px' }
  ]
}

export default contentConfig

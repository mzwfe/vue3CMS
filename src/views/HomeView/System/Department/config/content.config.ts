const contentConfig = {
  pageName: 'department',
  header: {
    title: '部门列表',
    btnTitle: '新增部门'
  },
  propsList: [
    { type: 'selection', label: '选择', width: '50px' },
    { type: 'index', label: '序号', width: '60px' },

    { type: 'normal', label: '部门名称', prop: 'name', width: '160px' },
    { type: 'normal', label: '部门领导', prop: 'leader', width: '100px' },
    { type: 'normal', label: '上级部门', prop: 'parentId', width: '120px' },

    { type: 'custom', label: '部门领导', prop: 'leader', width: '100px', slotName: 'leaaa' },

    { type: 'timer', label: '创建时间', prop: 'createAt' },
    { type: 'timer', label: '更新时间', prop: 'updateAt' },

    { type: 'handler', label: '操作', width: '160px' }
  ]
}

export default contentConfig

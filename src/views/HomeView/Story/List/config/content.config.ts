const contentConfig = {
  pageName: 'story',
  header: {
    title: '故事列表'
  },
  propsList: [
    { type: 'selection', label: '选择', width: '50px' },
    { type: 'index', label: '序号', width: '60px' },

    { type: 'normal', label: '故事名称', prop: 'title', width: '100px' },
    { type: 'normal', label: '故事内容', prop: 'content' },

    { type: 'timer', label: '创建时间', prop: 'createAt', width: '300px' }
  ]
}

export default contentConfig

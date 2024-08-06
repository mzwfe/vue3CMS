<script setup lang="ts">
import useSystemStore from '@/stores/home/system/system'
import { formatDate } from '@/utils/format'
import { storeToRefs } from 'pinia'
import { ref } from 'vue'

const emit = defineEmits(['newClick', 'editClick'])

// 1.请求usersList数据
const currentPage = ref(1)
const pageSize = ref(10)
const systemStore = useSystemStore()
fetchPageList()

// 2.获取usersList数据, 进行展示
const { pageList, pageTotalCount } = storeToRefs(systemStore)

// 3.点击按钮, 启用/禁用用户
function handleEnableClick(row: any) {
  row.enable = Number(!row.enable)
}

// 4.页码相关逻辑
function handleSizeChange(val: number) {
  fetchPageList()
}
function handleCurrentChange(val: number) {
  fetchPageList()
}

// 5.查询页面数据
function fetchPageList(formData: any = {}) {
  // 获取offset和size
  const size = pageSize.value
  const offset = (currentPage.value - 1) * pageSize.value
  const pageInfo = { size, offset }
  const allInfo = { ...formData, ...pageInfo }
  systemStore.postPageListAction('department', allInfo)
}

// 6.编辑/删除/新建按钮的点击
function editClick(row: any) {
  emit('editClick', row)
}
function deleteClick(row: any) {
  // 删除操作
  systemStore.deletePageDataByIdAction('department', row.id)
  // 重新加载数据, 刷新页面
  const size = pageSize.value
  const offset = (currentPage.value - 1) * pageSize.value
  const pageInfo = { size, offset }
  fetchPageList(pageInfo)
}
function handleNewUserClick() {
  emit('newClick')
}

defineExpose({ fetchPageList })
</script>

<template>
  <div class="content">
    <div class="header">
      <h3 class="title">部门列表</h3>
      <el-button type="primary" @click="handleNewUserClick">新建部门</el-button>
    </div>
    <div class="table">
      <el-table :data="pageList" border style="width: 100%">
        <el-table-column type="selection" width="50px" align="center" />
        <el-table-column type="index" label="序号" width="60px" align="center" />

        <el-table-column prop="name" label="部门名称" align="center" width="160px" />
        <el-table-column prop="leader" label="部门领导" align="center" width="100px" />
        <el-table-column prop="parentId" label="上级部门" align="center" width="120px" />

        <el-table-column prop="createAt" label="创建时间" align="center">
          <template #default="scope">
            {{ formatDate(scope.row.createAt, 'YYYY/MM/DD HH:mm:ss') }}
          </template>
        </el-table-column>
        <el-table-column prop="updateAt" label="更新时间" align="center">
          <template #default="scope">
            {{ formatDate(scope.row.updateAt, 'YYYY/MM/DD HH:mm:ss') }}
          </template>
        </el-table-column>

        <el-table-column class="btns" label="操作" align="center" width="180px">
          <template #default="scope">
            <el-button
              class="1"
              size="small"
              text
              type="primary"
              icon="Edit"
              @click="editClick(scope.row)"
            >
              编辑
            </el-button>
            <el-button
              size="small"
              text
              type="danger"
              icon="Delete"
              @click="deleteClick(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 30]"
        size="small"
        :background="true"
        layout="sizes, prev, pager, next, jumper, total"
        :total="pageTotalCount"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<style lang="less" scoped>
.content {
  background-color: #fff;
  margin-top: 20px;
  padding: 15px;

  .header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
    align-items: flex-end;

    .title {
      font-size: 22px;
      font-weight: 600;
    }
  }
}

.table {
  :deep(.el-table__cell) {
    padding: 12px 0 !important;
  }

  :deep(.el-button) {
    margin-left: 0;
    padding: 0px 10px;
  }
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}
</style>

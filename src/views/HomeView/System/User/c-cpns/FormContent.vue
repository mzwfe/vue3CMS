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
fetchUsersList()

// 2.获取usersList数据, 进行展示
const { usersList, totalCount } = storeToRefs(systemStore)

// 3.点击按钮, 启用/禁用用户
function handleEnableClick(row: any) {
  row.enable = Number(!row.enable)
}

// 4.页码相关逻辑
function handleSizeChange(val: number) {
  fetchUsersList()
}
function handleCurrentChange(val: number) {
  fetchUsersList()
}

// 5.查询页面数据
function fetchUsersList(formData: any = {}) {
  // 获取offset和size
  const size = pageSize.value
  const offset = (currentPage.value - 1) * pageSize.value
  const pageInfo = { size, offset }
  const allInfo = { ...formData, ...pageInfo }
  systemStore.postUsersListAction(allInfo)
}

// 6.编辑/删除/新建按钮的点击
function editClick(row: any) {
  emit('editClick', row)
}
function deleteClick(row: any) {
  // 删除操作
  systemStore.deleteUserByIdAction(row.id)
  // 重新加载数据, 刷新页面
  const size = pageSize.value
  const offset = (currentPage.value - 1) * pageSize.value
  const pageInfo = { size, offset }
  fetchUsersList(pageInfo)
}
function handleNewUserClick() {
  emit('newClick')
}

defineExpose({ fetchUsersList })
</script>

<template>
  <div class="content">
    <div class="header">
      <h3 class="title">用户列表</h3>
      <el-button type="primary" @click="handleNewUserClick">新建用户</el-button>
    </div>
    <div class="table">
      <el-table :data="usersList" border style="width: 100%">
        <el-table-column type="selection" width="50px" align="center" />
        <el-table-column type="index" label="序号" width="60px" align="center" />

        <el-table-column prop="name" label="用户名" align="center" width="160px" />
        <el-table-column prop="realname" label="真实姓名" align="center" width="100px" />
        <el-table-column prop="cellphone" label="手机号" align="center" width="120px" />
        <el-table-column prop="enable" label="状态" align="center" width="80px">
          <!-- 作用域插槽 -->
          <template #default="scope">
            <el-button
              size="small"
              :type="scope.row.enable ? 'success' : 'danger'"
              plain
              @click="handleEnableClick(scope.row)"
            >
              {{ scope.row.enable ? '启用' : '禁用' }}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column prop="createAt" label="创建时间" align="center">
          <template #default="scope">
            <span class="fold">{{ formatDate(scope.row.createAt, 'YYYY/MM/DD HH:mm:ss') }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="updateAt" label="更新时间" align="center">
          <template #default="scope">
            <span class="fold">{{ formatDate(scope.row.updateAt, 'YYYY/MM/DD HH:mm:ss') }}</span>
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
        :total="totalCount"
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
  height: 50vh;

  :deep(.el-table__cell) {
    padding: 12px 0 !important;
  }

  :deep(.el-table--fit) {
    height: 50vh;
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

.fold {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>

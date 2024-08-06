<script setup lang="ts">
import usePermissions from '@/hooks/usePermissions'
import useSystemStore from '@/stores/home/system/system'
import { formatDate } from '@/utils/format'
import { storeToRefs } from 'pinia'
import { ref } from 'vue'

interface IProps {
  contentConfig: {
    pageName: string
    header?: {
      title?: string
      btnTitle?: string
    }
    propsList: any[]
    childrenTree?: any
  }
}

const props = defineProps<IProps>()

const emit = defineEmits(['newClick', 'editClick'])

// 获取按钮权限

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
  systemStore.postPageListAction(props.contentConfig.pageName, allInfo)
}

// 6.编辑/删除/新建按钮的点击
function editClick(row: any) {
  emit('editClick', row)
}
function deleteClick(row: any) {
  // 删除操作
  systemStore.deletePageDataByIdAction(props.contentConfig.pageName, row.id)
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
      <h3 class="title">{{ contentConfig?.header?.title ?? '数据列表' }}</h3>
      <el-button v-if="contentConfig.header?.btnTitle" type="primary" @click="handleNewUserClick">
        {{ contentConfig.header?.btnTitle ?? '新建数据' }}
      </el-button>
    </div>
    <div class="table">
      <el-table :data="pageList" border style="width: 100%" v-bind="contentConfig.childrenTree">
        <template v-for="item in contentConfig.propsList" :key="item.prop">
          <template v-if="item.type === 'timer'">
            <el-table-column class="timer" v-bind="item" align="center">
              <template #default="scope">
                <span class="fold">
                  {{ formatDate(scope.row[item.prop], 'YYYY/MM/DD HH:mm:ss') }}
                </span>
              </template>
            </el-table-column>
          </template>
          <template v-else-if="item.type === 'handler'">
            <el-table-column class="btns" align="center" v-bind="item">
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
          </template>
          <template v-else-if="item.type === 'custom'">
            <el-table-column align="center" v-bind="item">
              <template #default="scope">
                <slot :name="item.slotName" v-bind="scope"></slot>
              </template>
            </el-table-column>
          </template>
          <template v-else>
            <el-table-column align="center" v-bind="item"></el-table-column>
          </template>
        </template>
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

// 设置时间折叠样式
.fold {
  overflow: hidden; /*超出部分隐藏*/
  white-space: nowrap; /*禁止换行*/
  text-overflow: ellipsis; /*省略号*/
}
</style>

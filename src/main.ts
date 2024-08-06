import { createApp } from 'vue'
import 'normalize.css'
import './assets/css/index.less'

import App from './App.vue'
import router from './router'
import store from './stores'
import registerIcons from './global/register-icons'

// 针对ElMessage和ElLoading引入样式
// import 'element-plus/theme-chalk/el-message.css'
// import 'element-plus/theme-chalk/el-loading.css'

// 1. 全局引入element-plus
// import ElementPlus from 'element-plus'
// import 'element-plus/dist/index.css'
// app.use(ElementPlus)

// 2.按需引入, 用到那个组件引入哪个
// import { ElButton } from 'element-plus'
// app.component(ElButton.name as string, ElButton)

const app = createApp(App)

app.use(registerIcons)
app.use(store)
app.use(router)
app.mount('#app')

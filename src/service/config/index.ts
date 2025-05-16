// 2.代码逻辑判断, 判断当前环境
// vite默认提供的环境变量
// console.log(import.meta.env.MODE)
// console.log(import.meta.env.DEV) // 是否开发环境
// console.log(import.meta.env.PROD) // 是否生产环境
// console.log(import.meta.env.SSR) // 是否是服务器端渲染(server side render)

let BASE_URL = ''
if (import.meta.env.DEV) {
  // 设置开发环境url
  BASE_URL = 'http://127.0.0.1:5000/api'
} else if (import.meta.env.PROD) {
  // 设置生产环境url
  BASE_URL = 'http://127.0.0.1:5000/api'
}

const TIME_OUT = 5000
export { BASE_URL, TIME_OUT }

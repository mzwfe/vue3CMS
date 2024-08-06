import { localCache } from '@/utils/cache'
import { BASE_URL, TIME_OUT } from './config'
import ZWRequest from './request'
import { LOGIN_TOKEN } from '@/global/constance'
import router from '@/router'

const zwRequest = new ZWRequest({
  baseURL: BASE_URL,
  timeout: TIME_OUT
})
const zwRequest2 = new ZWRequest({
  baseURL: BASE_URL,
  timeout: TIME_OUT,
  interceptors: {
    requestSuccessFn: (config) => {
      const token = localCache.getCache(LOGIN_TOKEN)
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    }
  }
})
export { zwRequest, zwRequest2 }

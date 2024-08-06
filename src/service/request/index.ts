import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig } from 'axios'
import type { zwRequestConfig } from './type'

class ZWRequest {
  instance: AxiosInstance
  // request实例 => axios实例
  constructor(config: zwRequestConfig) {
    this.instance = axios.create(config)

    // 拦截器: 显示加载动画/加入token/修改配置
    this.instance.interceptors.request.use(
      (config) => {
        // 显示加载动画/加入token/修改配置
        return config
      },
      (err) => {
        return err
      }
    )
    this.instance.interceptors.response.use(
      (config) => {
        return config.data
      },
      (err) => {
        return err
      }
    )

    // 多个拦截器可以同时存在
    // 添加实例拦截器
    if (config.interceptors) {
      this.instance.interceptors.request.use(
        config.interceptors?.requestSuccessFn,
        config.interceptors?.requestFailureFn
      ),
        this.instance.interceptors.response.use(
          config.interceptors?.responseSuccessFn,
          config.interceptors?.responseFailureFn
        )
    }
  }

  // 封装网络请求的方法
  request<T>(config: AxiosRequestConfig) {
    return this.instance.request<any, T>(config)
  }

  get<T>(config: AxiosRequestConfig) {
    return this.request<T>({ ...config, method: 'GET' })
  }

  post<T>(config: AxiosRequestConfig) {
    return this.request<T>({ ...config, method: 'POST' })
  }

  delete<T>(config: AxiosRequestConfig) {
    return this.request<T>({ ...config, method: 'DELETE' })
  }

  patch<T>(config: AxiosRequestConfig) {
    return this.request<T>({ ...config, method: 'PATCH' })
  }
}

export default ZWRequest

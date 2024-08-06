import type { AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from 'axios'

export interface zwRequestConfig extends AxiosRequestConfig {
  interceptors?: {
    requestSuccessFn?: (config: InternalAxiosRequestConfig) => InternalAxiosRequestConfig
    requestFailureFn?: (err: any) => any
    responseSuccessFn?: (res: AxiosResponse) => AxiosResponse
    responseFailureFn?: (err: any) => any
  }
}

enum CacheEnum {
  Local,
  Session
}

class Cache {
  private storage: Storage
  constructor(type: CacheEnum) {
    this.storage = type === CacheEnum.Local ? localStorage : sessionStorage
  }
  setCache(key: string, value: any) {
    if (value) {
      this.storage.setItem(key, JSON.stringify(value))
    }
  }

  getCache(key: string) {
    const value = this.storage.getItem(key)
    if (value) {
      return JSON.parse(value)
    }
  }

  deleteCache(key: string) {
    this.storage.removeItem(key)
  }

  clearCache() {
    this.storage.clear()
  }
}

const localCache = new Cache(CacheEnum.Local)
const sessonCache = new Cache(CacheEnum.Session)

export { localCache, sessonCache }

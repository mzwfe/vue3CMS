import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
dayjs.extend(utc)
/**
 * 格式化日期
 * @param utcStr 传入需要格式化的时间字符串
 * @param formatStr 格式化的格式 默认为 'YYYY-MM-DD HH:mm:ss'
 * @param timeArea 时区 默认为 8
 * @returns 格式化后的时间字符串
 */
export function formatDate(
  utcStr: string,
  formatStr: string = 'YYYY-MM-DD HH:mm:ss',
  timeArea: number = 8
) {
  return dayjs.utc(utcStr).utcOffset(timeArea).format(formatStr)
}

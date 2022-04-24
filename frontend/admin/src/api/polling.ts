import { isFunction } from '/@/utils/is';

/**
 * @descripting 轮询接口
 * @param {Function} api 接口，使用lambda将参数封装
 * @param {Number} delay 轮询间隔时间
 * @param {Function} terminationChecker 轮询中断器，接收 response, 返回 true 则中断轮询
 * @param {Function} requestResultHandler 轮询数据处理，
 */
export default function polling(
  api: Function,
  delay = 1000,
  terminationChecker?: Function,
  requestResultHandler?: Function,
) {
  return new Promise((resolve) => {
    api()
      .then((data) => {
        if (isFunction(requestResultHandler)) requestResultHandler(data);
        return data;
      })
      .then((data) => {
        // 分段后then 不受 api 的 error影响，相当于finally
        if (!(isFunction(terminationChecker) && terminationChecker(data))) {
          setTimeout(() => {
            resolve(polling(api, delay, terminationChecker, requestResultHandler));
          }, delay);
        } else {
          resolve(data);
        }
      });
  });
}

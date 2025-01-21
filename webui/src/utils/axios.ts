import Axios from 'axios';
import type { AxiosError, AxiosResponse } from 'axios';
import type { ApiSuccess, StatusCode } from '#/api';

export const axios = Axios.create({
  withCredentials: true,
});

axios.interceptors.response.use(
  (res: AxiosResponse) => res,
  (err: AxiosError<ApiSuccess>) => {
    const status = err.response?.status as StatusCode;
    const msg_en = err.response?.data.msg_en ?? '';
    const msg_zh = err.response?.data.msg_zh ?? '';

    const message = useMessage();
    const { returnUserLangText } = useMyI18n();

    const errorMsg = returnUserLangText({
      en: msg_en,
      'zh-CN': msg_zh,
    });

    const { isLoggedIn } = useAuth();

    switch (status) {
      /** token 过期 */
      case 401:
        isLoggedIn.value = false;
        if (errorMsg) message.error(errorMsg);
        break;
      /** 执行失败 */
      case 406:
        if (errorMsg) message.error(errorMsg);
        break;
      case 500:
        isLoggedIn.value = false;
        message.error(
          returnUserLangText({
            en: 'Server error!',
            'zh-CN': '服务器错误！',
          })
        );
        break;
    }

    const error = {
      status,
      msg_en,
      msg_zh,
    };

    return Promise.reject(error);
  }
);

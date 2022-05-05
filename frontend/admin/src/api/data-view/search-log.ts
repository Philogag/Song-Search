import { defHttp } from '/@/utils/http/axios';

enum Api {
  GetSearchLogPage = '/search/logs/get-page',
}

export const apiGetSearchLogPage = (params) => {
  return defHttp.post<any>({ url: Api.GetSearchLogPage, params });
};

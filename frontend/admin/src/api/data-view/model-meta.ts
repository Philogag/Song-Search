import { defHttp } from '/@/utils/http/axios';

enum Api {
  GetModelMeta = '/model-meta/get-page',
}

export const apiGetModelMetaPage = (params) => {
  return defHttp.post<any>({ url: Api.GetModelMeta, params });
};


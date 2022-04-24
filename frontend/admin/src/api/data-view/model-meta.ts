import { defHttp } from '/@/utils/http/axios';

enum Api {
  GetModelMeta = '/model-meta/get-page',
  TrainModel = '/model-meta/run-train',
}

export const apiGetModelMetaPage = (params) => {
  return defHttp.post<any>({ url: Api.GetModelMeta, params });
};

export const apiTrainModel = (modelId: string, forceAll = false) => {
  return defHttp.get<any>({ url: `${Api.TrainModel}/${modelId}?force_all=${forceAll}` });
};

import { defHttp } from '/@/utils/http/axios';

enum Api {
  Search = '/search/',
  GetSearchResult = '/search/get-result',
  SetResultFeedback = '/search/set-user-feedback',
}

export const apiSearch = (params) => {
  return defHttp.get<any>({ url: Api.Search, params });
};

export const apiGetSearchResult = (searchLogId) => {
  return defHttp.get<any>({ url: `${Api.GetSearchResult}/${searchLogId}` });
}

export const apiSetResultFeedback = (searchLogDetailId, score) => {
  return defHttp.get<any>({ url: `${Api.SetResultFeedback}/${searchLogDetailId}?score=${score}` });
}
import { defHttp } from '/@/utils/http/axios';
import { UploadFileParams } from '/#/axios';
import { uploadApi } from '/@/api/sys/upload';

enum Api {
  GetSongsPage = '/songs-source/get-page',
  ImportSongsSource = '/songs-source/import',
}

export const apiGetSongsSourcePage = (params) => {
  return defHttp.post<any>({ url: Api.GetSongsPage, params });
};

export const apiImportSongsSource = (
  params: UploadFileParams,
  onUploadProgress: (progressEvent: ProgressEvent) => void = () => {},
) => {
  return uploadApi(params, onUploadProgress, Api.ImportSongsSource);
};

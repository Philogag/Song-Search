import { UploadApiResult } from '../model/sys/uploadModel';
import { defHttp } from '/@/utils/http/axios';
import { UploadFileParams } from '/#/axios';
import { useGlobSetting } from '/@/hooks/setting';

const { uploadUrl: globalUploadUrl = '' } = useGlobSetting();

/**
 * @description: Upload interface
 */
export function uploadApi(
  params: UploadFileParams,
  onUploadProgress: (progressEvent: ProgressEvent) => void = () => {},
  url = globalUploadUrl,
) {
  return defHttp.uploadFile<UploadApiResult>(
    {
      url: url,
      onUploadProgress,
    },
    params,
  );
}

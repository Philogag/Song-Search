import { defHttp } from '/@/utils/http/axios';

enum Api {
  CheckNewMessages = '/message/check-new',
  SetMessageChecked = '/message/set-message-checked',
}

export function apiCheckNewMessages(params) {
  return defHttp.post<any[]>({
    url: Api.CheckNewMessages,
    params,
  });
}

export function apiSetMessageChecked(message_id: string) {
  return defHttp.get<any>({
    url: `${Api.SetMessageChecked}/${message_id}`,
  });
}

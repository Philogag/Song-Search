import { defHttp } from '/@/utils/http/axios';
import { Result } from "/#/axios";
import { BasicSelectionResult } from "/@/api/model/baseModel";

enum Api {
  GetSportMeetingManagementPage = '/sport-meeting/get-management-list',
  GetSportMeetingSelection = '/sport-meeting/get-selection',
  CreateOrUpdateSportMeetingItem = '/sport-meeting/create-or-update',
  DeleteSportMeetingItem = '/sport-meetings/delete',
}

export const apiGetSportMeetingPage = (params) => {
  return defHttp.post<any>({ url: Api.GetSportMeetingManagementPage, params});
};


export const apiCreateOrUpdateSportMeetingItem = (params) => {
  return defHttp.post<Result>(
    {
      url: Api.CreateOrUpdateSportMeetingItem,
      params,
    },
    {
      isTransformResponse: false,
    }
  )
}


export const apiDeleteSportMeetingItem = (id: string) => {
  return defHttp.get<Result>(
    {
      url: `${Api.DeleteSportMeetingItem}/${id}`
    },
    {
      isTransformResponse: false,
    }
  );
}


export const apiGetSportMeetingSelection = (org_id) => {
  return defHttp.get<BasicSelectionResult[]>(
    {
      url: `${Api.GetSportMeetingSelection}/${org_id}`,
    }
  )
}

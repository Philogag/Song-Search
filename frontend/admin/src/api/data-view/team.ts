import { defHttp } from '/@/utils/http/axios';
import { Result } from "/#/axios";
import { BasicSelectionResult } from "/@/api/model/baseModel";

enum Api {
  GetTeamManagementPage = '/team/get-management-list',
  GetTeamSelection = '/team/get-selection',
  CreateOrUpdateTeamItem = '/team/create-or-update',
  DeleteTeamItem = '/team/delete',
}

export const apiGetTeamPage = (params) => {
  return defHttp.post<any>({ url: Api.GetTeamManagementPage, params});
};


export const apiCreateOrUpdateTeamItem = (params) => {
  return defHttp.post<Result>(
    {
      url: Api.CreateOrUpdateTeamItem,
      params,
    },
    {
      isTransformResponse: false,
    }
  )
}


export const apiDeleteTeamItem = (id: string) => {
  return defHttp.get<Result>(
    {
      url: `${Api.DeleteTeamItem}/${id}`
    },
    {
      isTransformResponse: false,
    }
  );
}


export const apiGetTeamSelectionBySportMeeting = (sport_meeting_id) => {
  return defHttp.get<BasicSelectionResult[]>(
    {
      url: `${Api.GetTeamSelection}/${sport_meeting_id}`,
    }
  )
}

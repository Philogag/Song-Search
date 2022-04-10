import { defHttp } from '/@/utils/http/axios';
import { Result } from "/#/axios";
import { BasicSelectionResult } from "/@/api/model/baseModel";

enum Api {
  GetSportMeetingCompetitionManagementPage = '/sport-meeting-competition/get-management-list',
  GetSportMeetingCompetitionSelection = '/sport-meeting-competition/get-selection',
  CreateOrUpdateSportMeetingCompetitionItem = '/sport-meeting-competition/create-or-update',
  DeleteSportMeetingCompetitionItem = '/sport-meeting-competition/delete',
  GetSportMeetingCompetitionSelectionByPeople = '/sport-meeting-competition/get-selection-by-people/',
}

export const apiGetSportMeetingCompetitionPage = (params) => {
  return defHttp.post<any>({ url: Api.GetSportMeetingCompetitionManagementPage, params});
};


export const apiCreateOrUpdateSportMeetingCompetitionItem = (params) => {
  return defHttp.post<Result>(
    {
      url: Api.CreateOrUpdateSportMeetingCompetitionItem,
      params,
    },
    {
      isTransformResponse: false,
    }
  )
}


export const apiDeleteSportMeetingCompetitionItem = (id: string) => {
  return defHttp.get<Result>(
    {
      url: `${Api.DeleteSportMeetingCompetitionItem}/${id}`
    },
    {
      isTransformResponse: false,
    }
  );
}


export const apiGetSportMeetingCompetitionSelection = (org_id) => {
  return defHttp.get<BasicSelectionResult[]>(
    {
      url: `${Api.GetSportMeetingCompetitionSelection}/${org_id}`,
    }
  )
}

export const apiGetSportMeetingCompetitionSelectionByPeople = (people_id) => {
  return defHttp.get<BasicSelectionResult[]>(
    {
      url: `${Api.GetSportMeetingCompetitionSelectionByPeople}/${people_id}`,
    }
  )
}

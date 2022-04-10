import { BasicColumn } from '/@/components/Table';
import { FormSchema } from '/@/components/Table';
import {getUserOrganizationId, isSuperAdmin} from "/@/tools/checkRole";
import {apiGetSportMeetingSelection} from "/@/api/data-view/sport-meeting";
import {
  apiGetTeamGroupSelectionBySportMeeting
} from "/@/api/constant/team-group";
import {integer} from "vue-types";

export const columns = (show_detail: boolean): BasicColumn[] => [
  {
    title: '所属组织',
    dataIndex: 'organizationName',
    width: 220,
    align: 'center',
    ifShow: show_detail,
  },
  {
    title: '所属运动会',
    dataIndex: 'sportMeetingName',
    width: 240,
    align: 'center',
    ifShow: show_detail,
  },
  {
    title: '名称',
    dataIndex: 'name',
    align: 'center',
  },
  {
    title: '报名人数',
    dataIndex: 'peopleLimit',
    align: 'center',
    customRender: ({record}) => {
      return record.peopleCount * 1 + ' / ' + (record.peopleLimit === 0 ? '-' : `${record.peopleLimit}`);
    }
  },
  {
    title: '号码布',
    dataIndex: 'numberClothBegin',
    align: 'center',
    // @ts-ignore
    customRender: ({record}) => {
      return `${record?.numberClothBegin} ~ ${record?.numberClothEnd}`
    }
  },
  {
    title: '参赛组',
    dataIndex: 'allowedGroupName',
    width: 80,
    align: 'center',
  },
];


export const searchFormSchema = (defaultValue, permission): FormSchema[] => [
  {
    field: 'sportMeetingId',
    label: '运动会：',
    component: 'ApiSelect',
    defaultValue: defaultValue.sportMeetingId,
    componentProps: ({formModel}) => ({
      api: ({id}) => apiGetSportMeetingSelection(id),
      params: {
        id: formModel.organizationId,
      }
    }),
    colProps: {span: 8},
    show: permission.sportMeetingFilter,
  },
  {
    field: 'allowedGroup',
    label: '参赛组: ',
    component: 'ApiSelect',
    componentProps: ({formModel}) => ({
      api: ({id}) => apiGetTeamGroupSelectionBySportMeeting(id),
      params: {
        id: formModel.sportMeetingId,
      },
    }),
    colProps: {span: 8},
  }
]


export const formSchema: FormSchema[] = [
  {
    field: 'id',
    label: 'ID',
    component: 'Input',
    show: false,
  },
  {
    field: 'version',
    label: 'Version',
    component: 'Input',
    required: true,
    defaultValue: 1,
    show: false,
  },
  {
    field: 'organizationId',
    label: '所属组织',
    component: 'ApiSelect',
    componentProps: {
      api: apiGetOrganizationSelection,
    },
    defaultValue: getUserOrganizationId(),
    show: isSuperAdmin(),
    colProps: { lg: 24, md: 24 },
  },
  {
    field: 'sportMeetingId',
    label: '所属运动会',
    component: 'ApiSelect',
    componentProps: ({formModel}) => ({
      api: ({org_id}) => {
        return typeof(org_id) === "string" ? apiGetSportMeetingSelection(org_id) : [];
      },
      params: {
        org_id: formModel.organizationId
      },
      showSearch: true,
      optionFilterProp: 'label',
    }),
    required: true,
    colProps: { lg: 24, md: 24 },
  },
  {
    field: 'name',
    label: '名称',
    component: 'Input',
    required: true,
    colProps: { lg: 24, md: 24 },
  },
  {
    field: 'allowedGroup',
    label: '参加参赛组',
    component: 'ApiSelect',
    componentProps: ({formModel}) => ({
      api: ({id}) => {
        return typeof(id) === "string" ? apiGetTeamGroupSelectionBySportMeeting(id) : [];
      },
      params: {
        id: formModel.sportMeetingId
      },
      mode: "multiple",
      showSearch: true,
      optionFilterProp: 'label',
    }),
    required: true,
    colProps: { lg: 24, md: 24 },
  },
  {
    field: 'dividerDetail',
    label: '详细配置',
    component: 'Divider',
    colProps: { lg: 24, md: 24 },
  },
  {
    field: 'peopleLimit',
    label: '代表队限报人数',
    helpMessage: "填0则不限",
    component: 'InputNumber',
    required: true,
    colProps: { lg: 24, md: 24 },
  },
  {
    field: 'competitionPerPeople',
    label: '单人报名项目数',
    helpMessage: "填0则不限",
    component: 'InputNumber',
    required: true,
    colProps: { lg: 24, md: 24 },
  },
  {
    field: 'numberClothBegin',
    label: '号码布起始',
    helpMessage: '请自行保证不冲突',
    component: 'Input',
    required: true,
    colProps: { lg: 24, md: 24 },
  },
  {
    field: 'numberClothEnd',
    label: '号码布结束',
    helpMessage: '请自行保证不冲突',
    component: 'Input',
    required: true,
    colProps: { lg: 24, md: 24 },
  },
];

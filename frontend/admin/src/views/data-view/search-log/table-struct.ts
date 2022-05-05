import { BasicColumn } from '/@/components/Table';
import { mean } from '../../../utils/helper/arrayHelper';

export const columns = (): BasicColumn[] => [
  {
    title: '创建时间',
    dataIndex: 'createAt',
    align: 'center',
  },
  {
    title: '用户输入',
    dataIndex: 'searchText',
    align: 'center',
  },
  {
    title: '平均置信度',
    dataIndex: 'resultConfidenceAverage',
    align: 'center',
    customRender: ({record}) => {
      if (record.details)
        return (mean(record.details.map((item) => item?.resultConfidence)) * 100).toFixed(1) + '%';
    }
  },
  {
    title: '平均反馈结果',
    dataIndex: 'userFeedbackAverage',
    align: 'center',
    customRender: ({record}) => {
      if (record.details){
        const result = mean(record.details.map((item) => item?.userFeedback).filter((x) => x))
        return result === 0 ? '-' : result.toFixed(1);
      }
    }
  },
];

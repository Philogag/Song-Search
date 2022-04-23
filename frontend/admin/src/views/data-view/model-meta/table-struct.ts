import { BasicColumn } from '/@/components/Table';

export const columns = (): BasicColumn[] => [
  {
    title: '名称',
    dataIndex: 'modelName',
    width: 220,
    align: 'center',
  },
  {
    title: '状态',
    dataIndex: 'author',
    width: 240,
    align: 'center',
  },
  {
    title: '最近训练时间',
    dataIndex: 'lastTrainAt',
    align: 'center',
  },
];

import { BasicColumn } from '/@/components/Table';

export const columns = (): BasicColumn[] => [
  {
    title: '标题',
    dataIndex: 'title',
    width: 220,
    align: 'center',
  },
  {
    title: '作者',
    dataIndex: 'author',
    width: 240,
    align: 'center',
  },
  {
    title: '朝代',
    dataIndex: 'dynasty',
    align: 'center',
  },
  {
    title: 'Tag',
    dataIndex: 'tags',
    align: 'center',
    // customRender: ({record}) => {
    //   return record.peopleCount * 1 + ' / ' + (record.peopleLimit === 0 ? '-' : `${record.peopleLimit}`);
    // }
  },
  {
    title: '导入时间',
    dataIndex: 'createdAt',
    align: 'center',
    // customRender: ({record}) => {
    //   return record.peopleCount * 1 + ' / ' + (record.peopleLimit === 0 ? '-' : `${record.peopleLimit}`);
    // }
  },
];

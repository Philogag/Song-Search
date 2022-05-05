<template>
  <PageWrapper>
    <BasicTable @register="registerTable">
      <template #tableTitle>
        <InputSearch
          v-model:value="params.searchText"
          placeholder="模糊搜索"
          style="width: 300px"
          @search="onSearch"
          allow-clear
        />
      </template>
      <template #expandedRowRender="{ record }">
        <List style="margin: 0" :data-source="record.details">
          <template #renderItem="{ item }">
            <ListItem >
              <Space>
                <span>{{ item.resultTitle }}</span>
                <Tag color="#2db7f5">{{ item.resultDynasty ? item.resultDynasty + ' · ' : '' }}{{ item.resultAuthor }}</Tag>
                <Tag color="#87d068">置信度：{{ item.resultConfidence * 100 }}%</Tag>
                <Tag color="#87d068">反馈：{{ item.userFeedback ?? '-' }}</Tag>
              </Space>
            </ListItem>
          </template>
        </List>
      </template>
    </BasicTable>
  </PageWrapper>
</template>
<script lang="ts">
  import { defineComponent, reactive } from 'vue';
  import { InputSearch, List, ListItem, Tag, Space } from 'ant-design-vue';
  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import { PageWrapper } from '/@/components/Page';
  import { columns } from './table-struct';
  import { apiGetSearchLogPage } from '/@/api/data-view/search-log';
  export default defineComponent({
    name: 'AthletesLevelManagement',
    components: {
      PageWrapper,
      BasicTable,
      TableAction,
      InputSearch,
      Tag,
      List,
      ListItem,
      Space,
    },
    setup() {
      const params = reactive({
        searchText: '',
      });

      const [registerTable, { reload }] = useTable({
        api: async (pageParams) => {
          const res = await apiGetSearchLogPage({
            pageIndex: pageParams.pageSize * (pageParams.page - 1),
            pageSize: pageParams.pageSize,
            searchText: params.searchText ? params.searchText : undefined,
          });
          return {
            items: res.data,
            total: res.filterCount,
          };
        },
        columns: columns(),
        isTreeTable: false,
        pagination: true,
        striped: false,
        showTableSetting: false,
        bordered: true,
        showIndexColumn: false,
        canResize: false,
        // actionColumn: {
        //   width: 120,
        //   title: '操作',
        //   dataIndex: 'action',
        //   slots: { customRender: 'action' },
        //   fixed: undefined,
        // },
        useSearchForm: false,
        // formConfig: {
        //   labelWidth: 120,
        //   schemas: searchFormSchema(),
        //   showResetButton: false,
        // },
      });
      function handleSuccess() {
        reload();
      }
      function onSearch() {
        reload();
      }

      return {
        params,
        registerTable,
        handleSuccess,
        onSearch,
      };
    },
  });
</script>
<style>
  .vben-basic-table {
    padding: 0;
  }
</style>

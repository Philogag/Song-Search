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
      <template #toolbar> </template>
      <template #action="{ record }">
        <TableAction
          :actions="[
            {
              icon: 'codicon:run-all',
              onClick: handleTrainModel.bind(null, record.id),
            },
            {
              icon: 'bx:reset',
              color: 'error',
              popConfirm: {
                title: '是否确认重置模型向量库',
                confirm: handleResetModel.bind(null, record.id),
                placement: 'topRight',
              },
            },
          ]"
        />
      </template>
    </BasicTable>
  </PageWrapper>
</template>
<script lang="ts">
  import { defineComponent, reactive } from 'vue';
  import { InputSearch, message } from 'ant-design-vue';
  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import { PageWrapper } from '/@/components/Page';
  import { columns } from './table-struct';
  import { apiGetModelMetaPage, apiTrainModel } from '/@/api/data-view/model-meta';
  export default defineComponent({
    name: 'AthletesLevelManagement',
    components: {
      PageWrapper,
      BasicTable,
      TableAction,
      InputSearch,
    },
    setup() {
      const params = reactive({
        searchText: '',
      });

      const [registerTable, { reload }] = useTable({
        api: async (pageParams) => {
          const res = await apiGetModelMetaPage({
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
        actionColumn: {
          width: 120,
          title: '操作',
          dataIndex: 'action',
          slots: { customRender: 'action' },
          fixed: undefined,
        },
        useSearchForm: false,
        // formConfig: {
        //   labelWidth: 120,
        //   schemas: searchFormSchema(),
        //   showResetButton: false,
        // },
      });
      function handleTrainModel(id: string) {
        apiTrainModel(id, false).then(() => {
          message.info('模型后台训练中...');
        });
      }
      function handleResetModel(id: string) {
        apiTrainModel(id, true).then(() => {
          message.info('模型后台训练中...');
        });
      }
      function handleSuccess() {
        reload();
      }
      function onSearch() {
        reload();
      }

      return {
        params,
        registerTable,
        handleTrainModel,
        handleResetModel,
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

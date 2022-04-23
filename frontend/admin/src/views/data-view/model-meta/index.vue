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
              onClick: handleRunTrain.bind(null, record.id),
            },
            // {
            //   icon: 'ant-design:delete-outlined',
            //   color: 'error',
            //   popConfirm: {
            //     title: '是否确认删除',
            //     confirm: handleDelete.bind(null, record),
            //     placement: 'topRight',
            //   },
            // },
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
  import { apiGetModelMetaPage } from '/@/api/data-view/model-meta';
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
      function handleRunTrain(id: string) {
        console.log(id);
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
        handleRunTrain,
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

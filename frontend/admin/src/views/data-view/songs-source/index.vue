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
      <template #toolbar>
        <Upload :showUploadList="false" :multiple="false" :customRequest="handleImport">
          <a-button type="primary" preIcon="clarity:import-solid">导入</a-button>
        </Upload>
      </template>
      <template #action="{ record }">
        <TableAction
          :actions="[
            {
              icon: 'ant-design:delete-outlined',
              color: 'error',
              popConfirm: {
                title: '是否确认删除',
                confirm: handleDelete.bind(null, record),
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
  import { InputSearch, message, Upload } from 'ant-design-vue';
  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import { PageWrapper } from '/@/components/Page';
  import { columns } from './table-struct';
  import { apiGetSongsSourcePage, apiImportSongsSource } from '/@/api/data-view/songs-source';
  export default defineComponent({
    name: 'AthletesLevelManagement',
    components: {
      PageWrapper,
      BasicTable,
      TableAction,
      InputSearch,
      Upload,
    },
    setup() {
      const params = reactive({
        searchText: '',
      });

      const [registerTable, { reload }] = useTable({
        api: async (pageParams) => {
          const res = await apiGetSongsSourcePage({
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
      function handleImport({ file }) {
        console.log(file);
        apiImportSongsSource({
          filename: file.name,
          file: file,
        }).then(() => {
          message.success('导入成功');
          reload();
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
        handleImport,
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

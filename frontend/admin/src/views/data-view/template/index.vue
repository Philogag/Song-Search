<template>
  <PageWrapper>
    <BasicTable
      @register="registerTable"
    >
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
        <a-button type="primary" @click="handleCreate"> 新建代表队 </a-button>
      </template>
      <template #action="{ record }">
        <TableAction
          :actions="[
            {
              icon: 'clarity:note-edit-line',
              onClick: handleEdit.bind(null, record),
            },
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
    <Editor @register="registerDrawer" @success="handleSuccess" />
  </PageWrapper>
</template>
<script lang="ts">
  import { defineComponent, reactive } from 'vue';
  import { InputSearch, CheckboxGroup, Checkbox } from "ant-design-vue";
  import { BasicTable, useTable, TableAction } from '/@/components/Table';
  import { useDrawer } from '/@/components/Drawer';
  import { PageWrapper } from '/@/components/Page';
  import Editor from './Editor.vue';
  import { columns, searchFormSchema } from './team.data';
  import {getUserOrganizationId, isSuperAdmin} from "/@/tools/checkRole";
  import {apiDeleteTeamItem, apiGetTeamPage} from "/@/api/data-view/team";
  import { getSportMeetingId } from '../../sport-meeting/get-sport-meeting-id';
  export default defineComponent({
    name: 'AthletesLevelManagement',
    components: {
      PageWrapper,
      BasicTable,
      Editor,
      TableAction,
      InputSearch,
      CheckboxGroup,
      Checkbox,
    },
    setup() {
      const currentSportMeeting = getSportMeetingId();
      const currentOrganization = getUserOrganizationId();
      const showSearchForm = isSuperAdmin() && currentSportMeeting === undefined;

      const params = reactive({
        searchText: "",
      })

      const searchFormSettings = reactive({
        defaultValue: {
          organizationId: currentOrganization,
          sportMeetingId: currentSportMeeting,
        },
        permission: {
          organizationFilter: false,
          sportMeetingFilter: !currentSportMeeting,
        }
      })

      const [registerDrawer, { openDrawer }] = useDrawer();
      const [registerTable, { reload }] = useTable({
        api: async (pageParams) => {
          const res = await apiGetTeamPage({
            pageIndex: pageParams.pageSize * (pageParams.page - 1),
            pageSize: pageParams.pageSize,
            searchText: params.searchText ? params.searchText : undefined,
            filterColumns: {
              organizationId: pageParams.organizationId ? [pageParams.organizationId] : null,
              sportMeetingId: pageParams.sportMeetingId ? [pageParams.sportMeetingId] : null,
              allowedGroup: pageParams.allowedGroup ? pageParams.allowedGroup : null,
            }
          });
          return {
            items: res.data,
            total: res.filterCount,
          }
        },
        columns: columns(showSearchForm),
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
        useSearchForm: true,
        formConfig: {
          labelWidth: 120,
          schemas: searchFormSchema(searchFormSettings.defaultValue, searchFormSettings.permission),
          showResetButton: false,
        },
      });
      function handleCreate() {
        openDrawer(true, {
          isUpdate: false,
        });
      }
      function handleEdit(record: Recordable) {
        openDrawer(true, {
          record,
          isUpdate: true,
        });
      }
      function handleDelete(record: Recordable) {
        apiDeleteTeamItem(record.id).then((res) => {
          if (res.code == 200) {
            // console.log("Delete athletes-level: " + record.id);
            reload();
          }
        })
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
        registerDrawer,
        handleCreate,
        handleEdit,
        handleDelete,
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

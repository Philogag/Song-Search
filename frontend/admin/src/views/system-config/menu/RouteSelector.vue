<template>
  <BasicDrawer
    v-bind="$attrs"
    @register="registerDrawer"
    showFooter
    :title="title"
    width="30%"
    @ok="handleSubmit"
  >
    <Spin :spinning="treeLoading">
      <BasicTree
        :treeData="treeData"
        v-model:checkedKeys="checkedKeys"
        :checkable="true"
        ref="asyncExpandTreeRef"
      />
    </Spin>
  </BasicDrawer>
</template>
<script lang="ts">
import {computed, defineComponent, ref, unref} from 'vue';
  import { BasicDrawer, useDrawerInner } from '/@/components/Drawer';
  import {
    apiGetMenuDataRouteIdList,
    apiSetMenuDataRouteIdList,
  } from "/@/api/system-config/menu";
  import { useMessage } from '/@/hooks/web/useMessage';
  import { BasicTree, TreeActionType } from '/@/components/Tree';
  import {apiGetDataRouteSelection} from "/@/api/system-config/route";
  export default defineComponent({
    name: 'MenuSelector',
    components: { BasicDrawer, BasicTree },
    emits: ['success', 'register'],
    setup(_, { emit }) {
      const { notification } = useMessage();
      const asyncExpandTreeRef = ref<Nullable<TreeActionType>>(null);
      const treeData = ref([]);
      const checkedKeys = ref([]);
      const treeLoading = ref(false);
      const menuId = ref("");
      const menuTitle = ref("");
      const title = computed(() => "授权菜单 - " + unref(menuTitle));

      const build_tree = (value) => {
        return {
          title: value.label,
          key: value.value,
          children: value.children?.map((child) => build_tree(child))
        }
      };

      const [registerDrawer, { setDrawerProps, closeDrawer }] = useDrawerInner(async ({menu_id, menu_title}) => {
        menuId.value = menu_id;
        menuTitle.value = menu_title;
        treeLoading.value = true;
        let tmpTreeData = await apiGetDataRouteSelection();
        //@ts-ignore
        treeData.value = tmpTreeData.map((value) => build_tree(value));
        //@ts-ignore
        checkedKeys.value = await apiGetMenuDataRouteIdList(menu_id);
        // unref(asyncExpandTreeRef)?.expandAll(true);
        treeLoading.value = false;
      });

      async function handleSubmit() {
        try {
          console.log(checkedKeys.value)
          apiSetMenuDataRouteIdList({
            menuId: menuId.value,
            routeIdList: checkedKeys.value,
          }).then(res => {
            if (res.message.length == 0){
              closeDrawer();
              emit('success');
            } else {
              notification.error({
                message: '错误',
                description: res.message.join("\n"),
              });
            }
          })
        } finally {
          setDrawerProps({ confirmLoading: false });
        }
      }
      return {
        title,
        registerDrawer,
        asyncExpandTreeRef,
        treeData,
        checkedKeys,
        treeLoading,
        handleSubmit,
      };
    },
  });
</script>

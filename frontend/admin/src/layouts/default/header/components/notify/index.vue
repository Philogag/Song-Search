<template>
  <div :class="prefixCls">
    <Popover title="" trigger="click" :overlayClassName="`${prefixCls}__overlay`">
      <Badge :count="count" dot :numberStyle="numberStyle">
        <BellOutlined />
      </Badge>
      <template #content>
        <NoticeList :list="messageList" v-if="!messageList.checked" @title-click="onNoticeClick" />
      </template>
    </Popover>
  </div>
</template>
<script lang="ts">
  import { computed, defineComponent, onMounted, onUnmounted, ref } from 'vue';
  import { Popover, Badge } from 'ant-design-vue';
  import { BellOutlined } from '@ant-design/icons-vue';
  import { ListItem } from './data';
  import NoticeList from './NoticeList.vue';
  import { useDesign } from '/@/hooks/web/useDesign';
  import { useMessage } from '/@/hooks/web/useMessage';
  import polling from '/@/api/polling';
  import { apiCheckNewMessages, apiSetMessageChecked } from '/@/api/sys/message';
  import moment from "moment";

  export default defineComponent({
    components: { Popover, BellOutlined, Badge, NoticeList },
    setup(_, { emit }) {
      const { prefixCls } = useDesign('header-notify');
      const { createMessage } = useMessage();
      const pollingCallExit = ref(false);
      const messageList = ref([]);
      const lastMessageAt = ref<Nullable<String>>(undefined);

      const count = computed(() => {
        return messageList.value.length;
      });

      function onNoticeClick(record: ListItem) {
        apiSetMessageChecked(record.id).then(() => {
          record.titleDelete = !record.titleDelete;
        });
      }

      async function requestResultHandler(data) {
        messageList.value.length = 0;
        data.forEach((item) => {
          messageList.value.unshift({
            id: item.id,
            title: item.title,
            description: item.content,
            checked: item.checked,
            avatar: item.status === 'success' ? '' : '',
          });
        });
        lastMessageAt.value = Math.max(
          lastMessageAt.value,
          ...data.map((item) => item.handledAt),
        );
        console.log(lastMessageAt.value);
      }

      onMounted(() => {
        pollingCallExit.value = false;
        polling(
          () =>
            apiCheckNewMessages({
              after: lastMessageAt.value,
            }),
          30 * 1000, // 30s
          () => pollingCallExit.value,
          requestResultHandler,
        );
      });
      onUnmounted(() => {
        pollingCallExit.value = true;
      });

      return {
        prefixCls,
        messageList,
        count,
        onNoticeClick,
        numberStyle: {},
      };
    },
  });
</script>
<style lang="less">
  @prefix-cls: ~'@{namespace}-header-notify';

  .@{prefix-cls} {
    padding-top: 2px;

    &__overlay {
      width: 360px;
    }

    .ant-tabs-content {
      width: 300px;
    }

    .ant-badge {
      font-size: 18px;

      .ant-badge-multiple-words {
        padding: 0 4px;
      }

      svg {
        width: 0.9em;
      }
    }
  }
</style>

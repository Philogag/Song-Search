<template>
  <div class="fill-height">
    <img class="image-backgrond fixed" src="../../assets/images/search_bg.jpg" alt="" />
    <Layout class="w-full">
      <Header class="block-search mb-12 fixed" style="z-index: 1">
        <div style="width: fit-content; margin: 0 auto;">
          <InputSearch
            class="search-input"
            style="--border-radius: 14px"
            v-model:value="searchText"
            placeholder="输入搜索内容"
            enter-button
            size="large"
            @search="handleSearch"
          />
        </div>
      </Header>

      <Content v-if="searchResult.length > 0">
      <div class="block-result border">
        <div class="m-6 mt-2 mb-2">
         <List :dataSource="searchResult">
          <template #renderItem="{ item }">
            <ListItem>
              <template #actions>
                <Rate
                  allowHalf
                  v-model:value="item.userFeedback"
                  :allowClear="false"
                  @change="(value) => handleSetRate(item.id, value)"
                />
              </template>
              <ListItemMeta :description="item.content">
                <template #title>
                  {{ item.title }}
                  <Tag color="#2db7f5">{{ item.dynasty ? item.dynasty + ' · ' : '' }}{{ item.author }}</Tag>
                  <Tag color="#87d068">{{ (item.resultConfidence * 100).toFixed(1) }}%</Tag>
                </template>
              </ListItemMeta>
            </ListItem>
          </template>
        </List>
        </div>
      </div>
      </Content>
    </Layout>

  </div>
</template>
<script>
import { defineComponent, onMounted, ref } from 'vue';
import { InputSearch, Tag, List, ListItem, ListItemMeta, Rate,  } from 'ant-design-vue';
import polling from '/@/api/polling';
import { apiSearch, apiGetSearchResult, apiSetResultFeedback } from '/@/api/search';
import { data } from './test';
export default defineComponent({
  name: 'Search',
  components: {
    InputSearch,
    List,
    ListItem,
    ListItemMeta,
    Rate,
    Tag,
  },
  setup() {
    const show = ref(false);
    const searchText = ref('飞流直下三千尺，疑似银河落九川');
    const searchResult = ref([]);

    onMounted(() => {
      setTimeout(() => {
        show.value = true;
      }, 300);
    });

    function handleSearch() {
      // 发送搜索请求
      apiSearch({
        search_text: searchText.value,
      })
        .then((res) => {
          // 获取搜索id
          if (res.searchLogId) {
            return res.searchLogId;
          } else {
            throw 'res.searchLogId not exist.';
          }
        })
        .then((searchLogId) =>
          // 轮询查询结果
          polling(
            () => apiGetSearchResult(searchLogId),
            1000,
            (data) => data.length > 0,
          ),
        )
        .then((data) => {
          // 渲染结果
          searchResult.value = data;
        });
    }

    function handleSetRate(id, value) {
      apiSetResultFeedback(id, value);
    }

    return {
      show,
      searchText,
      searchResult,
      handleSearch,
      handleSetRate,
    };
  },
});
</script>
<style>
.fixed {
  position: fixed;
}

.image-backgrond {
  -webkit-user-drag: none;
  width: 100%;
  height: 100%;
  opacity: 0.4;
  z-index: -999;
}

/* 定义变量 */

.search-input {
  margin: auto auto;
  width: 400px;
  box-shadow: 6px 6px 5px #888888;
  --border-radius: 0px;
  border-radius: var(--border-radius);
}
.search-input input {
  border-top-left-radius: var(--border-radius);
  border-bottom-left-radius: var(--border-radius);
}
.search-input button {
  border-top-right-radius: var(--border-radius);
  border-bottom-right-radius: var(--border-radius);
}
.search-input .ant-input-group-addon {
  background: transparent;
}

.block-search {
  margin: auto;
  margin-top: 20px;
  margin-bottom: 20px;
  width: 100%;
  position: fixed;
}
.block-result {
  margin: 0 auto;
  margin-top: 90px;
  margin-bottom: 20px;
  width: 70%;
  background: white;
  border-radius: 14px;
}

.result-card {
  width: 100%;
}

.result-content {
  white-space: pre-wrap;
}

.fill-height {
  width: 100%;
  min-height: 100%;
  display: flex;
}

.ant-list-item-meta-title {
  font-size: 22px;
}
.ant-list-item-meta-description {
  color: rgb(82, 82, 82);
}
</style>

<template>
  <div>
    <transition name="transitionFade">
      <img class="image-backgrond fixed" src="../../assets/images/search_bg.jpg" alt="" />
    </transition>

    <InputSearch
      class="search-input fixed"
      style="--border-radius: 14px"
      v-model:value="searchText"
      placeholder="输入搜索内容"
      enter-button
      size="large"
      @search="handleSearch"
    />
  </div>
</template>
<script>
  import { defineComponent, onMounted, ref } from 'vue';
  import { InputSearch } from 'ant-design-vue';
  export default defineComponent({
    name: 'Search',
    components: {
      InputSearch,
    },
    setup() {
      const show = ref(false);
      const searchText = ref('');

      onMounted(() => {
        setTimeout(() => {
          show.value = true;
        }, 300);
      });

      function handleSearch() {}

      return {
        show,
        searchText,
        handleSearch,
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
  }
  .transitionFade-enter-active {
    transition: opacity 2s;
  }
  .transitionFade-enter-to {
    opacity: 1;
  }
  .transitionFade-enter {
    opacity: 0;
  }

  /* 定义变量 */

  .search-input {
    width: 400px;
    left: 50%;
    top: 40%;
    transform: translate(-50%, -50%);
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
</style>

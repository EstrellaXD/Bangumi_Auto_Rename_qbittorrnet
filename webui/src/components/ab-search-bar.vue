<script lang="ts" setup>
import { vOnClickOutside } from '@vueuse/components';
import type { BangumiRule } from '#/bangumi';

defineEmits<{
  (e: 'add-bangumi', bangumiRule: BangumiRule): void;
}>();

const showProvider = ref(false);
const { providers, provider, loading, inputValue, bangumiList } = storeToRefs(
  useSearchStore()
);
const { getProviders, onSearch, clearSearch } = useSearchStore();

onMounted(() => {
  getProviders();
});

function onSelect(site: string) {
  provider.value = site;
  showProvider.value = false;
}
</script>

<template>
  <ab-search
    v-model:inputValue="inputValue"
    :provider="provider"
    :loading="loading"
    @search="onSearch"
    @select="() => (showProvider = !showProvider)"
  />

  <div
    v-show="showProvider"
    v-on-click-outside="() => (showProvider = false)"
    abs
    top-84
    left-540
    w-100
    rounded-12
    shadow
    bg-white
    z-99
    overflow-hidden
  >
    <div
      v-for="site in providers"
      :key="site"
      hover:bg-theme-row
      is-btn
      @click="() => onSelect(site)"
    >
      <div text="h3 primary" hover="text-white" p-12 truncate>
        {{ site }}
      </div>
    </div>
  </div>

  <div v-on-click-outside="clearSearch" abs top-84 left-192 z-8>
    <transition-group name="fade-list" tag="ul" space-y-12>
      <li v-for="bangumi in bangumiList" :key="bangumi.order">
        <ab-bangumi-card
          :bangumi="bangumi.value"
          type="search"
          @click="() => $emit('add-bangumi', bangumi.value)"
        />
      </li>
    </transition-group>
  </div>
</template>

<style lang="scss" scoped></style>

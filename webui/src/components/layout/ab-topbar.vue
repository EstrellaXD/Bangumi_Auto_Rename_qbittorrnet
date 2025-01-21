<script lang="ts" setup>
import {
  Format,
  Me,
  Pause,
  PlayOne,
  Power,
  Refresh,
} from '@icon-park/vue-next';
import { ruleTemplate } from '#/bangumi';
import type { BangumiRule } from '#/bangumi';

const { t, changeLocale } = useMyI18n();
const { running, onUpdate, offUpdate } = useAppInfo();

const showAccount = ref(false);
const showAddRSS = ref(false);
const searchRule = ref<BangumiRule>();

const { start, pause, shutdown, restart, resetRule } = useProgramStore();
const { refreshPoster } = useBangumiStore();

const items = [
  {
    id: 1,
    label: () => t('topbar.start'),
    icon: PlayOne,
    handle: start,
  },
  {
    id: 2,
    label: () => t('topbar.pause'),
    icon: Pause,
    handle: pause,
  },
  {
    id: 3,
    label: () => t('topbar.restart'),
    icon: Refresh,
    handle: restart,
  },
  {
    id: 4,
    label: () => t('topbar.shutdown'),
    icon: Power,
    handle: shutdown,
  },
  {
    id: 5,
    label: () => t('topbar.refresh_poster'),
    icon: Refresh,
    handle: refreshPoster,
  },
  {
    id: 6,
    label: () => t('topbar.reset_rule'),
    icon: Format,
    handle: resetRule,
  },
  {
    id: 7,
    label: () => t('topbar.profile.title'),
    icon: Me,
    handle: () => {
      showAccount.value = true;
    },
  },
];

const onSearchFocus = ref(false);

function addSearchResult(bangumi: BangumiRule) {
  showAddRSS.value = true;
  searchRule.value = bangumi;
  console.log('searchRule', searchRule.value);
}

watch(showAddRSS, (val) => {
  if (!val) {
    searchRule.value = ruleTemplate;
    setTimeout(() => {
      onSearchFocus.value = false;
    }, 300);
  }
});

onBeforeMount(() => {
  onUpdate();
});

onUnmounted(() => {
  offUpdate();
});
</script>

<template>
  <div
    h="pc:60 50"
    bg-theme-row
    text-white
    rounded="pc:16 10"
    fx-cer
    px="pc:24 15"
  >
    <div flex="~ gap-x-16">
      <div fx-cer gap-x="pc:16 10">
        <img src="/images/logo-light.svg" alt="favicon" wh="pc:24 20" />
        <img
          v-show="onSearchFocus === false"
          src="/images/AutoBangumi.svg"
          alt="AutoBangumi"
          rel
          h="18 pc:24"
          pc:top-2
        />
      </div>

      <div hidden pc:block>
        <ab-search-bar @add-bangumi="addSearchResult" />
      </div>
    </div>

    <div ml-auto>
      <ab-status-bar
        :items="items"
        :running="running"
        @click-add="() => (showAddRSS = true)"
        @change-lang="changeLocale"
      />
    </div>
    <ab-change-account v-model:show="showAccount"></ab-change-account>
    <ab-add-rss
      v-model:show="showAddRSS"
      v-model:rule="searchRule"
    ></ab-add-rss>
  </div>
</template>

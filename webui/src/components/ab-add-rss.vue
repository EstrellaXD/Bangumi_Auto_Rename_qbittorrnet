<script lang="ts" setup>
import type { BangumiRule } from '#/bangumi';
import type { RSS } from '#/rss';
import { rssTemplate } from '#/rss';
import { ruleTemplate } from '#/bangumi';

/** v-model show */
const show = defineModel('show', { default: false });

const message = useMessage();
const { getAll } = useBangumiStore();
const { t } = useMyI18n();

const rss = ref<RSS>(rssTemplate);
const rule = defineModel<BangumiRule>('rule', { default: ruleTemplate });
const parserType = ['mikan', 'tmdb', 'parser'];

const windowState = reactive({
  loading: false,
  rule: false,
  next: false,
});
const loading = reactive({
  collect: false,
  subscribe: false,
});

watch(show, (val) => {
  if (!val) {
    rss.value = rssTemplate;
    setTimeout(() => {
      windowState.next = false;
    }, 300);
  } else if (val && rule.value.official_title !== '') {
    windowState.next = true;
    windowState.rule = true;
  }
});

function addRss() {
  if (rss.value.url === '') {
    message.error(t('notify.please_enter', [t('notify.rss_link')]));
  } else if (rss.value.aggregate) {
    useApi(apiRSS.add, {
      showMessage: true,
      onBeforeExecute() {
        windowState.loading = true;
      },
      onSuccess() {
        show.value = false;
      },
      onFinally() {
        windowState.loading = false;
      },
    }).execute(rss.value);
  } else {
    useApi(apiDownload.analysis, {
      showMessage: true,
      onBeforeExecute() {
        windowState.loading = true;
      },
      onSuccess(res) {
        rule.value = res;
        windowState.next = true;
        windowState.rule = true;
      },
      onFinally() {
        windowState.loading = false;
      },
    }).execute(rss.value);
  }
}

function collect() {
  if (rule.value) {
    useApi(apiDownload.collection, {
      showMessage: true,
      onBeforeExecute() {
        loading.collect = true;
      },
      onSuccess() {
        getAll();
        show.value = false;
      },
      onFinally() {
        loading.collect = false;
      },
    }).execute(rule.value);
  }
}

function subscribe() {
  if (rule.value) {
    useApi(apiDownload.subscribe, {
      showMessage: true,
      onBeforeExecute() {
        loading.subscribe = true;
      },
      onSuccess() {
        getAll();
        show.value = false;
      },
      onFinally() {
        loading.subscribe = false;
      },
    }).execute(rule.value, rss.value);
  }
}
</script>

<template>
  <ab-popup v-model:show="show" :title="$t('topbar.add.title')" css="w-360">
    <div v-if="!windowState.next" space-y-12>
      <ab-setting
        v-model:data="rss.url"
        :label="$t('topbar.add.rss_link')"
        type="input"
        :prop="{
          placeholder: $t('topbar.add.placeholder_link'),
        }"
      ></ab-setting>

      <ab-setting
        v-model:data="rss.name"
        :label="$t('topbar.add.name')"
        type="input"
        :prop="{
          placeholder: $t('topbar.add.placeholder_name'),
        }"
      ></ab-setting>

      <ab-setting
        v-model:data="rss.aggregate"
        :label="$t('topbar.add.aggregate')"
        type="switch"
      ></ab-setting>

      <ab-setting
        v-model:data="rss.parser"
        :label="$t('topbar.add.parser')"
        type="select"
        :prop="{
          items: parserType,
        }"
        :bottom-line="true"
      ></ab-setting>

      <div flex="~ justify-end">
        <ab-button size="small" :loading="windowState.loading" @click="addRss">
          {{ $t('topbar.add.button') }}
        </ab-button>
      </div>
    </div>

    <div v-else-if="windowState.rule">
      <ab-rule v-model:rule="rule"></ab-rule>
      <div flex="~ justify-end gap-x-10">
        <ab-button size="small" :loading="loading.collect" @click="collect">
          {{ $t('topbar.add.collect') }}
        </ab-button>

        <ab-button size="small" :loading="loading.subscribe" @click="subscribe">
          {{ $t('topbar.add.subscribe') }}
        </ab-button>
      </div>
    </div>
  </ab-popup>
</template>

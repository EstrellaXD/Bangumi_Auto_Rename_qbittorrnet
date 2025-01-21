<script lang="ts" setup>
import type { RssParser, RssParserLang } from '#/config';
import type { SettingItem } from '#/components';

const { t } = useMyI18n();
const { getSettingGroup } = useConfigStore();

const parser = getSettingGroup('rss_parser');

/** @ts-expect-error Incorrect order */
const langs: RssParserLang = ['zh', 'en', 'jp'];

const items: SettingItem<RssParser>[] = [
  {
    configKey: 'enable',
    label: () => t('config.parser_set.enable'),
    type: 'switch',
  },
  {
    configKey: 'language',
    label: () => t('config.parser_set.language'),
    type: 'select',
    prop: {
      items: langs,
    },
  },
  {
    configKey: 'filter',
    label: () => t('config.parser_set.exclude'),
    type: 'dynamic-tags',
  },
];
</script>

<template>
  <ab-fold-panel :title="$t('config.parser_set.title')">
    <div space-y-12>
      <ab-setting
        v-for="i in items"
        :key="i.configKey"
        v-bind="i"
        v-model:data="parser[i.configKey]"
      ></ab-setting>
    </div>
  </ab-fold-panel>
</template>

<script lang="ts" setup>
import type { BangumiRule } from '#/bangumi';
import type { SettingItem } from '#/components';

const { t } = useMyI18n();

const rule = defineModel<BangumiRule>('rule', {
  required: true,
});

const items: SettingItem<BangumiRule>[] = [
  {
    configKey: 'official_title',
    label: () => t('homepage.rule.official_title'),
    type: 'input',
    prop: {
      type: 'text',
    },
  },
  {
    configKey: 'year',
    label: () => t('homepage.rule.year'),
    type: 'input',
    css: 'w-72',
    prop: {
      type: 'text',
    },
  },
  {
    configKey: 'season',
    label: () => t('homepage.rule.season'),
    type: 'input',
    css: 'w-72',
    prop: {
      type: 'number',
    },
    bottomLine: true,
  },
  {
    configKey: 'offset',
    label: () => t('homepage.rule.offset'),
    type: 'input',
    css: 'w-72',
    prop: {
      type: 'number',
    },
  },
  {
    configKey: 'filter',
    label: () => t('homepage.rule.exclude'),
    type: 'dynamic-tags',
    bottomLine: true,
  },
];
</script>

<template>
  <div space-y-12>
    <ab-setting
      v-for="i in items"
      :key="i.configKey"
      v-bind="i"
      v-model:data="rule[i.configKey]"
    ></ab-setting>
  </div>
</template>

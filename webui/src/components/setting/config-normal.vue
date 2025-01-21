<script lang="ts" setup>
import type { Log, Program } from '#/config';
import type { SettingItem } from '#/components';

const { t } = useMyI18n();
const { getSettingGroup } = useConfigStore();

const program = getSettingGroup('program');
const log = getSettingGroup('log');

const programItems: SettingItem<Program>[] = [
  {
    configKey: 'rss_time',
    label: () => t('config.normal_set.rss_interval'),
    type: 'input',
    css: 'w-72',
    prop: {
      type: 'number',
      placeholder: 'port',
    },
  },
  {
    configKey: 'rename_time',
    label: () => t('config.normal_set.rename_interval'),
    type: 'input',
    css: 'w-72',
    prop: {
      type: 'number',
      placeholder: 'port',
    },
  },
  {
    configKey: 'webui_port',
    label: () => t('config.normal_set.web_port'),
    type: 'input',
    css: 'w-72',
    prop: {
      type: 'number',
      placeholder: 'port',
    },
    bottomLine: true,
  },
];

const logItems: SettingItem<Log> = {
  configKey: 'debug_enable',
  label: () => t('config.normal_set.debug'),
  type: 'switch',
};
</script>

<template>
  <ab-fold-panel :title="$t('config.normal_set.title')">
    <div space-y-12>
      <ab-setting
        v-for="i in programItems"
        :key="i.configKey"
        v-bind="i"
        v-model:data="program[i.configKey]"
      ></ab-setting>

      <ab-setting
        v-bind="logItems"
        v-model:data="log[logItems.configKey]"
      ></ab-setting>
    </div>
  </ab-fold-panel>
</template>

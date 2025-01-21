<script lang="ts" setup>
import type { Downloader, DownloaderType } from '#/config';
import type { SettingItem } from '#/components';

const { t } = useMyI18n();
const { getSettingGroup } = useConfigStore();

const downloader = getSettingGroup('downloader');
const downloaderType: DownloaderType = ['qbittorrent'];

const items: SettingItem<Downloader>[] = [
  {
    configKey: 'type',
    label: () => t('config.downloader_set.type'),
    type: 'select',
    css: 'w-115',
    prop: {
      items: downloaderType,
    },
  },
  {
    configKey: 'host',
    label: () => t('config.downloader_set.host'),
    type: 'input',
    prop: {
      type: 'text',
      placeholder: '127.0.0.1:8989',
    },
  },
  {
    configKey: 'username',
    label: () => t('config.downloader_set.username'),
    type: 'input',
    prop: {
      type: 'text',
      placeholder: 'admin',
    },
  },
  {
    configKey: 'password',
    label: () => t('config.downloader_set.password'),
    type: 'input',
    prop: {
      type: 'text',
      placeholder: 'admindmin',
    },
    bottomLine: true,
  },
  {
    configKey: 'path',
    label: () => t('config.downloader_set.path'),
    type: 'input',
    prop: {
      type: 'text',
      placeholder: '/downloads/Bangumi',
    },
  },
  {
    configKey: 'ssl',
    label: () => t('config.downloader_set.ssl'),
    type: 'switch',
  },
];
</script>

<template>
  <ab-fold-panel :title="$t('config.downloader_set.title')">
    <div space-y-12>
      <ab-setting
        v-for="i in items"
        :key="i.configKey"
        v-bind="i"
        v-model:data="downloader[i.configKey]"
      ></ab-setting>
    </div>
  </ab-fold-panel>
</template>

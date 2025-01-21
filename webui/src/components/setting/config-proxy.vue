<script lang="ts" setup>
import type { Proxy, ProxyType } from '#/config';
import type { SettingItem } from '#/components';

const { t } = useMyI18n();
const { getSettingGroup } = useConfigStore();

const proxy = getSettingGroup('proxy');
const proxyType: ProxyType = ['http', 'https', 'socks5'];

const items: SettingItem<Proxy>[] = [
  {
    configKey: 'enable',
    label: () => t('config.proxy_set.enable'),
    type: 'switch',
  },
  {
    configKey: 'type',
    label: () => t('config.proxy_set.type'),
    type: 'select',
    prop: {
      items: proxyType,
    },
    bottomLine: true,
  },
  {
    configKey: 'host',
    label: () => t('config.proxy_set.host'),
    type: 'input',
    prop: {
      type: 'text',
      placeholder: '127.0.0.1',
    },
  },
  {
    configKey: 'port',
    label: () => t('config.proxy_set.port'),
    type: 'input',
    prop: {
      type: 'text',
      placeholder: '7890',
    },
  },
  {
    configKey: 'username',
    label: () => t('config.proxy_set.username'),
    type: 'input',
    prop: {
      type: 'text',
      placeholder: 'username',
    },
  },
  {
    configKey: 'password',
    label: () => t('config.proxy_set.password'),
    type: 'input',
    prop: {
      type: 'text',
      placeholder: 'password',
    },
  },
];
</script>

<template>
  <ab-fold-panel :title="$t('config.proxy_set.title')">
    <div space-y-12>
      <ab-setting
        v-for="i in items"
        :key="i.configKey"
        v-bind="i"
        v-model:data="proxy[i.configKey]"
      ></ab-setting>
    </div>
  </ab-fold-panel>
</template>

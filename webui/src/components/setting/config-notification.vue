<script lang="ts" setup>
import type { Notification, NotificationType } from '#/config';
import type { SettingItem } from '#/components';

const { t } = useMyI18n();
const { getSettingGroup } = useConfigStore();

const notification = getSettingGroup('notification');
const notificationType: NotificationType = [
  'telegram',
  'server-chan',
  'bark',
  'wecom',
  'wecom-robot'
];

const items: SettingItem<Notification>[] = [
  {
    configKey: 'enable',
    label: () => t('config.notification_set.enable'),
    type: 'switch',
    bottomLine: true,
  },
  {
    configKey: 'type',
    label: () => t('config.notification_set.type'),
    type: 'select',
    css: 'w-140',
    prop: {
      items: notificationType,
    },
  },
  {
    configKey: 'token',
    label: () => t('config.notification_set.token'),
    type: 'input',
    prop: {
      type: 'text',
      placeholder: 'token',
    },
  },
  {
    configKey: 'chat_id',
    label: () => t('config.notification_set.chat_id'),
    type: 'input',
    prop: {
      type: 'text',
      placeholder: 'chat id',
    },
  },
];
</script>

<template>
  <ab-fold-panel :title="$t('config.notification_set.title')">
    <div space-y-12>
      <ab-setting
        v-for="i in items"
        :key="i.configKey"
        v-bind="i"
        v-model:data="notification[i.configKey]"
      ></ab-setting>
    </div>
  </ab-fold-panel>
</template>

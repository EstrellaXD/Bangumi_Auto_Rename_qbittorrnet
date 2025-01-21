<script lang="ts" setup>
import type { BangumiManage, RenameMethod } from '#/config';
import type { SettingItem } from '#/components';

const { t } = useMyI18n();
const { getSettingGroup } = useConfigStore();

const manage = getSettingGroup('bangumi_manage');
const renameMethod: RenameMethod = ['normal', 'pn', 'advance', 'none'];

const items: SettingItem<BangumiManage>[] = [
  {
    configKey: 'enable',
    label: () => t('config.manage_set.enable'),
    type: 'switch',
  },
  {
    configKey: 'rename_method',
    label: () => t('config.manage_set.method'),
    type: 'select',
    prop: {
      items: renameMethod,
    },
    bottomLine: true,
  },
  {
    configKey: 'eps_complete',
    label: () => t('config.manage_set.eps'),
    type: 'switch',
  },
  {
    configKey: 'group_tag',
    label: () => t('config.manage_set.group_tag'),
    type: 'switch',
  },
  {
    configKey: 'remove_bad_torrent',
    label: () => t('config.manage_set.delete_bad_torrent'),
    type: 'switch',
  },
];
</script>

<template>
  <ab-fold-panel :title="$t('config.manage_set.title')">
    <div space-y-12>
      <ab-setting
        v-for="i in items"
        :key="i.configKey"
        v-bind="i"
        v-model:data="manage[i.configKey]"
      ></ab-setting>
    </div>
  </ab-fold-panel>
</template>

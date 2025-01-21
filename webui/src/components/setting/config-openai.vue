<script lang="ts" setup>
import { Caution } from '@icon-park/vue-next';
import type { SettingItem } from '#/components';
import type { ExperimentalOpenAI, OpenAIModel, OpenAIType } from '#/config';

const { t } = useMyI18n();
const { getSettingGroup } = useConfigStore();

const openAI = getSettingGroup('experimental_openai');
const openAIModels: OpenAIModel = ['gpt-3.5-turbo'];
const openAITypes: OpenAIType = ['openai', 'azure'];

const sharedItems: SettingItem<ExperimentalOpenAI>[] = [
  {
    configKey: 'enable',
    label: () => t('config.experimental_openai_set.enable'),
    type: 'switch',
  },
  {
    configKey: 'api_type',
    label: () => t('config.experimental_openai_set.api_type'),
    type: 'select',
    prop: {
      items: openAITypes,
    },
  },
  {
    configKey: 'api_key',
    label: () => t('config.experimental_openai_set.api_key'),
    type: 'input',
    prop: {
      type: 'password',
      placeholder: 'e.g: sk-3Bl****w2E9kW',
    },
  },
  {
    configKey: 'api_base',
    label: () => t('config.experimental_openai_set.api_base'),
    type: 'input',
    prop: {
      type: 'url',
      placeholder: 'OpenAI API Base URL',
    },
  },
];
const openAIItems: SettingItem<ExperimentalOpenAI>[] = [
  ...sharedItems,
  {
    configKey: 'model',
    label: () => t('config.experimental_openai_set.model'),
    type: 'select',
    prop: {
      items: openAIModels,
    },
  },
];

const azureItems: SettingItem<ExperimentalOpenAI>[] = [
  ...sharedItems,
  {
    configKey: 'api_version',
    label: () => t('config.experimental_openai_set.api_version'),
    type: 'input',
    prop: {
      type: 'text',
      placeholder: 'e.g: 2023-05-15',
    },
  },
  {
    configKey: 'deployment_id',
    label: () => t('config.experimental_openai_set.deployment_id'),
    type: 'input',
    prop: {
      type: 'text',
      placeholder: 'e.g: gpt-35-turbo',
    },
  },
];
</script>

<template>
  <ab-fold-panel :title="$t('config.experimental_openai_set.title')">
    <div fx-cer gap-2 mb-4 p-2 bg-amber-300 rounded-4>
      <Caution />
      <span>{{ $t('config.experimental_openai_set.warning') }}</span>
    </div>

    <div space-y-12>
      <ab-setting
        v-for="i in openAI.api_type === 'azure' ? azureItems : openAIItems"
        :key="i.configKey"
        v-bind="i"
        v-model:data="openAI[i.configKey]"
      ></ab-setting>
    </div>
  </ab-fold-panel>
</template>

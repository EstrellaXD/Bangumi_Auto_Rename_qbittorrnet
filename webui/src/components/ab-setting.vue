<script lang="ts" setup>
import { NDynamicTags } from 'naive-ui';
import type { AbSettingProps } from '#/components';

withDefaults(defineProps<AbSettingProps>(), {
  css: '',
  bottomLine: false,
});

const data = defineModel<any>('data');
</script>

<template>
  <div>
    <ab-label :label="label">
      <AbSwitch
        v-if="type === 'switch'"
        v-model:checked="data"
        v-bind="prop"
        :class="css"
      ></AbSwitch>

      <AbSelect
        v-else-if="type === 'select'"
        v-model="data"
        v-bind="prop"
        :class="css"
      ></AbSelect>

      <input
        v-else-if="type === 'input'"
        v-model="data"
        ab-input
        :class="css"
        v-bind="prop"
      />

      <div v-else-if="type === 'dynamic-tags'" max-w-200 overflow-auto pb-1>
        <NDynamicTags v-model:value="data" size="small"></NDynamicTags>
      </div>
    </ab-label>

    <div v-if="bottomLine" line my-12></div>
  </div>
</template>

<script lang="ts" setup>
definePage({
  name: 'Config',
});

const { getConfig, setConfig } = useConfigStore();
const { isMobile } = useBreakpointQuery();

onActivated(() => {
  getConfig();
});
</script>

<template>
  <div overflow-auto mt-12 flex-grow>
    <div h-full>
      <div grid="~ pc:cols-2 gap-20" mb-auto>
        <div space-y-20>
          <config-normal></config-normal>

          <config-parser></config-parser>

          <config-download></config-download>

          <config-manage></config-manage>
        </div>

        <div space-y-20>
          <config-notification></config-notification>

          <config-proxy></config-proxy>

          <config-player></config-player>

          <config-openai></config-openai>
        </div>
      </div>

      <div fx-cer justify-end gap-8 mt-20>
        <ab-button
          :class="[{ 'flex-1': isMobile }]"
          type="warn"
          @click="getConfig"
        >
          {{ $t('config.cancel') }}
        </ab-button>
        <ab-button
          :class="[{ 'flex-1': isMobile }]"
          type="primary"
          @click="setConfig"
        >
          {{ $t('config.apply') }}
        </ab-button>
      </div>
    </div>
  </div>
</template>

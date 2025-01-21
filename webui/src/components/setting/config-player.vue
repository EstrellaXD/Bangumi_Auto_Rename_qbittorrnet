<script lang="ts" setup>
const { types, type, url } = storeToRefs(usePlayerStore());
</script>

<template>
  <ab-fold-panel :title="$t('config.media_player_set.title')">
    <div space-y-12>
      <ab-setting
        v-model:data="type"
        type="select"
        :label="$t('config.media_player_set.type')"
        :prop="{ items: types }"
      ></ab-setting>

      <ab-setting
        v-model:data="url"
        type="input"
        :label="$t('config.media_player_set.url')"
        :prop="{ placeholder: 'media player url' }"
      ></ab-setting>
    </div>
  </ab-fold-panel>
</template>

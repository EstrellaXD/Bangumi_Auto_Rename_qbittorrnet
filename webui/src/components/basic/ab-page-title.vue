<script lang="ts" setup>
withDefaults(
  defineProps<{
    title: string;
  }>(),
  {
    title: 'title',
  }
);
</script>

<template>
  <div fx-cer gap-x-12>
    <div text="pc:h1 h2">{{ title }}</div>
    <div w-160 h-3 bg-theme-row rounded-full></div>
  </div>
</template>

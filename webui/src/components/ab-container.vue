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
  <div rounded-10 overflow-hidden>
    <div
      bg-theme-row
      w-full
      text-white
      px-20
      h="38 pc:45"
      fx-cer
      justify-between
      select-none
    >
      <div text="h3 pc:h2">{{ title }}</div>

      <slot name="title-right"></slot>
    </div>

    <div p="14 pc:20" bg-white text="14 inherit">
      <slot></slot>
    </div>
  </div>
</template>

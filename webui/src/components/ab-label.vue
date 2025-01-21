<script lang="ts" setup>
const props = withDefaults(
  defineProps<{
    label: string | (() => string);
  }>(),
  {
    label: '',
  }
);

const abLabel = computed(() => {
  if (typeof props.label === 'function') return props.label();
  else return props.label;
});
</script>

<template>
  <div flex="~ items-start justify-between">
    <div>{{ abLabel }}</div>

    <slot></slot>
  </div>
</template>

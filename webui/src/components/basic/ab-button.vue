<script lang="ts" setup>
import { NSpin } from 'naive-ui';

const props = withDefaults(
  defineProps<{
    type?: 'primary' | 'warn';
    size?: 'big' | 'normal' | 'small';
    link?: string | null;
    loading?: boolean;
  }>(),
  {
    type: 'primary',
    size: 'normal',
    link: null,
    loading: false,
  }
);

defineEmits(['click']);

const buttonSize = computed(() => {
  switch (props.size) {
    case 'big':
      return 'rounded-10 text-h1 w-276 h-55 text-h1';
    case 'normal':
      return 'rounded-6 w-170 h-36';
    case 'small':
      return 'rounded-6 w-86 h-28 text-main';
  }
});

const loadingSize = computed(() => {
  switch (props.size) {
    case 'big':
      return 'large';
    case 'normal':
      return 'small';
    case 'small':
      return 18;
  }
});
</script>

<template>
  <Component
    :is="link !== null ? 'a' : 'button'"
    :href="link"
    text-white
    outline-none
    f-cer
    :class="[`type-${type}`, buttonSize]"
    @click="$emit('click')"
  >
    <NSpin :show="loading" :size="loadingSize">
      <slot></slot>
    </NSpin>
  </Component>
</template>

<style lang="scss" scoped>
.type {
  &-primary {
    @include bg-mouse-event(#4e3c94, #281e52, #8e8a9c);
  }

  &-warn {
    @include bg-mouse-event(#943c61, #521e2a, #9c8a93);
  }
}
</style>

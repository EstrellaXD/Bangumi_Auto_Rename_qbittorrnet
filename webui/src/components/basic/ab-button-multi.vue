<script lang="ts" setup>
import { NSpin } from 'naive-ui';
import { Down } from '@icon-park/vue-next';

const props = withDefaults(
  defineProps<{
    type?: 'primary' | 'warn';
    size?: 'big' | 'normal' | 'small';
    link?: string | null;
    loading?: boolean;
    selections: string[];
  }>(),
  {
    type: 'primary',
    size: 'normal',
    link: null,
    loading: false,
  }
);

defineEmits(['click']);

const selected = ref<string>(props.selections[0]);
const showSelections = ref<boolean>(false);

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

const selectboxSize = computed(() => {
  switch (props.size) {
    case 'big':
      return 'w-276 rounded-10 text-h1';
    case 'normal':
      return 'w-170 rounded-6';
    case 'small':
      return 'w-86 rounded-6 text-main';
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

function onSelect(selection: string) {
  selected.value = selection;
  showSelections.value = false;
  console.log(selected.value);
}
</script>

<template>
  <div :class="buttonSize" f-cer overflow-hidden>
    <Component
      :is="link !== null ? 'a' : 'button'"
      :href="link"
      text-white
      outline-none
      wh-full
      pl-12
      :class="[`type-${type}`]"
      @click="$emit('click', selected)"
    >
      <NSpin :show="loading" :size="loadingSize">
        <div text-main>{{ selected }}</div>
      </NSpin>
    </Component>
    <div
      is-btn
      px-12
      h-full
      f-cer
      :class="[`selector-${type}`]"
      @click="() => (showSelections = !showSelections)"
    >
      <Down fill="white" />
    </div>
  </div>
  <div
    v-if="showSelections"
    abs
    z-70
    :class="selectboxSize"
    overflow-hidden
    class="select-box"
  >
    <div
      v-for="selection in selections"
      :key="selection"
      is-btn
      wh-full
      f-cer
      text-main
      py-8
      text-white
      :class="[`type-${type}`]"
      @click="onSelect(selection)"
    >
      {{ selection }}
    </div>
  </div>
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
.selector {
  &-primary {
    @include bg-mouse-event(#4e3c94, #281e52, #8e8a9c);
  }
  &-warn {
    @include bg-mouse-event(#943c61, #521e2a, #9c8a93);
  }
}

.select-box {
  transform: TranslateY(80%) TranslateX(-111%);
}
</style>

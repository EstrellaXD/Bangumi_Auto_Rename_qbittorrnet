<script lang="ts" setup>
import { Switch } from '@headlessui/vue';

const checked = defineModel<boolean>('checked', {
  default: false,
});
</script>

<template>
  <Switch v-model="checked" as="template">
    <div
      is-btn
      w-48
      h-28
      rounded-full
      rel
      flex="inline items-center"
      transition-colors
      duration-300
      p-3
      shadow="~ inset"
      class="box"
      :class="{ checked }"
    >
      <div
        wh-22
        rounded="1/2"
        transition-all
        duration-300
        class="slider"
        :class="{ checked, 'translate-x-20': checked }"
      ></div>
    </div>
  </Switch>
</template>

<style lang="scss" scope>
$bg-unchecked: #929292;
$bg-checked: #1c1259;

$slider-unchecked: #ececef;
$slider-checked: #fff;

.box {
  background: $bg-unchecked;

  &.checked {
    background: $bg-checked;
  }
}

.slider {
  &:not(.checked) {
    background: $slider-unchecked;
  }

  &.checked {
    background: $slider-checked;
  }
}
</style>

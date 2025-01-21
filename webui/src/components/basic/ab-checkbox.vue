<script lang="ts" setup>
import { Switch } from '@headlessui/vue';

withDefaults(
  defineProps<{
    small?: boolean;
  }>(),
  {
    small: false,
  }
);

const checked = defineModel<boolean>({ default: false });
</script>

<template>
  <Switch v-model="checked" as="template">
    <div flex="~ items-center gap-x-8" is-btn>
      <slot name="before"></slot>

      <div
        rel
        f-cer
        bg-white
        border="solid #3c239f"
        :class="[
          small ? 'wh-16 border-2 rounded-4' : 'wh-32 border-4 rounded-6',
          !checked && 'group',
        ]"
      >
        <div
          rounded-2
          transition="all duration-300"
          :class="[
            small ? 'wh-8' : 'wh-16',
            checked ? 'bg-[#3c239f]' : 'bg-transparent',
          ]"
          group-hover:bg="#cccad4"
          group-active:bg="#3c239f"
        ></div>
      </div>

      <slot name="after"></slot>
    </div>
  </Switch>
</template>

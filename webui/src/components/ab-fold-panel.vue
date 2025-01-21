<script lang="ts" setup>
import { Down, Up } from '@icon-park/vue-next';
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/vue';

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
  <Disclosure v-slot="{ open }">
    <div rounded-10 overflow-hidden h-max>
      <DisclosureButton
        bg-theme-row
        w-full
        text-white
        fx-cer
        px-20
        h="38 pc:45"
        justify-between
      >
        <div text="h3 pc:h2">{{ title }}</div>

        <Component :is="open ? Up : Down" size="24" />
      </DisclosureButton>

      <div
        bg-white
        py="10 pc:20"
        text="14 inherit"
        :class="[open ? 'px-20' : 'px-8']"
      >
        <div v-show="!open" line my-12></div>

        <DisclosurePanel>
          <slot></slot>
        </DisclosurePanel>
      </div>
    </div>
  </Disclosure>
</template>

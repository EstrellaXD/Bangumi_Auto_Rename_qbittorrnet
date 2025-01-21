<script lang="ts" setup>
import {
  Dialog,
  DialogPanel,
  TransitionChild,
  TransitionRoot,
} from '@headlessui/vue';

const props = withDefaults(
  defineProps<{
    title: string;
    maskClick?: boolean;
    css?: string;
  }>(),
  {
    title: 'title',
    maskClick: true,
    css: '',
  }
);

const show = defineModel('show', { default: false });

function close() {
  if (props.maskClick) {
    show.value = false;
  }
}
</script>

<template>
  <TransitionRoot appear :show="show" as="template">
    <Dialog as="div" class="relative z-10" @close="close">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div fixed inset-0 bg="black opacity-25" />
      </TransitionChild>

      <div fixed inset-0 overflow-y-auto>
        <div flex="~ items-center justify-center" min-h-full p-4 text-center>
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel>
              <ab-container :title="title" :class="[css]">
                <slot></slot>
              </ab-container>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

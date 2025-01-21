<script lang="ts" setup>
import {
  Listbox,
  ListboxButton,
  ListboxOption,
  ListboxOptions,
} from '@headlessui/vue';
import { Down, Up } from '@icon-park/vue-next';
import { isObject, isString } from 'radash';
import type { SelectItem } from '#/components';

const props = withDefaults(
  defineProps<{
    modelValue?: SelectItem | string;
    items: Array<SelectItem | string>;
  }>(),
  {}
);

const emit = defineEmits(['update:modelValue']);

const selected = ref<SelectItem | string>(
  props.modelValue || (props.items?.[0] ?? '')
);

const otherItems = computed(() => {
  return (
    props.items.filter((e) => {
      if (isString(e) && isString(selected.value)) {
        return e !== selected.value;
      } else if (isObject(e) && isObject(selected.value)) {
        return e.id !== selected.value.id;
      } else {
        return false;
      }
    }) ?? []
  );
});

const label = computed(() => {
  if (isString(selected.value)) {
    return selected.value;
  } else {
    return selected.value.label ?? selected.value.value;
  }
});

function getLabel(item: SelectItem | string) {
  if (isString(item)) {
    return item;
  } else {
    return item.label ?? item.value;
  }
}

function getDisabled(item: SelectItem | string) {
  return isString(item) ? false : item.disabled;
}

watchEffect(() => {
  emit('update:modelValue', selected.value);
});
</script>

<template>
  <Listbox v-slot="{ open }" v-model="selected">
    <div
      rel
      flex="inline col"
      rounded-6
      border="1 black"
      text-main
      p="y-4 x-12"
    >
      <ListboxButton bg-transparent fx-cer justify-between gap-x-24>
        <div>
          {{ label }}
        </div>
        <div :class="[{ hidden: open }]">
          <Down />
        </div>
      </ListboxButton>

      <ListboxOptions mt-8>
        <div flex="~ items-end justify-between gap-x-24">
          <div flex="~ col gap-y-8">
            <ListboxOption
              v-for="item in otherItems"
              v-slot="{ active }"
              :key="isString(item) ? item : item.id"
              :value="item"
              :disabled="getDisabled(item)"
            >
              <div
                :class="[
                  { 'text-primary': active },
                  getDisabled(item) ? 'is-disabled' : 'is-btn',
                ]"
              >
                {{ getLabel(item) }}
              </div>
            </ListboxOption>
          </div>

          <div :class="[{ hidden: !open }]"><Up /></div>
        </div>
      </ListboxOptions>
    </div>
  </Listbox>
</template>

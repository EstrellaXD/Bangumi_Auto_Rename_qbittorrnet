<script lang="ts" setup>
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue';
import { AddOne, International, System } from '@icon-park/vue-next';

withDefaults(
  defineProps<{
    running: boolean;
    items: {
      id: number;
      icon: any;
      label: string | (() => string);
      handle?: () => void | Promise<void>;
    }[];
  }>(),
  {
    running: false,
  }
);

defineEmits<{
  (e: 'changeLang'): void;
  (e: 'clickAdd'): void;
}>();

function abLabel(label: string | (() => string)) {
  if (typeof label === 'function') {
    return label();
  } else {
    return label;
  }
}
</script>

<template>
  <Menu>
    <div rel>
      <div fx-cer space-x="pc:16 10" text="pc:24 20">
        <International
          theme="outline"
          size="1em"
          fill="#fff"
          is-btn
          btn-click
          @click="() => $emit('changeLang')"
        />

        <AddOne
          theme="outline"
          size="1em"
          fill="#fff"
          is-btn
          btn-click
          @click="() => $emit('clickAdd')"
        />

        <MenuButton bg-transparent is-btn btn-click>
          <System theme="outline" size="1em" fill="#fff" />
        </MenuButton>

        <ab-status :running="running" />
      </div>

      <MenuItems
        abs
        top="pc:50 40"
        left="pc:32 0"
        w-120
        rounded-8
        bg-white
        overflow-hidden
        shadow
        z-99
      >
        <MenuItem v-for="i in items" :key="i.id" v-slot="{ active }">
          <div
            w-full
            h-32
            px-12
            fx-cer
            gap-x-8
            is-btn
            hover="text-white bg-primary"
            class="group"
            :class="[active ? 'text-white bg-theme-row' : 'text-black']"
            @click="() => i.handle && i.handle()"
          >
            <div
              group-hover="text-white"
              :class="[active ? 'text-white' : 'text-primary']"
            >
              <Component :is="i.icon" size="16"></Component>
            </div>
            <div text-main>{{ abLabel(i.label) }}</div>
          </div>
        </MenuItem>
      </MenuItems>
    </div>
  </Menu>
</template>

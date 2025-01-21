<script lang="ts" setup>
import { Down, Search } from '@icon-park/vue-next';
import { NSpin } from 'naive-ui';
import { watch } from 'vue';

withDefaults(
  defineProps<{
    provider: string;
    loading: boolean;
  }>(),
  {
    provider: '',
    loading: false,
  }
);

defineEmits(['select', 'search']);

const inputValue = defineModel<string>('inputValue');

watch(inputValue, (val) => {
  console.log(val);
});
</script>

<template>
  <div
    bg="#7752B4"
    text-white
    fx-cer
    rounded-12
    h-36
    pl-12
    gap-x-12
    w-400
    overflow-hidden
    shadow-inner
  >
    <Search
      v-if="!loading"
      theme="outline"
      size="24"
      fill="#fff"
      is-btn
      btn-click
      @click="$emit('search')"
    />
    <NSpin v-else :size="20" />

    <input
      v-model="inputValue"
      type="text"
      :placeholder="$t('topbar.search.placeholder')"
      input-reset
      @keyup.enter="$emit('search')"
    />
    <div
      h-full
      f-cer
      justify-between
      px-12
      w-100
      class="provider"
      is-btn
      @click="$emit('select')"
    >
      <div text-h3 truncate>
        {{ provider }}
      </div>
      <div class="provider">
        <Down />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.provider {
  background: #4e2a94;
}
</style>

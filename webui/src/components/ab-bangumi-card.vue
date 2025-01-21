<script lang="ts" setup>
import { ErrorPicture, Write } from '@icon-park/vue-next';
import type { BangumiRule } from '#/bangumi';

withDefaults(
  defineProps<{
    type?: 'primary' | 'search' | 'mobile';
    bangumi: BangumiRule;
  }>(),
  {
    type: 'primary',
  }
);

defineEmits(['click']);
</script>

<template>
  <div v-if="type === 'primary'" w-150 is-btn @click="() => $emit('click')">
    <div rounded-4 overflow-hidden poster-shandow rel>
      <div w-full h-210>
        <template v-if="bangumi.poster_link">
          <img :src="bangumi.poster_link" alt="poster" wh-full />
        </template>

        <template v-else>
          <div wh-full f-cer border="1 white">
            <ErrorPicture theme="outline" size="24" fill="#333" />
          </div>
        </template>
      </div>

      <div
        abs
        f-cer
        z-1
        inset-0
        opacity-0
        transition="all duration-300"
        hover="backdrop-blur-2 bg-white bg-opacity-30 opacity-100"
        active="duration-0 bg-opacity-60"
        class="group"
      >
        <div
          text-white
          rounded="1/2"
          wh-44
          f-cer
          bg-theme-row
          group-active="poster-pen-active"
        >
          <Write size="20" />
        </div>
      </div>
    </div>

    <div py-4>
      <div text-h3 truncate>{{ bangumi.official_title }}</div>

      <div space-x-5>
        <ab-tag :title="`Season ${bangumi.season}`" type="primary" />
        <ab-tag
          v-if="bangumi.group_name"
          :title="bangumi.group_name"
          type="primary"
        />
      </div>
    </div>
  </div>
  <div
    v-else-if="type === 'search'"
    w-480
    rounded-12
    p-4
    shadow
    bg="#eee5f4"
    transition="opacity ease-in-out duration-300"
  >
    <div bg-white rounded-8 p-12 fx-cer justify-between gap-x-16>
      <div w-400 gap-x-16 fx-cer>
        <div h-44 w-72 rounded-6 overflow-hidden>
          <template v-if="bangumi.poster_link">
            <img
              :src="bangumi.poster_link"
              alt="poster"
              w-full
              translate-y="-25%"
            />
          </template>

          <template v-else>
            <div wh-full f-cer border="1 white">
              <ErrorPicture theme="outline" size="24" fill="#333" />
            </div>
          </template>
        </div>
        <div flex="~ col gap-y-4">
          <div w-300 text="h3 primary" truncate>
            {{ bangumi.official_title }}
          </div>
          <div flex="~ gap-x-8">
            <template
              v-for="i in ['season', 'group_name', 'subtitle']"
              :key="i"
            >
              <ab-tag
                v-if="bangumi[i]"
                :title="i === 'season' ? `Season ${bangumi[i]}` : bangumi[i]"
                type="primary"
              />
            </template>
          </div>
        </div>
      </div>
      <ab-add :round="true" type="medium" @click="() => $emit('click')" />
    </div>
  </div>
</template>

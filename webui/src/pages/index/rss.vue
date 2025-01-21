<script lang="tsx" setup>
import { NDataTable } from 'naive-ui';
import type { RSS } from '#/rss';

definePage({
  name: 'RSS',
});

const { t } = useMyI18n();
const { rss, selectedRSS } = storeToRefs(useRSSStore());
const { getAll, deleteSelected, disableSelected, enableSelected } =
  useRSSStore();

onActivated(() => {
  getAll();
});

const RSSTableOptions = computed(() => {
  const columns = [
    {
      type: 'selection',
    },
    {
      title: t('rss.name'),
      key: 'name',
      className: 'text-h3',
      ellipsis: {
        tooltip: true,
      },
    },
    {
      title: t('rss.url'),
      key: 'url',
      className: 'text-h3',
      minWidth: 400,
      align: 'center',
      ellipsis: {
        tooltip: true,
      },
    },
    {
      title: t('rss.status'),
      key: 'status',
      className: 'text-h3',
      align: 'right',
      minWidth: 200,
      render(rss: RSS) {
        return (
          <div flex="~ justify-end gap-x-8">
            {rss.parser && <ab-tag type="primary" title={rss.parser} />}
            {rss.aggregate && <ab-tag type="primary" title="aggregate" />}
            {rss.enabled ? (
              <ab-tag type="active" title="active" />
            ) : (
              <ab-tag type="inactive" title="inactive" />
            )}
          </div>
        );
      },
    },
  ];

  const rowKey = (rss: RSS) => rss.id;

  return {
    columns,
    data: rss.value,
    pagination: false,
    bordered: false,
    rowKey,
    maxHeight: 500,
  } as unknown as InstanceType<typeof NDataTable>;
});
</script>

<template>
  <div overflow-auto mt-12 flex-grow>
    <ab-container :title="$t('rss.title')">
      <NDataTable
        v-bind="RSSTableOptions"
        @update:checked-row-keys="(e) => (selectedRSS = (e as number[]))"
      ></NDataTable>

      <div v-if="selectedRSS.length > 0">
        <div line my-12></div>
        <div flex="~ justify-end gap-x-10">
          <ab-button @click="enableSelected">{{ $t('rss.enable') }}</ab-button>
          <ab-button @click="disableSelected">{{
            $t('rss.disable')
          }}</ab-button>
          <ab-button class="type-warn" @click="deleteSelected">{{
            $t('rss.delete')
          }}</ab-button>
        </div>
      </div>
    </ab-container>
  </div>
</template>

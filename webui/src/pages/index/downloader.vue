<script lang="ts" setup>
definePage({
  name: 'Downloader',
});

const { config } = storeToRefs(useConfigStore());
const { getConfig } = useConfigStore();

const isNull = computed(() => {
  return config.value.downloader.host === '';
});

const url = computed(() => {
  const downloader = config.value.downloader;
  const host = downloader.host.replace(/http(s?)\:\/\//, '');
  const protocol = downloader.ssl ? 'https' : 'http';

  return `${protocol}://${host}`;
});

onActivated(() => {
  getConfig();
});
</script>

<template>
  <div overflow-auto mt-12 flex-grow>
    <template v-if="isNull">
      <div wh-full f-cer text-h1 text-primary>
        <RouterLink to="/config" hover:underline>{{
          $t('downloader.hit')
        }}</RouterLink>
      </div>
    </template>

    <iframe
      :src="url"
      frameborder="0"
      allowfullscreen="true"
      wh-full
      flex-1
      rounded-12
    ></iframe>
  </div>
</template>

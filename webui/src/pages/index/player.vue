<script lang="ts" setup>
definePage({
  name: 'Player',
});

const { url } = storeToRefs(usePlayerStore());
</script>

<template>
  <div overflow-auto mt-12 flex-grow>
    <template v-if="url === ''">
      <div wh-full f-cer text-h1 text-primary>
        <RouterLink to="/config" hover:underline>{{
          $t('player.hit')
        }}</RouterLink>
      </div>
    </template>
    <iframe
      v-else
      :src="url"
      frameborder="0"
      allowfullscreen="true"
      wh-full
      flex-1
      rounded-12
    ></iframe>
  </div>
</template>

<script lang="ts" setup>
withDefaults(
  defineProps<{
    running: boolean;
    size?: string;
  }>(),
  {
    running: false,
    size: '1em',
  }
);
</script>

<template>
  <div f-cer :style="{ width: size, height: size }">
    <div rounded="1/2" f-cer border="2 solid white" wh-full>
      <div
        :class="[running ? 'bg-running' : 'bg-stopped']"
        rounded="1/2"
        wh-10
        transition-colors
      ></div>
    </div>
  </div>
</template>

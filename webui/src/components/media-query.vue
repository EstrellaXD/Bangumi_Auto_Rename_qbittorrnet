<script lang="ts" setup>
const { isMobile } = useBreakpointQuery();
</script>

<template>
  <template v-if="isMobile">
    <slot name="mobile"></slot>
  </template>

  <template v-else>
    <slot></slot>
  </template>
</template>

<style lang="scss" scope></style>

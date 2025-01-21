<script setup lang="ts">
import { type GlobalThemeOverrides, NConfigProvider } from 'naive-ui';

const theme: GlobalThemeOverrides = {
  Spin: {
    color: '#fff',
  },
  DataTable: {
    thColor: 'rgba(255, 255, 255, 0)',
    thColorHover: 'rgba(255, 255, 255, 0)',
    tdColorHover: 'rgba(255, 255, 255, 0)',
  },
  Checkbox: {
    colorChecked: '#4e3c94',
    borderFocus: '#4e3c94',
    boxShadowFocus: '0 0 0 2px rgba(78, 60, 148, 0.2)',
    borderChecked: '1px solid #4e3c94',
  },
};

const { refresh, isLoggedIn } = useAuth();

if (isLoggedIn.value) {
  refresh();
}
</script>

<template>
  <Suspense>
    <NConfigProvider :theme-overrides="theme">
      <RouterView></RouterView>
    </NConfigProvider>
  </Suspense>
</template>

<style lang="scss">
@import './style/transition';
@import './style/var';
@import './style/global';
</style>

<script lang="ts" setup>
definePage({
  name: 'Index',
  redirect: '/bangumi',
});
</script>

<template>
  <div class="layout-container">
    <ab-topbar />

    <main class="layout-main">
      <ab-sidebar />

      <div class="layout-content">
        <ab-page-title :title="$route.name"></ab-page-title>

        <RouterView v-slot="{ Component }">
          <KeepAlive>
            <component :is="Component" />
          </KeepAlive>
        </RouterView>
      </div>
    </main>
  </div>
</template>

<style lang="scss" scoped>
.layout-container {
  width: 100%;
  height: 100%;

  padding: var(--layout-padding);
  gap: var(--layout-gap);

  display: flex;
  flex-direction: column;

  background: #f0f0f0;

  @include forPC {
    min-width: 1024px;
    min-height: 768px;
  }

  @include forMobile {
    overflow: hidden;
    height: 100vh;
  }
}

.layout-main {
  display: flex;
  gap: 20px;

  overflow: hidden;
  height: calc(100vh - 2 * var(--layout-padding) - 60px - var(--layout-gap));

  @include forMobile {
    flex-direction: column-reverse;
    height: calc(100vh - var(--layout-padding) * 2 - var(--layout-gap));
    gap: var(--layout-gap);
  }
}

.layout-content {
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
  flex: 1;
}
</style>

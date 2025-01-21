<script lang="ts" setup>
const props = withDefaults(
  defineProps<{
    type: 'primary' | 'warn' | 'inactive' | 'active' | 'notify';
    title: string;
  }>(),
  {
    type: 'primary',
    title: 'title',
  }
);

const InnerStyle = computed(() => {
  return `${props.type}-inner`;
});
</script>

<template>
  <div p-1 rounded-16 inline-flex :class="type">
    <div bg-white rounded-12 px-8 text-10 truncate max-w-72 :class="InnerStyle">
      {{ title }}
    </div>
  </div>
</template>

<style lang="scss" scoped>
$primary-map: (
  border: linear-gradient(90.5deg, #492897 1.53%, #783674 96.48%),
  inner: #eee5f4,
  font: #000000,
);

$warn-map: (
  border: #892f2f,
  inner: #ffdfdf,
  font: #892f2f,
);

$inactive-map: (
  border: #797979,
  inner: #e0e0e0,
  font: #3f3f3f,
);

$active-map: (
  border: #104931,
  inner: #e5f4e0,
  font: #4c6643,
);

$notify-map: (
  border: #f5c451,
  inner: #fff4db,
  font: #a76e18,
);

$types-map: (
  primary: $primary-map,
  warn: $warn-map,
  inactive: $inactive-map,
  active: $active-map,
  notify: $notify-map,
);

@each $type, $colors in $types-map {
  .#{$type} {
    background: map-get($colors, border);

    &-inner {
      background: map-get($colors, inner);
      color: map-get($colors, font);
    }
  }
}
</style>

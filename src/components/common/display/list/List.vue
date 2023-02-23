<template>
  <q-list :bordered="props.bordered">
    <template v-for="(item, index) in props.items || []" :key="index">
      <slot name="item" :item="item" :index="index" />
    </template>
    <slot />
  </q-list>
</template>

<script lang="ts">
/**
 * A generic list component.
 */
export default {
  name: "List",
};
</script>

<script setup lang="ts">
const props = defineProps<{
  items?: unknown[];
  bordered?: boolean;
}>();
</script>

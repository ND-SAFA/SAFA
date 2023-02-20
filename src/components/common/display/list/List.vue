<template>
  <q-list>
    <template v-for="(item, index) in props.items" :key="index">
      <slot name="item" :item="item" :index="index" />
    </template>
  </q-list>
</template>

<script lang="ts">
/**
 * A generic list component
 */
export default {
  name: "List",
};
</script>

<script setup lang="ts">
const props = defineProps<{
  items: Record<string, unknown>[];
}>();
</script>

<template>
  <q-list :bordered="props.bordered">
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
  bordered?: boolean;
}>();
</script>

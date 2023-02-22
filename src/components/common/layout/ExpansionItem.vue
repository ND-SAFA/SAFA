<template>
  <q-expansion-item :label="props.label">
    <q-card class="q-my-md">
      <slot />
    </q-card>
  </q-expansion-item>
</template>

<script lang="ts">
/**
 * A generic expansion item.
 */
export default {
  name: "ExpansionItem",
};
</script>

<script setup lang="ts">
const props = defineProps<{
  label: string;
}>();
</script>

<template>
  <div class="mb-4">
    <v-card variant="outlined" :class="className">
      <slot />
    </v-card>
  </div>
</template>

<script lang="ts">
/**
 * Displays a card that contains panel content.
 */
export default {
  name: "PanelCard",
};
</script>

<script setup lang="ts">
import { computed, withDefaults, defineProps } from "vue";

const props = withDefaults(
  defineProps<{
    color?: "primary" | "error" | "none";
  }>(),
  {
    color: "primary",
  }
);

const className = computed(
  () => `pa-4 overflow-hidden bg-neutral ${props.color}-border`
);
</script>

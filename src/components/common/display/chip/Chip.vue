<template>
  <q-chip
    :class="props.class"
    :outline="props.outlined"
    :color="props.color"
    :data-cy="props.dataCy"
    :style="props.style"
    :clickable="props.clickable"
    :removable="removable"
    @click="emit('click')"
    @remove="emit('remove')"
  >
    <typography v-if="!!props.label" :value="props.label" />
    <slot />
  </q-chip>
</template>

<script lang="ts">
/**
 * Displays a generic chip.
 */
export default {
  name: "Chip",
};
</script>

<script setup lang="ts">
import { ChipProps } from "@/types";
import { Typography } from "../content";

const props = defineProps<ChipProps>();

const emit = defineEmits<{
  /**
   * When the chip is clicked.
   * Only emitted with `props.clickable`.
   */
  (e: "click"): void;
  /**
   * When the remove button is clicked.
   * Only emitted with `props.removable`.
   */
  (e: "remove"): void;
}>();
</script>

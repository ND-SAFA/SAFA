<template>
  <q-chip
    :class="props.class"
    :outline="props.outline"
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
import { ThemeColor } from "@/types";
import { Typography } from "../content";

const props = defineProps<{
  /**
   * A chip label to display.
   */
  label?: string;
  /**
   * The class names for the chip.
   */
  class?: string;
  /**
   * The css style of the chip.
   */
  style?: string;
  /**
   * Whether the chip is outlined.
   */
  outline?: boolean;
  /**
   * Whether the chip is clickable.
   */
  clickable?: boolean;
  /**
   * Whether the chip is removable. Displays a remove icon button.
   */
  removable?: boolean;
  /**
   * The color of the chip
   */
  color?: ThemeColor;
  /**
   * A testing selector to set on the chip.
   */
  dataCy?: string;
}>();

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

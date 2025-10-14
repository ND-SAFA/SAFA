<template>
  <q-chip
    :class="props.class"
    :outline="props.outlined"
    :color="chipColor"
    :data-cy="props.dataCy"
    :style="chipStyle"
    :clickable="props.clickable"
    :removable="removable"
    :dense="props.dense"
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
import { computed } from "vue";
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

const chipColor = computed(() => {
  if (props.color?.includes("#")) {
    return "";
  } else if (props.color) {
    return props.color;
  } else {
    return "";
  }
});

const chipStyle = computed(() => {
  if (props.style) {
    return props.style;
  } else if (props.color?.includes("#")) {
    return `color: ${props.color}; border-color: ${props.color} !important`;
  } else {
    return "";
  }
});
</script>

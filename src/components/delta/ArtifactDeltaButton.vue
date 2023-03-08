<template>
  <text-button
    outlined
    block
    :color="color"
    class="q-mb-sm"
    @click="emit('click')"
  >
    <typography
      ellipsis
      :value="name"
      :color="color"
      style="max-width: 300px"
    />
  </text-button>
</template>

<script lang="ts">
/**
 * Displays an artifact delta button.
 */
export default {
  name: "ArtifactDeltaButton",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { DeltaType, ThemeColor } from "@/types";
import { TextButton, Typography } from "@/components/common";

const props = defineProps<{
  /**
   * The changed entity name.
   */
  name: string;
  /**
   * The type of change delta for this entity.
   */
  deltaType: DeltaType;
}>();

const emit = defineEmits<{
  (e: "click"): void;
}>();

const color = computed<ThemeColor>(() => {
  switch (props.deltaType) {
    case "added":
      return "positive";
    case "modified":
      return "primary";
    case "removed":
      return "negative";
    default:
      return "black";
  }
});
</script>

<template>
  <list-item clickable :title="props.name" @click="emit('click')" />
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
import { DeltaType } from "@/types";
import { ListItem } from "@/components/common";

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
</script>

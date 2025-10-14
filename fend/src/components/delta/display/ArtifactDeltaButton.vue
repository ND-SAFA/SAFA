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
import { ArtifactDeltaButtonProps } from "@/types";
import { ListItem } from "@/components/common";

const props = defineProps<ArtifactDeltaButtonProps>();

const emit = defineEmits<{
  (e: "click"): void;
}>();
</script>

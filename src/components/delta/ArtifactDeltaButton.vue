<template>
  <list-item
    clickable
    :class="className"
    :title="props.name"
    @click="emit('click')"
  />
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
import { DeltaType } from "@/types";
import { useTheme } from "@/hooks";
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

const { darkMode } = useTheme();

const className = computed(() =>
  darkMode.value ? "" : ` bg-${props.deltaType}`
);
</script>

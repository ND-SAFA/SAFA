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
import { getEnumColor } from "@/util";
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

const className = computed(() => `bg-${getEnumColor(props.deltaType)}`);
</script>

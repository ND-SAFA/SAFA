<template>
  <div v-if="isOpen">
    <slot />
  </div>
</template>

<script lang="ts">
/**
 * Controls the open state of a details right side panel.
 */
export default {
  name: "DetailsPanel",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { DetailsOpenState } from "@/types";
import { appStore } from "@/hooks";

const props = defineProps<{
  /**
   * The panel being controlled.
   */
  panel: DetailsOpenState;
}>();

const isOpen = computed(() => appStore.isDetailsPanelOpen === props.panel);
</script>

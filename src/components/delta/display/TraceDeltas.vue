<template>
  <panel-card v-if="inDeltaView" title="Trace Links" collapsable borderless>
    <delta-button-group
      is-traces
      delta-type="added"
      :items="addedTraces"
      @click="handleAddedSelect"
    />
    <delta-button-group
      is-traces
      delta-type="removed"
      :items="removedTraces"
      @click="handleRemovedSelect"
    />
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays trace delta information.
 */
export default {
  name: "TraceDeltas",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { deltaStore, selectionStore } from "@/hooks";
import { PanelCard } from "@/components/common";
import DeltaButtonGroup from "./DeltaButtonGroup.vue";

const inDeltaView = computed(() => deltaStore.inDeltaView);
const addedTraces = computed(() => deltaStore.addedTraces);
const removedTraces = computed(() => deltaStore.removedTraces);

/**
 * Selects an added trace.
 * @param id - The trace to select.
 */
function handleAddedSelect(id: string): void {
  selectionStore.selectTraceLink(addedTraces.value[id]);
}

/**
 * Selects a removed trace.
 * @param id - The trace to select.
 */
function handleRemovedSelect(id: string): void {
  selectionStore.selectTraceLink(removedTraces.value[id]);
}
</script>

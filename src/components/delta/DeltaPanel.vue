<template>
  <details-panel panel="delta">
    <delta-panel-nav />
    <artifact-deltas />
    <trace-deltas />
  </details-panel>
</template>

<script lang="ts">
/**
 * Displays project version delta information.
 */
export default {
  name: "DeltaPanel",
};
</script>

<script setup lang="ts">
import DetailsPanel from "@/components/navigation/detailsDrawer/DetailsPanel.vue";
import DeltaPanelNav from "./DeltaPanelNav.vue";
import ArtifactDeltas from "./ArtifactDeltas.vue";
import TraceDeltas from "./TraceDeltas.vue";
</script>

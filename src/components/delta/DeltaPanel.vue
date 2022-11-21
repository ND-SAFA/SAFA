<template>
  <div v-if="isOpen">
    <delta-panel-nav />
    <artifact-deltas />
    <trace-deltas />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore } from "@/hooks";
import DeltaPanelNav from "./DeltaPanelNav.vue";
import ArtifactDeltas from "./ArtifactDeltas.vue";
import TraceDeltas from "./TraceDeltas.vue";

/**
 * Displays project version delta information.
 */
export default Vue.extend({
  name: "DeltaPanel",
  components: { DeltaPanelNav, ArtifactDeltas, TraceDeltas },
  computed: {
    /**
     * @return Whether this panel is open.
     */
    isOpen(): boolean {
      return appStore.isDetailsPanelOpen === "delta";
    },
  },
});
</script>

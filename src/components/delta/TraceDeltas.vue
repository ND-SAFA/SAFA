<template>
  <v-container v-if="isDeltaMode">
    <typography el="h2" variant="subtitle" value="Trace Links" />
    <v-divider />

    <v-list expand>
      <delta-button-group
        is-traces
        deltaType="added"
        :items="addedTraces"
        @click="handleAddedSelect"
      />
      <delta-button-group
        is-traces
        deltaType="removed"
        :items="removedTraces"
        @click="handleRemovedSelect"
      />
    </v-list>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { deltaStore, selectionStore } from "@/hooks";
import { Typography } from "@/components/common";
import DeltaButtonGroup from "./DeltaButtonGroup.vue";

/**
 * Displays trace delta information.
 *
 * @emits `open` - On open.
 */
export default Vue.extend({
  name: "TraceDeltas",
  components: { DeltaButtonGroup, Typography },
  data() {
    return {
      openPanels: [0, 1],
    };
  },
  computed: {
    /**
     * @return All added traces.
     */
    addedTraces() {
      return deltaStore.addedTraces;
    },
    /**
     * @return All removed traces.
     */
    removedTraces() {
      return deltaStore.removedTraces;
    },
    /**
     * @return Whether the app is in delta view.
     */
    isDeltaMode(): boolean {
      return deltaStore.inDeltaView;
    },
  },
  methods: {
    /**
     * Selects an added trace.
     * @param id - The trace to select.
     */
    handleAddedSelect(id: string): void {
      selectionStore.selectTraceLink(this.addedTraces[id]);
    },
    /**
     * Selects a removed trace.
     * @param id - The trace to select.
     */
    handleRemovedSelect(id: string): void {
      selectionStore.selectTraceLink(this.removedTraces[id]);
    },
  },
  watch: {
    /**
     * When the delta traces change, set all panels to open.
     */
    isDeltaMode() {
      const panels: number[] = [];

      if (Object.keys(this.addedTraces).length > 0) panels.push(0);
      if (Object.keys(this.removedTraces).length > 0) panels.push(1);

      this.openPanels = panels;
      this.$emit("open");
    },
  },
});
</script>

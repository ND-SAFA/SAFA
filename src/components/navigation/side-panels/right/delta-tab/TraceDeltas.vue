<template>
  <v-container v-if="isDeltaMode">
    <typography el="h2" variant="subtitle" value="Trace Links" />
    <v-divider class="mb-2" />

    <v-expansion-panels class="ma-0 pa-0" multiple v-model="openPanels">
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
    </v-expansion-panels>

    <trace-link-approval-modal
      :is-open="isTraceModalOpen"
      :link="selectedDeltaLink"
      @close="isTraceModalOpen = false"
    />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { TraceLink } from "@/types";
import { deltaModule } from "@/store";
import { Typography } from "@/components/common";
import { TraceLinkApprovalModal } from "@/components/trace-link";
import DeltaButtonGroup from "./DeltaButtonGroup.vue";

/**
 * Displays trace delta information.
 *
 * @emits `open` - On open.
 */
export default Vue.extend({
  name: "TraceDeltas",
  components: { DeltaButtonGroup, TraceLinkApprovalModal, Typography },
  data() {
    return {
      isTraceModalOpen: false,
      selectedDeltaLink: undefined as TraceLink | undefined,
      openPanels: [0, 1],
    };
  },
  computed: {
    /**
     * @return All added traces.
     */
    addedTraces() {
      return deltaModule.addedTraces;
    },
    /**
     * @return All removed traces.
     */
    removedTraces() {
      return deltaModule.removedTraces;
    },
    /**
     * @return Whether the app is in delta view.
     */
    isDeltaMode(): boolean {
      return deltaModule.inDeltaView;
    },
  },
  methods: {
    /**
     * Selects an added trace.
     * @param id - The trace to select.
     */
    handleAddedSelect(id: string): void {
      this.selectedDeltaLink = this.addedTraces[id];
      this.isTraceModalOpen = true;
    },
    /**
     * Selects a removed trace.
     * @param id - The trace to select.
     */
    handleRemovedSelect(id: string): void {
      this.selectedDeltaLink = this.removedTraces[id];
      this.isTraceModalOpen = true;
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

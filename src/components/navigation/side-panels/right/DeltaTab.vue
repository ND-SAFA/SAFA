<template>
  <v-expansion-panels class="ma-0 pa-0" multiple v-model="openPanels">
    <delta-panel-nav />
    <delta-button-group
      v-if="isDeltaMode"
      deltaType="added"
      class="mt-10"
      :artifacts="addedArtifacts"
      @click="handleAddedSelect"
    />
    <delta-button-group
      v-if="isDeltaMode"
      deltaType="removed"
      :artifacts="removedArtifacts"
      @click="handleRemovedSelect"
    />
    <delta-button-group
      v-if="isDeltaMode"
      deltaType="modified"
      :artifacts="modifiedArtifacts"
      @click="handleModifiedSelect"
    />
    <artifact-delta-diff
      v-if="selectedDeltaArtifact !== undefined"
      :isOpen="selectedDeltaArtifact !== undefined"
      :name="selectedDeltaArtifact.name"
      :input-artifact="selectedDeltaArtifact.artifact"
      :delta-type="selectedDeltaArtifact.deltaType"
      @close="handleCloseModal"
    />
  </v-expansion-panels>
</template>

<script lang="ts">
import Vue from "vue";
import { DeltaType, DeltaArtifact, ChangedArtifact } from "@/types";
import { deltaModule } from "@/store";
import {
  DeltaPanelNav,
  DeltaButtonGroup,
  ArtifactDeltaDiff,
} from "./delta-tab";

/**
 * Displays delta information.
 *
 * @emits `open` - On open.
 */
export default Vue.extend({
  name: "DeltaTab",
  components: { ArtifactDeltaDiff, DeltaButtonGroup, DeltaPanelNav },
  data() {
    return {
      selectedDeltaArtifact: undefined as ChangedArtifact | undefined,
      openPanels: [0, 1, 2],
    };
  },
  computed: {
    /**
     * @return All added artifacts.
     */
    addedArtifacts() {
      return deltaModule.addedArtifacts;
    },
    /**
     * @return All removed artifacts.
     */
    removedArtifacts() {
      return deltaModule.removedArtifacts;
    },
    /**
     * @return All modified artifacts.
     */
    modifiedArtifacts() {
      return deltaModule.modifiedArtifacts;
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
     * Selects an artifact..
     */
    handleArtifactSelect(
      name: string,
      artifact: DeltaArtifact,
      deltaType: DeltaType
    ): void {
      this.selectedDeltaArtifact = { name, artifact, deltaType };
    },
    /**
     * Selects an added artifact.
     * @param id - The artifact to select.
     */
    handleAddedSelect(id: string): void {
      this.handleArtifactSelect(
        this.addedArtifacts[id].name,
        this.addedArtifacts[id],
        "added"
      );
    },
    /**
     * Selects a modified artifact.
     * @param id - The artifact to select.
     */
    handleModifiedSelect(id: string): void {
      this.handleArtifactSelect(
        this.modifiedArtifacts[id].after.name,
        this.modifiedArtifacts[id],
        "modified"
      );
    },
    /**
     * Selects a removed artifact.
     * @param id - The artifact to select.
     */
    handleRemovedSelect(id: string): void {
      this.handleArtifactSelect(
        this.removedArtifacts[id].name,
        this.removedArtifacts[id],
        "removed"
      );
    },
    /**
     * Closes the delta modal.
     */
    handleCloseModal(): void {
      this.selectedDeltaArtifact = undefined;
    },
  },
  watch: {
    /**
     * When the delta artifacts change, set all panels to open.
     */
    deltaArtifacts() {
      this.$emit("open");
      this.openPanels = [0, 1, 2];
    },
  },
});
</script>

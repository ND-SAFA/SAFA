<template>
  <v-container v-if="isDeltaMode">
    <typography el="h2" variant="subtitle" value="Artifacts" />
    <v-divider />

    <v-list expand>
      <delta-button-group
        delta-type="added"
        :items="addedArtifacts"
        @click="handleAddedSelect"
      />
      <delta-button-group
        delta-type="removed"
        :items="removedArtifacts"
        @click="handleRemovedSelect"
      />
      <delta-button-group
        delta-type="modified"
        :items="modifiedArtifacts"
        @click="handleModifiedSelect"
      />
    </v-list>

    <artifact-delta-diff
      v-if="selectedDeltaArtifact !== undefined"
      :isOpen="selectedDeltaArtifact !== undefined"
      :name="selectedDeltaArtifact.name"
      :input-artifact="selectedDeltaArtifact.artifact"
      :delta-type="selectedDeltaArtifact.deltaType"
      @close="handleCloseModal"
    />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { DeltaType, DeltaArtifact, ChangedArtifact } from "@/types";
import { deltaStore } from "@/hooks";
import { Typography } from "@/components/common";
import ArtifactDeltaDiff from "./ArtifactDeltaDiff.vue";
import DeltaButtonGroup from "./DeltaButtonGroup.vue";

/**
 * Displays artifact delta information.
 *
 * @emits `open` - On open.
 */
export default Vue.extend({
  name: "ArtifactDeltas",
  components: { ArtifactDeltaDiff, DeltaButtonGroup, Typography },
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
      return deltaStore.addedArtifacts;
    },
    /**
     * @return All removed artifacts.
     */
    removedArtifacts() {
      return deltaStore.removedArtifacts;
    },
    /**
     * @return All modified artifacts.
     */
    modifiedArtifacts() {
      return deltaStore.modifiedArtifacts;
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
    isDeltaMode() {
      const panels: number[] = [];

      if (Object.keys(this.addedArtifacts).length > 0) panels.push(0);
      if (Object.keys(this.removedArtifacts).length > 0) panels.push(1);
      if (Object.keys(this.modifiedArtifacts).length > 0) panels.push(2);

      this.openPanels = panels;
      this.$emit("open");
    },
  },
});
</script>

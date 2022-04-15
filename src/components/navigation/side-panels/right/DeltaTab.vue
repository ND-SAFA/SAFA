<template>
  <v-expansion-panels class="ma-0 pa-0" multiple v-model="openPanels">
    <delta-panel-nav />
    <delta-button-group
      v-if="isDeltaMode"
      deltaType="added"
      class="mt-10"
      :names="addedArtifactNames"
      :ids="addedArtifactIds"
      @click="
        (id) =>
          handleArtifactSelect(
            addedArtifacts[id].name,
            addedArtifacts[id],
            'added'
          )
      "
    />
    <delta-button-group
      v-if="isDeltaMode"
      deltaType="removed"
      :names="removedArtifactNames"
      :ids="removedArtifactIds"
      @click="
        (id) =>
          handleArtifactSelect(
            removedArtifacts[id].name,
            removedArtifacts[id],
            'removed'
          )
      "
    />
    <delta-button-group
      v-if="isDeltaMode"
      deltaType="modified"
      :names="modifiedArtifactNames"
      :ids="modifiedArtifactIds"
      @click="
        (id) =>
          handleArtifactSelect(
            modifiedArtifacts[id].after.name,
            modifiedArtifacts[id],
            'modified'
          )
      "
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
import { artifactModule, deltaModule } from "@/store";
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
      openPanels: [] as number[],
    };
  },
  computed: {
    /**
     * @return All visible artifacts.
     */
    artifacts() {
      return artifactModule.artifacts;
    },
    /**
     * @return All added artifacts.
     */
    addedArtifacts() {
      return deltaModule.addedArtifacts;
    },
    /**
     * @return All added artifact names.
     */
    addedArtifactNames(): string[] {
      return Object.values(this.addedArtifacts).map((a) => a.name);
    },
    /**
     * @return All added artifact ids.
     */
    addedArtifactIds(): string[] {
      return Object.values(this.addedArtifacts).map((a) => a.id);
    },
    /**
     * @return All removed artifacts.
     */
    removedArtifacts() {
      return deltaModule.removedArtifacts;
    },
    /**
     * @return All removed artifact names.
     */
    removedArtifactNames(): string[] {
      return Object.values(this.removedArtifacts).map((a) => a.name);
    },
    /**
     * @return All removed artifact ids.
     */
    removedArtifactIds(): string[] {
      return Object.values(this.removedArtifacts).map((a) => a.id);
    },
    /**
     * @return All modified artifacts.
     */
    modifiedArtifacts() {
      return deltaModule.modifiedArtifacts;
    },
    /**
     * @return All modified artifact names.
     */
    modifiedArtifactNames(): string[] {
      return Object.values(this.modifiedArtifacts).map((a) => a.after.name);
    },
    /**
     * @return All modified artifact ids.
     */
    modifiedArtifactIds(): string[] {
      return Object.values(this.modifiedArtifacts).map((a) => a.after.id);
    },
    /**
     * @return All changed artifact names.
     */
    deltaArtifacts(): string[] {
      return [
        ...this.addedArtifactNames,
        ...this.removedArtifactNames,
        ...this.modifiedArtifactNames,
      ];
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
     * Selects an artifact delta.
     */
    handleArtifactSelect(
      name: string,
      artifact: DeltaArtifact,
      deltaType: DeltaType
    ): void {
      this.selectedDeltaArtifact = { name, artifact, deltaType };
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

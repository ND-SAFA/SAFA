<template>
  <v-expansion-panels class="ma-0 pa-0" multiple v-model="openPanels">
    <delta-panel-nav />
    <delta-button-group
      v-if="isDeltaMode"
      deltaType="added"
      class="mt-10"
      :names="addedArtifactNames"
      @click="(name) => selectArtifact(name, addedArtifactNames[name], 'added')"
    />
    <delta-button-group
      v-if="isDeltaMode"
      deltaType="removed"
      :names="removedArtifactNames"
      @click="
        (name) => selectArtifact(name, removedArtifactNames[name], 'removed')
      "
    />
    <delta-button-group
      v-if="isDeltaMode"
      deltaType="modified"
      :names="artifactsModified"
      @click="
        (name) => selectArtifact(name, artifactsModified[name], 'modified')
      "
    />
    <artifact-delta-diff
      v-if="selectedDeltaArtifact !== undefined"
      :isOpen="selectedDeltaArtifact !== undefined"
      :delta-type="selectedDeltaArtifact[2]"
      :input-artifact="selectedDeltaArtifact[1]"
      :name="selectedDeltaArtifact[0]"
      @close="closeDeltaModal"
    />
  </v-expansion-panels>
</template>

<script lang="ts">
import { Artifact, EntityModification, DeltaType } from "@/types";
import Vue from "vue";
import { deltaModule, projectModule } from "@/store";
import {
  DeltaPanelNav,
  DeltaButtonGroup,
  ArtifactDeltaDiff,
} from "./delta-tab";

type DeltaArtifact = Artifact | EntityModification<Artifact>;
type OptionalDeltaArtifact = [string, DeltaArtifact, string] | undefined;

/**
 * Displays delta information.
 *
 * @emits `open` - On open.
 */
export default Vue.extend({
  components: { ArtifactDeltaDiff, DeltaButtonGroup, DeltaPanelNav },
  data() {
    return {
      selectedDeltaArtifact: undefined as OptionalDeltaArtifact,
      openPanels: [] as number[],
    };
  },
  methods: {
    selectArtifact(
      name: string,
      artifact: DeltaArtifact,
      deltaType: DeltaType
    ): void {
      this.selectedDeltaArtifact = [name, artifact, deltaType];
    },
    closeDeltaModal(): void {
      this.selectedDeltaArtifact = undefined;
    },
  },
  computed: {
    artifacts(): Artifact[] {
      return projectModule.getArtifacts;
    },
    artifactHashmap(): Record<string, Artifact> {
      return projectModule.getArtifactHashmap;
    },
    addedArtifactNames(): string[] {
      return Object.keys(deltaModule.addedArtifacts);
    },
    removedArtifactNames(): string[] {
      return Object.keys(deltaModule.removedArtifacts);
    },
    modifiedArtifactNames(): string[] {
      return Object.keys(deltaModule.modifiedArtifacts);
    },
    deltaArtifacts(): string[] {
      return this.addedArtifactNames.concat(
        this.removedArtifactNames.concat(this.modifiedArtifactNames)
      );
    },
    isDeltaMode(): boolean {
      return deltaModule.getIsDeltaViewEnabled;
    },
  },
  watch: {
    deltaArtifacts() {
      this.$emit("open");
      this.openPanels = [0, 1, 2];
    },
  },
});
</script>

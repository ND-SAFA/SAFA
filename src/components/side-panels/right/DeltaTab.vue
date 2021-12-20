<template>
  <v-expansion-panels class="ma-0 pa-0" multiple v-model="openPanels">
    <delta-panel-nav />
    <delta-button-group
      v-if="isDeltaMode"
      deltaType="added"
      class="mt-10"
      :names="addedArtifactNames"
      @click="(name) => selectArtifact(name, addedArtifacts[name], 'added')"
    />
    <delta-button-group
      v-if="isDeltaMode"
      deltaType="removed"
      :names="removedArtifactNames"
      @click="(name) => selectArtifact(name, removedArtifacts[name], 'removed')"
    />
    <delta-button-group
      v-if="isDeltaMode"
      deltaType="modified"
      :names="modifiedArtifactNames"
      @click="
        (name) => selectArtifact(name, modifiedArtifacts[name], 'modified')
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
      return projectModule.artifacts;
    },
    artifactHashmap(): Record<string, Artifact> {
      return projectModule.getArtifactHashmap;
    },
    addedArtifacts(): Record<string, Artifact> {
      return deltaModule.addedArtifacts;
    },
    addedArtifactNames(): string[] {
      return Object.keys(this.addedArtifacts);
    },
    removedArtifacts(): Record<string, Artifact> {
      return deltaModule.removedArtifacts;
    },
    removedArtifactNames(): string[] {
      return Object.keys(this.removedArtifacts);
    },
    modifiedArtifacts(): Record<string, EntityModification<Artifact>> {
      return deltaModule.modifiedArtifacts;
    },
    modifiedArtifactNames(): string[] {
      return Object.keys(this.modifiedArtifacts);
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

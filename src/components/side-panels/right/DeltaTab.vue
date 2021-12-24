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
          selectArtifact(addedArtifacts[id].name, addedArtifacts[id], 'added')
      "
    />
    <delta-button-group
      v-if="isDeltaMode"
      deltaType="removed"
      :names="removedArtifactNames"
      :ids="removedArtifactIds"
      @click="
        (id) =>
          selectArtifact(
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
          selectArtifact(
            modifiedArtifacts[id].after.name,
            modifiedArtifacts[id],
            'modified'
          )
      "
    />
    <artifact-delta-diff
      v-if="selectedDeltaArtifact !== undefined"
      :isOpen="selectedDeltaArtifact !== undefined"
      :name="selectedDeltaArtifact[0]"
      :input-artifact="selectedDeltaArtifact[1]"
      :delta-type="selectedDeltaArtifact[2]"
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
    addedArtifacts(): Record<string, Artifact> {
      return deltaModule.addedArtifacts;
    },
    addedArtifactNames(): string[] {
      return Object.values(this.addedArtifacts).map((a) => a.name);
    },
    addedArtifactIds(): string[] {
      return Object.values(this.addedArtifacts).map((a) => a.id);
    },
    removedArtifacts(): Record<string, Artifact> {
      return deltaModule.removedArtifacts;
    },
    removedArtifactNames(): string[] {
      return Object.values(this.removedArtifacts).map((a) => a.name);
    },
    removedArtifactIds(): string[] {
      return Object.values(this.removedArtifacts).map((a) => a.id);
    },
    modifiedArtifacts(): Record<string, EntityModification<Artifact>> {
      return deltaModule.modifiedArtifacts;
    },
    modifiedArtifactNames(): string[] {
      return Object.values(this.modifiedArtifacts).map((a) => a.after.name);
    },
    modifiedArtifactIds(): string[] {
      return Object.values(this.modifiedArtifacts).map((a) => a.after.id);
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

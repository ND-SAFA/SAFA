<template>
  <v-container>
    <v-expansion-panels class="ma-0 pa-0" multiple v-model="openPanels">
      <DeltaStateNav />
      <DeltaButtonGroup
        v-if="isDeltaMode"
        deltaType="added"
        class="mt-10"
        :artifacts="artifactsAdded"
        @onArtifactClick="(name) => selectArtifact(name, artifactsAdded[name])"
      />
      <DeltaButtonGroup
        v-if="isDeltaMode"
        deltaType="removed"
        :artifacts="artifactsRemoved"
        @onArtifactClick="
          (name) => selectArtifact(name, artifactsRemoved[name])
        "
      />
      <DeltaButtonGroup
        v-if="isDeltaMode"
        deltaType="modified"
        :artifacts="artifactsModified"
        @onArtifactClick="
          (name) => selectArtifact(name, artifactsModified[name])
        "
      />
    </v-expansion-panels>
    <ArtifactDeltaDiff
      v-if="selectedDeltaArtifact !== undefined"
      :isOpen="selectedDeltaArtifact !== undefined"
      :artifact="selectedDeltaArtifact[1]"
      :name="selectedDeltaArtifact[0]"
      @onClose="closeDeltaModal"
    />
  </v-container>
</template>

<script lang="ts">
import {
  AddedArtifact,
  ArtifactDelta,
  ModifiedArtifact,
  RemovedArtifact,
  DeltaArtifacts,
  Artifact,
} from "@/types";
import ArtifactDeltaDiff from "@/components/side-panels/right/delta-tab/ArtifactDeltaDiff.vue";
import DeltaButtonGroup from "@/components/side-panels/right/delta-tab/DeltaButtonGroup.vue";
import DeltaStateNav from "@/components/side-panels/right/delta-tab/DeltaPanelNav.vue";
import Vue from "vue";
import { deltaModule, projectModule } from "@/store";

type OptionalDeltaArtifact = [string, ArtifactDelta] | undefined;

export default Vue.extend({
  components: { ArtifactDeltaDiff, DeltaButtonGroup, DeltaStateNav },
  data() {
    return {
      selectedDeltaArtifact: undefined as OptionalDeltaArtifact,
      openPanels: [] as number[],
    };
  },
  methods: {
    selectArtifact(name: string, artifact: ArtifactDelta): void {
      this.selectedDeltaArtifact = [name, artifact];
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
    artifactsAdded(): Record<string, AddedArtifact> {
      return deltaModule.getAdded;
    },
    artifactsRemoved(): Record<string, RemovedArtifact> {
      return deltaModule.getRemoved;
    },
    artifactsModified(): Record<string, ModifiedArtifact> {
      return deltaModule.getModified;
    },
    deltaArtifacts(): DeltaArtifacts {
      return {
        added: this.artifactsAdded,
        removed: this.artifactsRemoved,
        modified: this.artifactsModified,
      };
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

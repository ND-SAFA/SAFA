<template>
  <v-container>
    <v-row>
      <v-expansion-panels>
        <artifact-file-panel
          v-for="(artifactFile, i) in artifactFiles"
          :key="artifactFile.type"
          :artifactFile="artifactFile"
          :traceFiles="getTraceFiles(artifactFile)"
          :menuLabels="getMenuLabels(artifactFile.type)"
          @onAddTracePath="addTraceFile($event)"
          @onAddTraceFile="addTraceFile($event)"
          @onClearTraceFile="addTraceFile($event)"
          @onAddFile="addFile(i, $event)"
          @onClearFile="clearFile(i)"
          @onDelete="deleteArtifactFile(i)"
        />
      </v-expansion-panels>
    </v-row>
    <v-row justify="center" class="mt-5">
      <v-container>
        <v-row
          v-if="artifactFiles.length === 0"
          justify="center"
          style="color: red"
          class="mb-10"
        >
          <label>No Artifact Types have been created.</label>
        </v-row>
        <v-row justify="center">
          <v-btn
            @click="isCreateArtifactOpen = true"
            small
            fab
            color="secondary"
          >
            <v-icon> mdi-plus </v-icon>
          </v-btn>
        </v-row>
      </v-container>
    </v-row>
    <ArtifactNameModal
      :isOpen="isCreateArtifactOpen"
      @onSubmit="addArtifactFile"
      @onClose="isCreateArtifactOpen = false"
    />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { ArtifactFile, TraceFile } from "@/types/common-components";
import ArtifactFilePanel from "@/components/project/creator/ArtifactFilePanel.vue";
import ArtifactNameModal from "@/components/project/creator/ArtifactNameModal.vue";

export default Vue.extend({
  components: {
    ArtifactFilePanel,
    ArtifactNameModal,
  },
  data() {
    return {
      traceFiles: [] as TraceFile[],
      artifactFiles: [] as ArtifactFile[],
      isCreateArtifactOpen: false,
    };
  },
  computed: {
    artifactTypes(): string[] {
      return this.artifactFiles.map((artifactFile) => artifactFile.type);
    },
  },
  methods: {
    deleteArtifactFile(i: number): void {
      this.artifactFiles = this.artifactFiles.filter((f, index) => index !== i);
    },
    addArtifactFile(artifactName: string): void {
      this.artifactFiles = this.artifactFiles.concat([
        {
          type: artifactName,
        },
      ]);
    },
    addFile(i: number, file: File): void {
      Vue.set(this.artifactFiles, i, { ...this.artifactFiles[i], file });
    },
    clearFile(i: number): void {
      Vue.set(this.artifactFiles, i, {
        ...this.artifactFiles[i],
        file: undefined,
      });
    },
    getTraceFiles(artifactFile: ArtifactFile): TraceFile[] {
      return this.traceFiles.filter(
        (f) => f.source === artifactFile.type || f.target === artifactFile.type
      );
    },
    getMenuLabels(source: string): string[] {
      const traceIds = this.traceFiles.map((f) => `${f.source}-${f.target}`);
      return this.artifactTypes.filter((type) => {
        return (
          !traceIds.includes(`${type}-${source}`) &&
          !traceIds.includes(`${source}-${type}`) &&
          type !== source
        );
      });
    },

    addTraceFile(newTraceFile: TraceFile): void {
      const other: TraceFile[] = this.traceFiles.filter((f) => {
        return (
          f.source !== newTraceFile.source && f.target !== newTraceFile.target
        );
      });
      this.traceFiles = other.concat([newTraceFile]);
    },
  },
});
</script>

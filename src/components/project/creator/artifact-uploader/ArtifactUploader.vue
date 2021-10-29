<template>
  <v-container>
    <PanelController
      noItemError="No artifacts have been uploaded."
      :showError="artifactFiles.length === 0"
      :isValidStates="isValidStates"
      @onAdd="isCreateArtifactOpen = true"
      @onIsValid="$emit('onIsValid')"
      @onIsInvalid="$emit('onIsInvalid')"
    >
      <template v-slot:panels>
        <ArtifactFilePanel
          v-for="(artifactFile, i) in artifactFiles"
          :key="artifactFile.type"
          :artifactFile="artifactFile"
          @onChange="onChange(i, $event)"
          @onDelete="deleteArtifactFile(i)"
          @onIsValid="setFileIsValid(i, true)"
          @onIsInvalid="setFileIsValid(i, false)"
        />
      </template>
    </PanelController>
    <ArtifactNameModal
      :isOpen="isCreateArtifactOpen"
      @onSubmit="addArtifactFile"
      @onClose="isCreateArtifactOpen = false"
    />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { ArtifactFile } from "@/types/common-components";
import ArtifactFilePanel from "@/components/project/creator/artifact-uploader/ArtifactFilePanel.vue";
import ArtifactNameModal from "@/components/project/creator/artifact-uploader/ArtifactNameModal.vue";
import PanelController from "@/components/project/creator/shared/PanelController.vue";

const DEFAULT_VALID_STATE = false;

export default Vue.extend({
  components: {
    ArtifactFilePanel,
    ArtifactNameModal,
    PanelController,
  },
  data() {
    return {
      isValidStates: [] as boolean[],
      artifactFiles: [] as ArtifactFile[],
      isCreateArtifactOpen: false,
    };
  },
  watch: {
    isValid(): void {
      if (this.isValid) {
        this.$emit("onIsValid");
      } else {
        this.$emit("onIsInvalid");
      }
    },
  },
  computed: {
    isValid(): boolean {
      return this.isValidStates.filter((isValid) => !isValid).length === 0;
    },
  },
  methods: {
    onChange(i: number, file: File | undefined): void {
      Vue.set(this.artifactFiles, i, { ...this.artifactFiles[i], file });
      this.$emit("onChange", this.artifactFiles);
    },
    setFileIsValid(artifactFileIndex: number, isValid: boolean): void {
      Vue.set(this.isValidStates, artifactFileIndex, isValid);
    },
    deleteArtifactFile(i: number): void {
      this.artifactFiles = this.artifactFiles.filter((f, index) => index !== i);
    },
    addArtifactFile(artifactName: string): void {
      this.artifactFiles = this.artifactFiles.concat([
        {
          type: artifactName,
        },
      ]);
      this.isValidStates = this.isValidStates.concat([DEFAULT_VALID_STATE]);
      this.$emit("onChange", this.artifactFiles);
    },
  },
});
</script>

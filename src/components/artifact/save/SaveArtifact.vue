<template>
  <div>
    <save-artifact-inputs />
    <v-divider class="my-4" />
    <flex-box justify="space-between">
      <v-btn
        text
        v-if="isUpdate"
        color="error"
        @click="handleDelete"
        data-cy="button-artifact-delete"
      >
        <v-icon class="mr-1">mdi-delete</v-icon>
        Delete
      </v-btn>
      <v-spacer />
      <v-btn
        color="primary"
        :disabled="!canSave"
        data-cy="button-artifact-save"
        @click="handleSubmit"
      >
        <v-icon class="mr-1">mdi-content-save</v-icon>
        Save
      </v-btn>
    </flex-box>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { ArtifactSchema, CreatorOpenState } from "@/types";
import { appStore, artifactSaveStore, selectionStore } from "@/hooks";
import { handleDeleteArtifact, handleSaveArtifact } from "@/api";
import { FlexBox } from "@/components/common";
import SaveArtifactInputs from "./SaveArtifactInputs.vue";

/**
 * Displays inputs for editing and saving artifacts.
 */
export default Vue.extend({
  name: "SaveArtifact",
  components: {
    FlexBox,
    SaveArtifactInputs,
  },
  data() {
    return {
      isLoading: false,
    };
  },
  mounted() {
    artifactSaveStore.resetArtifact(true);
  },
  computed: {
    /**
     * @return The base artifact being edited.
     */
    baseArtifact(): ArtifactSchema | undefined {
      return selectionStore.selectedArtifact;
    },
    /**
     * @return Whether the artifact creator is open.
     */
    isOpen(): CreatorOpenState {
      return appStore.isDetailsPanelOpen && appStore.isArtifactCreatorOpen;
    },
    /**
     * @return  Whether the artifact can be saved.
     */
    canSave(): boolean {
      return artifactSaveStore.canSave;
    },
    /**
     * @return Whether an existing artifact is being updated.
     */
    isUpdate(): boolean {
      return artifactSaveStore.isUpdate;
    },
  },
  watch: {
    /**
     * Resets artifact data when opened.
     * If opened with a string, attempts to switch the artifact type to match the type given.
     */
    isOpen(openOrType: CreatorOpenState): void {
      if (!openOrType) return;

      artifactSaveStore.resetArtifact(openOrType);
    },
    /**
     * Resets artifact data when the base artifact changes.
     */
    baseArtifact(): void {
      artifactSaveStore.resetArtifact(true);
    },
  },
  methods: {
    /**
     * Attempts to delete the selected artifact.
     */
    handleDelete(): void {
      if (!this.baseArtifact) return;

      handleDeleteArtifact(this.baseArtifact, {
        onSuccess: () => appStore.closeSidePanels(),
      });
    },
    /**
     * Attempts to save the artifact.
     */
    handleSubmit(): void {
      this.isLoading = true;

      handleSaveArtifact(
        artifactSaveStore.finalizedArtifact,
        artifactSaveStore.isUpdate,
        artifactSaveStore.parentArtifact,
        {
          onSuccess: () => this.handleClose(),
          onComplete: () => (this.isLoading = false),
        }
      );
    },
    /**
     * Closes the artifact creator.
     */
    handleClose(): void {
      appStore.openDetailsPanel("displayArtifact");
    },
  },
});
</script>

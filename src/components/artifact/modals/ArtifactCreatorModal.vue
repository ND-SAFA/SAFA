<template>
  <generic-modal
    :title="creatorTitle"
    :is-open="!!isOpen"
    :is-loading="isLoading"
    size="l"
    data-cy="modal-artifact-save"
    @close="handleClose"
  >
    <template v-slot:body>
      <artifact-creator-inputs />
    </template>
    <template v-slot:actions>
      <v-row justify="end">
        <v-btn
          color="primary"
          :disabled="!canSave"
          data-cy="button-artifact-save"
          @click="handleSubmit"
        >
          Save
        </v-btn>
      </v-row>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue from "vue";
import { CreatorOpenState } from "@/types";
import { appStore, artifactSaveStore } from "@/hooks";
import { handleSaveArtifact } from "@/api";
import { GenericModal } from "@/components/common";
import ArtifactCreatorInputs from "./ArtifactCreatorInputs.vue";

/**
 * Modal for artifact creation.
 */
export default Vue.extend({
  name: "ArtifactCreator",
  components: {
    GenericModal,
    ArtifactCreatorInputs,
  },
  data() {
    return {
      isLoading: false,
    };
  },
  computed: {
    /**
     * Returns whether the artifact creator is open.
     */
    isOpen(): string | boolean {
      return appStore.isArtifactCreatorOpen;
    },
    /**
     * @return The name of the modal.
     */
    creatorTitle(): string {
      return artifactSaveStore.isUpdate ? "Edit Artifact" : "Create Artifact";
    },
    /**
     * @return  Whether the artifact can be saved.
     */
    canSave(): boolean {
      return artifactSaveStore.canSave;
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
  },
  methods: {
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
      appStore.closeArtifactCreator();
    },
  },
});
</script>

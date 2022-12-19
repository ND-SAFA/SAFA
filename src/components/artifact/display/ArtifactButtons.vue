<template>
  <flex-box t="2" v-if="doDisplay">
    <text-button
      text
      variant="artifact"
      data-cy="button-artifact-body"
      @click="handleViewBody"
    >
      View Body
    </text-button>
    <text-button
      text
      variant="edit"
      data-cy="button-artifact-edit"
      @click="handleEditArtifact"
    >
      Edit
    </text-button>
    <v-divider vertical />
    <text-button
      text
      variant="delete"
      data-cy="button-artifact-delete"
      @click="handleDeleteArtifact"
    >
      Delete
    </text-button>
  </flex-box>
</template>

<script lang="ts">
import Vue from "vue";
import { ArtifactSchema } from "@/types";
import { appStore, projectStore, selectionStore, sessionStore } from "@/hooks";
import { handleDeleteArtifact } from "@/api";
import { FlexBox, TextButton } from "@/components/common";

/**
 * Displays artifact buttons.
 */
export default Vue.extend({
  name: "ArtifactButtons",
  components: { TextButton, FlexBox },
  computed: {
    /**
     * @return Whether to display these actions.
     */
    doDisplay(): boolean {
      return sessionStore.isEditor(projectStore.project);
    },
    /**
     * @return The selected artifact.
     */
    artifact(): ArtifactSchema | undefined {
      return selectionStore.selectedArtifact;
    },
  },
  methods: {
    /**
     * Attempts to delete the selected artifact.
     */
    handleDeleteArtifact(): void {
      if (!this.artifact) return;

      handleDeleteArtifact(this.artifact, {
        onSuccess: () => appStore.closeSidePanels(),
      });
    },
    /**
     * Opens the artifact creator.
     */
    handleEditArtifact(): void {
      appStore.openArtifactCreatorTo({});
    },
    /**
     * Opens the artifact body display.
     */
    handleViewBody(): void {
      appStore.openDetailsPanel("displayArtifactBody");
    },
  },
});
</script>

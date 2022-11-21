<template>
  <flex-box t="2">
    <v-btn text data-cy="button-artifact-body" @click="handleViewBody">
      <v-icon class="mr-1">mdi-application-array-outline</v-icon>
      View Body
    </v-btn>
    <v-btn text data-cy="button-artifact-edit" @click="handleEditArtifact">
      <v-icon class="mr-1">mdi-pencil</v-icon>
      Edit
    </v-btn>
    <v-divider vertical />
    <v-btn
      text
      color="error"
      data-cy="button-artifact-delete"
      @click="handleDeleteArtifact"
    >
      <v-icon class="mr-1">mdi-delete</v-icon>
      Delete
    </v-btn>
  </flex-box>
</template>

<script lang="ts">
import Vue from "vue";
import { ArtifactModel } from "@/types";
import { appStore, selectionStore } from "@/hooks";
import { handleDeleteArtifact } from "@/api";
import { FlexBox } from "@/components/common";

/**
 * Displays artifact buttons.
 */
export default Vue.extend({
  name: "ArtifactButtons",
  components: { FlexBox },
  computed: {
    /**
     * @return The selected artifact.
     */
    artifact(): ArtifactModel | undefined {
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

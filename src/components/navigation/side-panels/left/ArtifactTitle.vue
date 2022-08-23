<template>
  <div class="mt-2">
    <v-row justify="end" class="mr-1 mb-1">
      <generic-icon-button
        tooltip="View Artifact Body"
        icon-id="mdi-application-array-outline"
        @click="handleViewBody"
      />
      <generic-icon-button
        v-if="!selectedArtifact.logicType"
        tooltip="Edit"
        icon-id="mdi-pencil"
        @click="handleEditArtifact"
      />
      <generic-icon-button
        color="error"
        tooltip="Delete"
        icon-id="mdi-delete"
        @click="handleDeleteArtifact"
      />
    </v-row>
    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <typography
          ellipsis
          v-on="on"
          v-bind="attrs"
          variant="subtitle"
          el="h1"
          :value="selectedArtifactName"
        />
      </template>
      {{ selectedArtifactName }}
    </v-tooltip>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { PanelType } from "@/types";
import { appStore, selectionStore } from "@/hooks";
import { handleDeleteArtifact } from "@/api";
import { GenericIconButton, Typography } from "@/components/common";

/**
 * Displays the selected node's title and option buttons.
 */
export default Vue.extend({
  name: "ArtifactTitle",
  components: {
    Typography,
    GenericIconButton,
  },
  computed: {
    /**
     * @return The selected artifact.
     */
    selectedArtifact() {
      return selectionStore.selectedArtifact;
    },
    /**
     * @return The selected artifact's name.
     */
    selectedArtifactName(): string {
      return this.selectedArtifact?.name || "";
    },
    /**
     * @return The selected artifact's body.
     */
    selectedArtifactBody(): string {
      return this.selectedArtifact?.body.trim() || "";
    },
    /**
     * An incredibly crude and temporary way to distinguish code nodes.
     *
     * @return Whether to display this body as code.
     */
    isCodeDisplay(): boolean {
      return this.selectedArtifact?.type.includes("code") || false;
    },
  },
  methods: {
    /**
     * Attempts to delete the selected artifact.
     */
    handleDeleteArtifact(): void {
      if (this.selectedArtifact !== undefined) {
        handleDeleteArtifact(this.selectedArtifact, {
          onSuccess: () => appStore.closePanel(PanelType.left),
        });
      }
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
      appStore.toggleArtifactBody();
    },
  },
});
</script>

<style scoped>
.artifact-title {
  width: 230px;
}
</style>

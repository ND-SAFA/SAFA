<template>
  <v-row align="center">
    <v-col>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <h1 v-on="on" v-bind="attrs" class="text-h4 artifact-title">
            {{ selectedArtifact.name }}
          </h1>
        </template>
        {{ selectedArtifact.name }}
      </v-tooltip>
    </v-col>
    <v-col>
      <v-row justify="end" class="mr-1">
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
        <artifact-creator-modal
          title="Edit Artifact Contents"
          :is-open="isArtifactCreatorOpen"
          :artifact="selectedArtifact"
          @close="isArtifactCreatorOpen = false"
        />
      </v-row>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import Vue from "vue";
import { PanelType } from "@/types";
import { appModule, artifactSelectionModule } from "@/store";
import { handleDeleteArtifact } from "@/api";
import { GenericIconButton } from "@/components/common";
import { ArtifactCreatorModal } from "@/components/artifact";

/**
 * Displays the selected node's title and option buttons.
 */
export default Vue.extend({
  name: "ArtifactTitle",
  components: { GenericIconButton, ArtifactCreatorModal },
  data() {
    return {
      isArtifactCreatorOpen: false,
    };
  },
  computed: {
    /**
     * @return The selected artifact.
     */
    selectedArtifact() {
      return artifactSelectionModule.getSelectedArtifact;
    },
    /**
     * @return The selected artifact's name.
     */
    selectedArtifactName(): string {
      return this.selectedArtifact?.name || "";
    },
  },
  methods: {
    /**
     * Opens the artifact edit modal.
     */
    handleEditArtifact(): void {
      this.isArtifactCreatorOpen = true;
    },
    /**
     * Attempts to delete the selected artifact.
     */
    handleDeleteArtifact(): void {
      if (this.selectedArtifact !== undefined) {
        handleDeleteArtifact(this.selectedArtifact).then(() => {
          appModule.closePanel(PanelType.left);
        });
      }
    },
  },
});
</script>

<style scoped>
.artifact-title {
  overflow: hidden;
  text-overflow: ellipsis;
  width: 135px;
}
</style>

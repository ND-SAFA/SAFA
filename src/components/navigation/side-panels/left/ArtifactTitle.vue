<template>
  <div class="my-2">
    <v-row justify="end" class="mr-1 mb-1">
      <generic-icon-button
        tooltip="View Artifact Body"
        icon-id="mdi-code-tags"
        @click="isArtifactBodyOpen = true"
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
        <h1
          v-on="on"
          v-bind="attrs"
          class="text-h6 text-ellipsis artifact-title"
        >
          {{ selectedArtifactName }}
        </h1>
      </template>
      {{ selectedArtifactName }}
    </v-tooltip>

    <generic-modal
      :is-open="isArtifactBodyOpen"
      :title="selectedArtifactName"
      :actionsHeight="0"
      size="l"
      @close="isArtifactBodyOpen = false"
    >
      <template v-slot:body>
        <pre class="text-body-1 mt-2 overflow-auto">
          {{ selectedArtifactBody }}
        </pre>
      </template>
    </generic-modal>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { PanelType } from "@/types";
import { appModule, artifactSelectionModule } from "@/store";
import { handleDeleteArtifact } from "@/api";
import { GenericIconButton, GenericModal } from "@/components/common";

/**
 * Displays the selected node's title and option buttons.
 */
export default Vue.extend({
  name: "ArtifactTitle",
  components: {
    GenericModal,
    GenericIconButton,
  },
  data() {
    return {
      isArtifactBodyOpen: false,
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
    /**
     * @return The selected artifact's body.
     */
    selectedArtifactBody(): string {
      return this.selectedArtifact?.body.trim() || "";
    },
  },
  methods: {
    /**
     * Attempts to delete the selected artifact.
     */
    handleDeleteArtifact(): void {
      if (this.selectedArtifact !== undefined) {
        handleDeleteArtifact(this.selectedArtifact, {
          onSuccess: () => appModule.closePanel(PanelType.left),
        });
      }
    },
    /**
     * Opens the artifact creator.
     */
    handleEditArtifact(): void {
      appModule.openArtifactCreatorTo();
    },
  },
});
</script>

<style scoped>
.artifact-title {
  width: 230px;
}
</style>

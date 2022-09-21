<template>
  <div>
    <flex-box align="center" justify="space-between">
      <attribute-chip
        artifact-type
        :value="selectedArtifactType"
        data-cy="text-selected-type"
      />
      <flex-box>
        <generic-icon-button
          tooltip="View Artifact Body"
          icon-id="mdi-application-array-outline"
          data-cy="button-selected-body"
          @click="handleViewBody"
        />
        <generic-icon-button
          v-if="isEditor && !selectedArtifact.logicType"
          tooltip="Edit"
          icon-id="mdi-pencil"
          data-cy="button-selected-edit"
          @click="handleEditArtifact"
        />
        <generic-icon-button
          v-if="isEditor"
          color="error"
          tooltip="Delete"
          icon-id="mdi-delete"
          data-cy="button-selected-delete"
          @click="handleDeleteArtifact"
        />
      </flex-box>
    </flex-box>
    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <typography
          ellipsis
          v-on="on"
          v-bind="attrs"
          variant="subtitle"
          el="h1"
          :value="selectedArtifactName"
          data-cy="text-selected-name"
        />
      </template>
      {{ selectedArtifactName }}
    </v-tooltip>
    <v-divider />
    <typography
      defaultExpanded
      y="2"
      variant="expandable"
      :value="selectedArtifactBody"
      data-cy="text-selected-body"
    />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { PanelType } from "@/types";
import { appStore, projectStore, selectionStore, sessionStore } from "@/hooks";
import { handleDeleteArtifact } from "@/api";
import { GenericIconButton, Typography } from "@/components/common";
import FlexBox from "@/components/common/display/FlexBox.vue";
import AttributeChip from "@/components/common/display/AttributeChip.vue";

/**
 * Displays the selected node's title and option buttons.
 */
export default Vue.extend({
  name: "ArtifactTitle",
  components: {
    AttributeChip,
    FlexBox,
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
     * @return The selected artifact's type.
     */
    selectedArtifactType(): string {
      return this.selectedArtifact?.type || "";
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
    /**
     * @return Whether the current user is an editor of the current project.
     */
    isEditor(): boolean {
      return sessionStore.isEditor(projectStore.project);
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

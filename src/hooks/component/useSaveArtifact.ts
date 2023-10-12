import { defineStore } from "pinia";

import { ArtifactCreatorOpenState, ArtifactSchema } from "@/types";
import { buildArtifact } from "@/util";
import {
  selectionStore,
  artifactStore,
  documentStore,
  appStore,
} from "@/hooks";
import { pinia } from "@/plugins";

/**
 * The save artifact store assists in creating and editing artifacts.
 */
export const useSaveArtifact = defineStore("saveArtifact", {
  state: () => ({
    /**
     * The artifact being created or edited.
     */
    editedArtifact: buildArtifact(selectionStore.selectedArtifact),
    /**
     * The id of the parent artifact to connect to, if there is one.
     */
    parentId: "",
    /**
     * Whether the artifact's name is valid.
     */
    isNameValid: false,
  }),
  getters: {
    /**
     * @return Whether an existing artifact is being updated.
     */
    isUpdate(): boolean {
      return !!selectionStore.selectedArtifact;
    },
    /**
     * @return Whether the artifact name has changed.
     */
    hasNameChanged(): boolean {
      return selectionStore.selectedArtifact?.name !== this.editedArtifact.name;
    },
    /**
     * @return Whether the base artifact has a summary.
     */
    hasSummary(): boolean {
      return !!selectionStore.selectedArtifact?.summary;
    },
    /**
     * @return The parent artifact of a logic node.
     */
    parentArtifact(): ArtifactSchema | undefined {
      return this.parentId
        ? artifactStore.getArtifactById(this.parentId)
        : undefined;
    },
    /**
     * @return Any errors to report on the name.
     */
    nameError(): string | false {
      return this.isNameValid || this.editedArtifact.name === ""
        ? false
        : "This name is already used, please select another.";
    },
    /**
     * @return Whether the artifact is valid and can be saved.
     */
    canSave(): boolean {
      const { type, body } = this.editedArtifact;

      return !!(this.isNameValid && body && type);
    },
    /**
     * @return The savable artifact data based on the edited artifact's fields.
     */
    finalizedArtifact(): ArtifactSchema {
      const { documentId } = documentStore.currentDocument;

      return buildArtifact({
        ...this.editedArtifact,
        documentIds: documentId ? [documentId] : [],
      });
    },
  },
  actions: {
    /**
     * Resets the state of the artifact to the selected artifact.
     */
    resetArtifact(): void {
      const artifact = selectionStore.selectedArtifact;

      this.editedArtifact = buildArtifact(artifact);
      this.isNameValid = !!artifact?.name;
      this.parentId = "";
    },

    /**
     * Opens the artifact creator to a specific node type.
     *
     * @param openTo - What to open to.
     */
    openPanel(openTo: {
      type?: ArtifactCreatorOpenState;
      isNewArtifact?: boolean;
    }): void {
      const { isNewArtifact } = openTo;

      if (isNewArtifact) selectionStore.clearSelections();

      this.resetArtifact();
      appStore.openDetailsPanel("saveArtifact");
    },
  },
});

export default useSaveArtifact(pinia);

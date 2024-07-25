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
    editedArtifact: buildArtifact(artifactStore.selectedArtifact),
    /**
     * The ids of the parent artifacts to connect to.
     */
    parentIds: [] as string[],
    /**
     * The ids of the child artifacts to connect to.
     */
    childIds: [] as string[],
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
      return !!artifactStore.selectedArtifact;
    },
    /**
     * @return Whether the artifact name has changed.
     */
    hasNameChanged(): boolean {
      return artifactStore.selectedArtifact?.name !== this.editedArtifact.name;
    },
    /**
     * @return Whether the base artifact has a summary.
     */
    hasSummary(): boolean {
      return !!artifactStore.selectedArtifact?.summary;
    },
    /**
     * @return The parent artifacts.
     */
    parentArtifacts(): ArtifactSchema[] {
      return this.parentIds
        .map((id) => artifactStore.getArtifactById(id))
        .filter((artifact) => !!artifact) as ArtifactSchema[];
    },
    /**
     * @return The child artifacts.
     */
    childArtifacts(): ArtifactSchema[] {
      return this.childIds
        .map((id) => artifactStore.getArtifactById(id))
        .filter((artifact) => !!artifact) as ArtifactSchema[];
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
     * @param updatedArtifact - Any artifact fields to set in the new edited artifact.
     * @param parentId - Any parent artifact to link to.
     */
    resetArtifact(
      updatedArtifact: Partial<ArtifactSchema> = {},
      parentId = ""
    ): void {
      const baseArtifact = artifactStore.selectedArtifact;

      this.editedArtifact = buildArtifact({
        ...(baseArtifact || {}),
        ...updatedArtifact,
      });
      this.isNameValid = !!this.editedArtifact.name;
      this.parentIds = parentId ? [parentId] : [];
      this.childIds = [];
    },

    /**
     * Opens the artifact creator to a specific node type.
     *
     * @param openTo - What to open to.
     */
    openPanel(openTo: ArtifactCreatorOpenState): void {
      const { isNewArtifact, artifact, parentId } = openTo;

      if (isNewArtifact) {
        selectionStore.clearSelections();
      } else if (artifact?.id) {
        selectionStore.selectArtifact(artifact.id);
      }

      this.resetArtifact(artifact, parentId);
      appStore.openDetailsPanel("saveArtifact");
    },
  },
});

export default useSaveArtifact(pinia);

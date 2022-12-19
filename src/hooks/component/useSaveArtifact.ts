import { defineStore } from "pinia";

import { ArtifactSchema, DocumentType } from "@/types";
import { createArtifact, createArtifactOfType } from "@/util";
import { pinia } from "@/plugins";
import selectionStore from "../graph/useSelection";
import artifactStore from "../project/useArtifacts";
import documentStore from "../project/useDocuments";

/**
 * The save artifact store assists in creating and editing artifacts.
 */
export const useSaveArtifact = defineStore("saveArtifact", {
  state: () => ({
    /**
     * The artifact being created or edited.
     */
    editedArtifact: createArtifact(selectionStore.selectedArtifact),
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
     * @return Whether the artifact type is for an FTA node.
     */
    isFTA(): boolean {
      return this.editedArtifact.documentType === DocumentType.FTA;
    },
    /**
     * @return Whether the artifact type is for a safety case node.
     */
    isSafetyCase(): boolean {
      return this.editedArtifact.documentType === DocumentType.SAFETY_CASE;
    },
    /**
     * @return Whether the artifact type is for an FMEA node.
     */
    isFMEA(): boolean {
      return this.editedArtifact.documentType === DocumentType.FMEA;
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
     * @return The computed type based on the artifact's document type.
     */
    computedArtifactType(): string {
      if (this.isFTA) {
        return this.parentArtifact?.type || this.editedArtifact.type;
      } else {
        return this.editedArtifact.type;
      }
    },
    /**
     * @return The computed name based on the artifact's document type.
     */
    computedName(): string {
      const { name, logicType } = this.editedArtifact;

      return this.isFTA
        ? `${this.parentArtifact?.name || this.parentId}-${logicType}`
        : name;
    },
    /**
     * @return Any errors to report on the name.
     */
    nameErrors(): string[] {
      return this.isNameValid || this.editedArtifact.name === ""
        ? []
        : ["This name is already used, please select another."];
    },
    canSave(): boolean {
      const { logicType, safetyCaseType, type, body } = this.editedArtifact;

      if (this.isFTA) {
        return !!(logicType && this.parentId);
      } else if (this.isSafetyCase) {
        return !!(this.isNameValid && body && safetyCaseType);
      } else if (this.isFMEA) {
        return !!(this.isNameValid && body);
      } else {
        return !!(this.isNameValid && body && type);
      }
    },
    /**
     * @return The savable artifact data based on the edited artifact's fields.
     */
    finalizedArtifact(): ArtifactSchema {
      const { documentId } = documentStore.currentDocument;
      const { logicType, safetyCaseType } = this.editedArtifact;

      return createArtifact({
        ...this.editedArtifact,
        name: this.computedName,
        type: this.computedArtifactType,
        documentIds: documentId ? [documentId] : [],
        logicType: this.isFTA ? logicType : undefined,
        safetyCaseType: this.isSafetyCase ? safetyCaseType : undefined,
      });
    },
  },
  actions: {
    /**
     * Resets the state of the artifact to the selected artifact.
     *
     * @param type - The type of artifact creation to open to.
     */
    resetArtifact(type: true | string | undefined): void {
      const artifact = selectionStore.selectedArtifact;

      this.editedArtifact = createArtifactOfType(artifact, type);
      this.isNameValid = !!artifact?.name;
    },
    /**
     * Updates the edited artifact to a new type.
     */
    updateArtifactType(): void {
      this.editedArtifact = createArtifactOfType(
        this.editedArtifact,
        this.editedArtifact.type
      );
    },
  },
});

export default useSaveArtifact(pinia);

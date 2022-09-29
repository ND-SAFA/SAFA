import { defineStore } from "pinia";
import { watch } from "@vue/composition-api";

import { ArtifactModel, DocumentType } from "@/types";
import { createArtifact, createArtifactOfType } from "@/util";
import { pinia } from "@/plugins";
import selectionStore from "../graph/useSelection";
import artifactStore from "../project/useArtifacts";
import documentStore from "../project/useDocuments";

/**
 * The use artifact store assists in creating and editing artifacts.
 */
export const useSaveArtifact = defineStore("useArtifact", {
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
    /**
     * Whether the edited artifact can be saved.
     */
    canSave: false,
  }),
  getters: {
    /**
     * @return Whether an existing artifact is being updated.
     */
    isUpdate(): boolean {
      return !!selectionStore.selectedArtifact;
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
    parentArtifact(): ArtifactModel | undefined {
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
     * @return The savable artifact data based on the edited artifact's fields.
     */
    finalizedArtifact(): ArtifactModel {
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
      this.updateCanSave();
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
    /**
     * Updates whether the edited artifact can be saved.
     */
    updateCanSave(): void {
      const { logicType, safetyCaseType, type, body } = this.editedArtifact;

      if (this.isFTA) {
        this.canSave = !!(logicType && this.parentId);
      } else if (this.isSafetyCase) {
        this.canSave = !!(this.isNameValid && body && safetyCaseType);
      } else if (this.isFMEA) {
        this.canSave = !!(this.isNameValid && body);
      } else {
        this.canSave = !!(this.isNameValid && body && type);
      }
    },
  },
});

const artifactSaveStore = useSaveArtifact(pinia);

/**
 * Check for artifact validity when fields change.
 */
watch(
  artifactSaveStore.editedArtifact,
  () => artifactSaveStore.updateCanSave(),
  {
    deep: true,
  }
);
watch([artifactSaveStore.isNameValid, artifactSaveStore.parentId], () =>
  artifactSaveStore.updateCanSave()
);

/**
 * Update artifact fields when the type changes.
 */
watch([artifactSaveStore.editedArtifact.type], () =>
  artifactSaveStore.updateArtifactType()
);

export default artifactSaveStore;

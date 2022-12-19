import { defineStore } from "pinia";

import { DocumentSchema } from "@/types";
import { createDocument } from "@/util";
import { pinia } from "@/plugins";
import artifactStore from "../project/useArtifacts";
import documentStore from "../project/useDocuments";
import subtreeStore from "../project/useSubtree";

/**
 * The save document store assists in creating and editing documents.
 */
export const useSaveDocument = defineStore("saveDocument", {
  state: () => ({
    /**
     * A base document being edited.
     */
    baseDocument: undefined as DocumentSchema | undefined,
    /**
     * The document being created or edited.
     */
    editedDocument: createDocument(),
    /**
     * The types of included artifacts.
     */
    includedTypes: [] as string[],
    /**
     * Whether to include child artifacts.
     */
    includeChildren: false,
    /**
     * The types of included child artifacts.
     */
    includedChildTypes: [] as string[],
    /**
     * The ids of included child artifacts.
     */
    childIds: [] as string[],
  }),
  getters: {
    /**
     * @return Whether an existing document is being updated.
     */
    isUpdate(): boolean {
      return !!this.baseDocument;
    },
    /**
     * @return Whether the current document name is valid.
     */
    isNameValid(): boolean {
      return (
        !documentStore.doesDocumentExist(this.editedDocument?.name) ||
        this.baseDocument?.name === this.editedDocument.name
      );
    },
    /**
     * @return Document name errors to display.
     */
    nameErrors(): string[] {
      return this.isNameValid
        ? []
        : ["This name is already used, please select another."];
    },
    /**
     * @return Whether the document can be saved.
     */
    canSave(): boolean {
      return this.editedDocument.name.length > 0 && this.isNameValid;
    },
    /**
     * @return The finalized document being saved.
     */
    finalizedDocument(): DocumentSchema {
      return {
        ...this.editedDocument,
        artifactIds: this.includeChildren
          ? [...this.editedDocument.artifactIds, ...this.childIds]
          : this.editedDocument.artifactIds,
      };
    },
  },
  actions: {
    /**
     * Resets the document value to the given base value.
     */
    resetDocument(): void {
      this.editedDocument = createDocument(this.baseDocument);
      this.includedTypes = [];
      this.includeChildren = false;
      this.includedChildTypes = [];
      this.childIds = [];
    },
    /**
     * Generates artifacts to save on this document.
     */
    updateArtifacts(): void {
      const baseArtifacts = this.baseDocument?.artifactIds || [];

      this.editedDocument.artifactIds =
        this.includedTypes.length > 0
          ? artifactStore.allArtifacts
              .filter(
                ({ id, type }) =>
                  this.includedTypes.includes(type) ||
                  baseArtifacts.includes(id)
              )
              .map(({ id }) => id)
          : baseArtifacts;
    },
    /**
     * Generates child artifacts to save on this document.
     */
    updateChildArtifacts(): void {
      this.childIds = subtreeStore.getMatchingChildren(
        this.editedDocument.artifactIds,
        this.includedChildTypes
      );
    },
  },
});

export default useSaveDocument(pinia);

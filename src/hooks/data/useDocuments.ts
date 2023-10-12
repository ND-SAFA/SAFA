import { defineStore } from "pinia";

import {
  LayoutPositionsSchema,
  DocumentSchema,
  DocumentType,
  ProjectSchema,
  ArtifactSchema,
} from "@/types";
import { buildDocument, DEFAULT_VIEW_NAME, removeMatches } from "@/util";
import {
  subtreeStore,
  layoutStore,
  projectStore,
  traceStore,
  artifactStore,
  selectionStore,
} from "@/hooks";
import { pinia } from "@/plugins";

/**
 * This module keeps track of the different document views for a project.
 */
export const useDocuments = defineStore("documents", {
  state() {
    const baseDocument = buildDocument();

    return {
      /**
       * The base document with all artifacts.
       */
      baseDocument,
      /**
       * The currently visible document.
       */
      currentDocument: baseDocument,
      /**
       * All custom project documents.
       */
      allDocuments: [baseDocument],
    };
  },
  getters: {
    /**
     * @return All custom documents & the base document.
     */
    projectDocuments(): DocumentSchema[] {
      return [...this.allDocuments, this.baseDocument];
    },
    /**
     * @return The current document id.
     */
    currentId(): string {
      return this.currentDocument.documentId;
    },
    /**
     * @return The current document type.
     */
    currentType(): DocumentType {
      return this.currentDocument.type;
    },
    /**
     * @return The current artifact ids.
     */
    currentArtifactIds(): string[] {
      return this.currentDocument.artifactIds;
    },
    /**
     * @return Whether the selected document is the base document.
     */
    isBaseDocument(): boolean {
      return this.currentId === "";
    },
  },
  actions: {
    /**
     * Initializes the current artifacts and traces visible in the current document.
     */
    initializeProject(project: ProjectSchema): void {
      const {
        artifacts,
        traces,
        currentDocumentId = this.currentDocument.documentId,
        documents = [],
        layout,
      } = project;

      const defaultDocument = buildDocument({
        name: DEFAULT_VIEW_NAME,
        project,
        artifactIds: artifacts.map(({ id }) => id),
        layout,
      });

      const loadedDocument =
        documents.find(({ documentId }) => documentId === currentDocumentId) ||
        defaultDocument;
      const currentArtifactIds = loadedDocument.artifactIds;

      this.allDocuments = documents;
      this.baseDocument = defaultDocument;
      this.currentDocument = loadedDocument;

      artifactStore.initializeArtifacts({ artifacts, currentArtifactIds });
      traceStore.initializeTraces({ traces, currentArtifactIds });
      layoutStore.updatePositions(loadedDocument.layout);
    },
    /**
     * Updates the given document's layout, and reruns the layout if on the base document.
     * @param documentId - The document to update.
     * @param layout - The new layout to set.
     */
    updateDocumentLayout(
      documentId: string,
      layout: LayoutPositionsSchema
    ): void {
      const document = this.allDocuments.find(
        (document) => documentId === document.documentId
      );

      if (!document) return;

      document.layout = layout;

      if (document.documentId !== this.currentId) return;

      layoutStore.updatePositions(layout);
    },
    /**
     * Updates the base document's layout, and reruns the layout if on the base document.
     * @param layout - The new layout to set.
     */
    updateBaseLayout(layout: LayoutPositionsSchema): void {
      projectStore.updateProject({ layout });

      this.baseDocument.layout = layout;

      if (!this.isBaseDocument) return;

      layoutStore.updatePositions(layout);
    },
    /**
     * Updates matching documents.
     *
     * @param updatedDocuments - The updated documents.
     */
    async updateDocuments(updatedDocuments: DocumentSchema[]): Promise<void> {
      const updatedIds = updatedDocuments.map((d) => d.documentId);
      const currentDocument = updatedDocuments.find(
        ({ documentId }) => documentId === this.currentId
      );

      if (currentDocument) {
        await this.switchDocuments(currentDocument);
      }

      this.allDocuments = [
        ...removeMatches(this.allDocuments, "documentId", updatedIds),
        ...updatedDocuments,
      ];
    },
    /**
     * Sets the current document and initializes its artifacts and traces.
     *
     * @param document - The document to switch to.
     */
    async switchDocuments(document: DocumentSchema): Promise<void> {
      const currentArtifactIds = document.artifactIds;

      this.currentDocument = document;
      artifactStore.initializeArtifacts({ currentArtifactIds });
      traceStore.initializeTraces({ currentArtifactIds });
      layoutStore.updatePositions(document.layout);
    },
    /**
     * Adds a new document.
     *
     * @param document - The document to add.
     */
    async addDocument(document: DocumentSchema): Promise<void> {
      this.allDocuments = [...this.allDocuments, document];

      await this.switchDocuments(document);
    },
    /**
     * Creates and adds a new document based on the neighborhood of an artifact.
     *
     * @param artifact - The artifact to display the neighborhood of.
     */
    async addDocumentOfNeighborhood(
      artifact: Pick<ArtifactSchema, "name" | "id">
    ): Promise<void> {
      const { neighbors } = subtreeStore.subtreeMap[artifact.id];
      const artifactIds = artifactStore.allArtifacts
        .filter(
          ({ id, type }) =>
            (artifact.id === id || neighbors.includes(id)) &&
            !selectionStore.ignoreTypes.includes(type)
        )
        .map(({ id }) => id);

      const document = buildDocument({
        project: projectStore.projectIdentifier,
        name: artifact.name,
        artifactIds,
      });

      await this.removeDocument("");
      await this.addDocument(document);
      layoutStore.mode = "tree";
    },
    /**
     * Creates and adds a new document for multiple types of artifacts.
     *
     * @param types - The artifact types to include in the document.
     */
    async addDocumentOfTypes(types: string[]): Promise<void> {
      const artifactsByType = artifactStore.allArtifactsByType;
      const document = buildDocument({
        project: projectStore.projectIdentifier,
        name: types.join(", "),
        artifactIds: types
          .map((type) => artifactsByType[type].map(({ id }) => id))
          .reduce((acc, cur) => [...acc, ...cur], []),
      });

      await this.removeDocument("");
      await this.addDocument(document);
      layoutStore.mode = types.length > 1 ? "tree" : "table";
    },
    /**
     * Adds artifacts to the current document.
     *
     * @param newIds - The new artifacts to add.
     */
    addDocumentArtifacts(newIds: string[]): void {
      this.currentDocument.artifactIds = [
        ...this.currentDocument.artifactIds.filter(
          (id) => !newIds.includes(id)
        ),
        ...newIds,
      ];
    },
    /**
     * Removes an existing document.
     *
     * @param document - The document, or document id, to delete.
     */
    async removeDocument(document: string | DocumentSchema): Promise<void> {
      const deleteDocumentId =
        typeof document === "string" ? document : document.documentId;

      const remainingDocuments = this.allDocuments.filter(
        ({ documentId }) => documentId !== deleteDocumentId
      );

      this.allDocuments = remainingDocuments;

      if (this.currentDocument.documentId !== deleteDocumentId) return;

      await this.switchDocuments(remainingDocuments[0] || this.baseDocument);
    },
    /**
     * Returns whether the given document name already exists.
     *
     * @param name - The name to search for.
     * @return Whether the name exists.
     */
    doesDocumentExist(name: string): boolean {
      return !!this.projectDocuments.find((document) => document.name === name);
    },
  },
});

export default useDocuments(pinia);

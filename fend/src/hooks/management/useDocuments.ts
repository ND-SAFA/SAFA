import { defineStore } from "pinia";
import {
  LayoutPositionsSchema,
  ViewSchema,
  ViewType,
  ProjectSchema,
} from "@/types";
import { buildDocument, DEFAULT_VIEW_NAME, removeMatches } from "@/util";
import {
  subtreeStore,
  layoutStore,
  traceStore,
  artifactStore,
  selectionStore,
} from "@/hooks";
import { QueryParams, updateParam } from "@/router";
import { pinia } from "@/plugins";

/**
 * This module keeps track of the different document views for a project.
 */
export const useDocuments = defineStore("documents", {
  state() {
    const baseDocument = buildDocument();

    return {
      /** The base document with all artifacts. */
      baseDocument,
      /** The currently visible document. */
      currentDocument: baseDocument,
      /** All custom project documents. */
      allDocuments: [baseDocument],
      /** The history of documents visited. */
      history: [] as ViewSchema[],
      /** The current index in the history. */
      historyIndex: 0,
    };
  },
  getters: {
    /**
     * @return All custom documents & the base document.
     */
    projectDocuments(): ViewSchema[] {
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
    currentType(): ViewType {
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
      return this.currentDocument.name === DEFAULT_VIEW_NAME;
    },
    /**
     * @return Whether there is a next document in the history.
     */
    hasNextHistory(): boolean {
      return this.historyIndex < this.history.length - 1;
    },
    /**
     * @return Whether there is a previous document in the history.
     */
    hasPreviousHistory(): boolean {
      return this.historyIndex > 0;
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
      layoutStore.updatePositions(
        loadedDocument.layout,
        currentArtifactIds.length
      );

      // In subsets of the base document, hide children of leaf nodes.
      if (this.isBaseDocument) return;

      subtreeStore.hideLeafSubtrees();
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

      layoutStore.updatePositions(layout, document.artifactIds.length);
    },
    /**
     * Updates the base document's layout, and reruns the layout if on the base document.
     * @param layout - The new layout to set.
     */
    updateBaseLayout(layout: LayoutPositionsSchema): void {
      this.baseDocument.layout = layout;

      if (!this.isBaseDocument) return;

      layoutStore.updatePositions(
        layout,
        this.currentDocument.artifactIds.length
      );
    },
    /**
     * Updates matching documents.
     * @param updatedDocuments - The updated documents.
     */
    async updateDocuments(updatedDocuments: ViewSchema[]): Promise<void> {
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
     * - The view is set to the TIM if the base graph is too large and the tree view is selected.
     * - In subsets of the base document, hides children of leaf nodes.
     * @param document - The document to switch to.
     */
    async switchDocuments(document: ViewSchema): Promise<void> {
      const currentArtifactIds = document.artifactIds;

      this.currentDocument = document;
      this.history.push(document);
      this.historyIndex = this.history.length - 1;
      subtreeStore.resetHiddenNodes();
      selectionStore.clearSelections({ onlySubtree: !document.documentId });
      artifactStore.initializeArtifacts({ currentArtifactIds });
      traceStore.initializeTraces({ currentArtifactIds });

      if (
        this.isBaseDocument &&
        artifactStore.largeNodeCount &&
        layoutStore.mode === "tree"
      ) {
        layoutStore.mode = "tim";
      }

      await layoutStore.updatePositions(
        document.layout,
        currentArtifactIds.length
      );

      await updateParam(
        QueryParams.VIEW,
        document.documentId || undefined,
        true
      );

      if (!this.isBaseDocument) {
        subtreeStore.hideLeafSubtrees();
      }
    },
    /**
     * Switches to the next or previous document in the history.
     * - Clears current selections and hidden nodes, as these are not saved between versions.
     * @param method - Whether to go forward or backward between documents.
     */
    switchDocumentHistory(method: "next" | "previous"): void {
      const documentIndex =
        method === "next" ? this.historyIndex + 1 : this.historyIndex - 1;
      const document = this.history[documentIndex];
      const currentArtifactIds = document?.artifactIds || [];

      if (!document) return;

      this.currentDocument = document;
      this.historyIndex = documentIndex;
      selectionStore.clearSelections();
      subtreeStore.resetHiddenNodes();
      artifactStore.initializeArtifacts({ currentArtifactIds });
      traceStore.initializeTraces({ currentArtifactIds });
      layoutStore.updatePositions(document.layout, currentArtifactIds.length);
    },
    /**
     * Adds a new document.
     * @param document - The document to add.
     */
    async addDocument(document: ViewSchema): Promise<void> {
      this.allDocuments = removeMatches(this.allDocuments, "documentId", [
        document.documentId,
      ]).concat(document);
      await this.switchDocuments(document);
    },
    /**
     * Adds artifacts to the current document.
     * @param newIds - The new artifacts to add.
     */
    addDocumentArtifacts(newIds: string[]): void {
      this.currentDocument.artifactIds = Array.from(
        new Set([...this.currentDocument.artifactIds, ...newIds])
      );
    },
    /**
     * Removes an existing document.
     * - If the document is the current document, the first document will be switched to.
     * @param document - The document, or document id, to delete.
     */
    async removeDocument(document: string | ViewSchema): Promise<void> {
      const deleteDocumentId =
        typeof document === "string" ? document : document.documentId;
      this.allDocuments = this.allDocuments.filter(
        ({ documentId }) => documentId !== deleteDocumentId
      );

      if (this.currentDocument.documentId !== deleteDocumentId) return;

      await this.switchDocuments(this.allDocuments[0] || this.baseDocument);
    },
    /**
     * Returns whether the given document name already exists.
     * @param name - The name to search for.
     * @return Whether the name exists.
     */
    doesDocumentExist(name: string): boolean {
      return !!this.projectDocuments.find((document) => document.name === name);
    },
    /**
     * Returns a document by its id.
     * @param id - The document id to search for.
     * @return The document, if one exists.
     */
    getDocument(id: string): ViewSchema | undefined {
      return this.projectDocuments.find(({ documentId }) => documentId === id);
    },
  },
});

export default useDocuments(pinia);

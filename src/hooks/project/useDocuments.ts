import { defineStore } from "pinia";

import { pinia } from "@/plugins";
import {
  ColumnModel,
  DocumentModel,
  DocumentType,
  ProjectModel,
} from "@/types";
import { createDocument, isTableDocument, removeMatches } from "@/util";
import { documentStore } from "@/hooks";
import layoutStore from "../graph/useLayout";
import projectStore from "./useProject";
import traceStore from "./useTraces";
import artifactStore from "./useArtifacts";

/**
 * This module keeps track of the different document views for a project.
 */
export const useDocuments = defineStore("documents", {
  state() {
    const baseDocument = createDocument();

    return {
      /**
       * Whether the document is currently in table view.
       */
      isTableView: false,
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
    projectDocuments(): DocumentModel[] {
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
     * @return Whether the current document type is for editing a table.
     */
    isEditableTableDocument(): boolean {
      return isTableDocument(this.currentDocument.type);
    },
    /**
     * @return Whether the current document type is for rendering a table.
     */
    isTableDocument(): boolean {
      return this.isTableView || this.isEditableTableDocument;
    },
    /**
     * @returns The column definitions for a table document.
     */
    tableColumns(): ColumnModel[] {
      return (this.isTableDocument && this.currentDocument.columns) || [];
    },
  },
  actions: {
    /**
     * Initializes the current artifacts and traces visible in the current document.
     */
    initializeProject(project: ProjectModel): void {
      const {
        artifacts,
        traces,
        currentDocumentId = this.currentDocument.documentId,
        documents = [],
        layout,
      } = project;

      const defaultDocument = createDocument({
        name: "Default",
        project,
        artifactIds: artifacts.map(({ id }) => id),
      });

      const loadedDocument =
        documents.find(({ documentId }) => documentId === currentDocumentId) ||
        defaultDocument;
      const currentArtifactIds = loadedDocument.artifactIds;

      this.$patch({
        allDocuments: documents,
        baseDocument: defaultDocument,
        currentDocument: loadedDocument,
      });

      artifactStore.initializeArtifacts({ artifacts, currentArtifactIds });
      traceStore.initializeTraces({ traces, currentArtifactIds });
      layoutStore.updatePositions(
        loadedDocument.documentId ? loadedDocument.layout : layout
      );
    },
    /**
     * Updates matching documents.
     *
     * @param updatedDocuments - The updated documents.
     */
    async updateDocuments(updatedDocuments: DocumentModel[]): Promise<void> {
      const updatedIds = updatedDocuments.map((d) => d.documentId);
      const currentDocument = updatedDocuments.find(
        ({ documentId }) => documentId === this.currentId
      );

      if (currentDocument) {
        await documentStore.switchDocuments(currentDocument);
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
    async switchDocuments(document: DocumentModel): Promise<void> {
      const currentArtifactIds = document.artifactIds;

      this.currentDocument = document;
      artifactStore.initializeArtifacts({ currentArtifactIds });
      traceStore.initializeTraces({ currentArtifactIds });

      if (document.documentId !== "") {
        layoutStore.updatePositions(document.layout);
      } else {
        layoutStore.updatePositions(projectStore.project.layout);
      }
    },
    /**
     * Adds a new document.
     *
     * @param document - The document to add.
     */
    async addDocument(document: DocumentModel): Promise<void> {
      this.allDocuments = [...this.allDocuments, document];

      await this.switchDocuments(document);
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
    async removeDocument(document: string | DocumentModel): Promise<void> {
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
     * Toggles whether the current document is in table view.
     */
    toggleTableView(): void {
      this.isTableView = !this.isTableView;
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
    /**
     * Returns whether the given column name already exists.
     *
     * @param name - The name to search for.
     * @return Whether the name exists.
     */
    doesColumnExist(name: string): boolean {
      return !!this.tableColumns.find((column) => column.name === name);
    },
  },
});

export default useDocuments(pinia);

import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";

import type { ColumnModel, ProjectModel, DocumentModel } from "@/types";
import { DocumentType } from "@/types";
import { createDocument, isTableDocument } from "@/util";
import { artifactModule, layoutModule, traceModule } from "@/store";
import { handleResetGraph, handleUpdateCurrentDocument } from "@/api";

@Module({ namespaced: true, name: "document" })
/**
 * This module defines the state of the currently visible document within a project.
 */
export default class DocumentModule extends VuexModule {
  /**
   * Whether the document is currently in table view.
   */
  private isTableView = false;
  /**
   * The currently visible document.
   */
  private currentDocument: DocumentModel = createDocument();
  /**
   * The base document with all artifacts.
   */
  private baseDocument: DocumentModel = createDocument();
  /**
   * All project documents.
   */
  private allDocuments: DocumentModel[] = [this.currentDocument];

  @Action
  /**
   * Initializes the current artifacts and traces visible in the current document.
   */
  initializeProject(project: ProjectModel): void {
    const {
      artifacts,
      traces,
      currentDocumentId = this.currentDocument.documentId,
      documents = [],
    } = project;

    const defaultDocument = createDocument({
      project,
      artifactIds: artifacts.map(({ id }) => id),
    });

    const loadedDocument = documents.find(
      ({ documentId }) => documentId === currentDocumentId
    );

    this.SET_ALL_DOCUMENTS(documents);
    this.SET_BASE_DOCUMENT(defaultDocument);

    if (loadedDocument) {
      const currentArtifactIds = loadedDocument.artifactIds;

      this.SET_CURRENT_DOCUMENT(loadedDocument);
      artifactModule.initializeArtifacts({ artifacts, currentArtifactIds });
      traceModule.initializeTraces({ traces, currentArtifactIds });
    } else {
      this.SET_CURRENT_DOCUMENT(defaultDocument);
      artifactModule.initializeArtifacts({ artifacts });
      traceModule.initializeTraces({ traces });
    }
  }

  @Action
  /**
   * Updates documents in store matching the documentIds of those given.
   *
   * @param updatedDocuments - The updated documents.
   */
  async updateDocuments(updatedDocuments: DocumentModel[]): Promise<void> {
    const updatedDocumentIds: string[] = updatedDocuments.map(
      (d) => d.documentId
    );
    const newDocuments = [
      ...this.allDocuments.filter(
        ({ documentId }) => !updatedDocumentIds.includes(documentId)
      ),
      ...updatedDocuments,
    ];
    this.SET_ALL_DOCUMENTS(newDocuments);

    if (updatedDocumentIds.includes(this.currentDocument.documentId)) {
      const updatedCurrentDocument: DocumentModel = updatedDocuments.filter(
        ({ documentId }) => documentId === this.currentDocument.documentId
      )[0];
      this.SET_CURRENT_DOCUMENT(updatedCurrentDocument);
    }
  }

  @Action
  /**
   * Sets the current document and initializes its artifacts and traces.
   */
  async switchDocuments(document: DocumentModel): Promise<void> {
    const currentArtifactIds = document.artifactIds;

    this.SET_CURRENT_DOCUMENT(document);
    await handleUpdateCurrentDocument(document);
    artifactModule.initializeArtifacts({ currentArtifactIds });
    traceModule.initializeTraces({ currentArtifactIds });
    await layoutModule.updateLayout();
    await handleResetGraph();
  }

  @Action
  /**
   * Adds a new document.
   */
  async addDocument(document: DocumentModel): Promise<void> {
    this.SET_ALL_DOCUMENTS([...this.allDocuments, document]);

    await this.switchDocuments(document);
  }

  @Action
  /**
   * Removes an existing document.
   */
  async removeDocument(document: DocumentModel): Promise<void> {
    const remainingDocuments = this.allDocuments.filter(
      ({ documentId }) => documentId !== document.documentId
    );

    this.SET_ALL_DOCUMENTS(remainingDocuments);

    if (this.currentDocument.documentId === document.documentId) {
      await this.switchDocuments(remainingDocuments[0] || this.baseDocument);
    }
  }

  @Action
  /**
   * Toggles whether the current document is in table view.
   */
  toggleTableView(): void {
    this.SET_TABLE_VIEW(!this.isTableView);
  }

  @Mutation
  /**
   * Sets the current document.
   */
  SET_ALL_DOCUMENTS(documents: DocumentModel[]): void {
    this.allDocuments = documents;
  }

  @Mutation
  /**
   * Sets the current document.
   */
  SET_CURRENT_DOCUMENT(document: DocumentModel): void {
    this.currentDocument = document;
  }

  @Mutation
  /**
   * Sets the current document.
   */
  SET_BASE_DOCUMENT(document: DocumentModel): void {
    this.baseDocument = document;
  }

  @Mutation
  /**
   * Sets whether the document is in table view.
   */
  SET_TABLE_VIEW(isTableView: boolean): void {
    this.isTableView = isTableView;
  }

  /**
   * @return The current document.
   */
  get projectDocuments(): DocumentModel[] {
    return [...this.allDocuments, this.baseDocument];
  }

  /**
   * @return The current document.
   */
  get document(): DocumentModel {
    return this.currentDocument;
  }

  /**
   * @return The current document.
   */
  get type(): DocumentType {
    return this.currentDocument.type;
  }

  /**
   * @return The default document.
   */
  get defaultDocument(): DocumentModel {
    return this.baseDocument;
  }

  /**
   * Returns whether the given document name already exists.
   */
  get doesDocumentExist(): (name: string) => boolean {
    return (newName) => {
      return !!this.projectDocuments.find(({ name }) => name === newName);
    };
  }

  /**
   * Returns whether the current document type is for editing a table.
   */
  get isEditableTableDocument(): boolean {
    return isTableDocument(this.currentDocument.type);
  }

  /**
   * Returns whether the current document type is for rendering a table.
   */
  get isTableDocument(): boolean {
    return this.isTableView || this.isEditableTableDocument;
  }

  /**
   * Returns the column definitions for a table document.
   */
  get tableColumns(): ColumnModel[] {
    return (this.isTableDocument && this.currentDocument.columns) || [];
  }

  /**
   * Returns whether the given column name already exists.
   */
  get doesColumnExist(): (name: string) => boolean {
    return (newName) => {
      return !!this.tableColumns.find(({ name }) => name === newName);
    };
  }
}

import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";

import type { DocumentColumn, Project, ProjectDocument } from "@/types";
import { ColumnDataType, DocumentType } from "@/types";
import { createDocument, isTableDocument } from "@/util";
import { appModule, artifactModule, traceModule } from "@/store";
import { resetGraphFocus } from "@/api";

@Module({ namespaced: true, name: "document" })
/**
 * This module defines the state of the currently visible document within a project.
 */
export default class DocumentModule extends VuexModule {
  /**
   * The currently visible document.
   */
  private currentDocument: ProjectDocument = createDocument();
  /**
   * The base document with all artifacts.
   */
  private baseDocument: ProjectDocument = createDocument();
  /**
   * All project documents.
   */
  private allDocuments: ProjectDocument[] = [this.currentDocument];

  @Action
  /**
   * Initializes the current artifacts and traces visible in the current document.
   */
  initializeProject(project: Project): void {
    const {
      artifacts,
      traces,
      currentDocumentId = "",
      documents = [],
    } = project;

    const defaultDocument = createDocument(
      project,
      artifacts.map(({ id }) => id)
    );

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
   * Reloads the artifact ids for all existing documents.
   *
   * @param updatedDocuments - The updated documents.
   */
  async updateDocuments(updatedDocuments: ProjectDocument[]): Promise<void> {
    this.allDocuments.forEach((storedDocument) => {
      const updatedDocument = updatedDocuments.find(
        ({ documentId }) => documentId === storedDocument.documentId
      );

      if (!updatedDocument) return;

      storedDocument.artifactIds = updatedDocument.artifactIds;
    });
  }

  @Action
  /**
   * Sets the current document and initializes its artifacts and traces.
   */
  async switchDocuments(document: ProjectDocument): Promise<void> {
    const currentArtifactIds = document.artifactIds;

    appModule.onLoadStart();

    this.SET_CURRENT_DOCUMENT(document);
    artifactModule.initializeArtifacts({ currentArtifactIds });
    traceModule.initializeTraces({ currentArtifactIds });
    await resetGraphFocus();

    setTimeout(appModule.onLoadEnd, 200);
  }

  @Action
  /**
   * Adds a new document.
   */
  async addDocument(document: ProjectDocument): Promise<void> {
    this.SET_ALL_DOCUMENTS([...this.allDocuments, document]);

    await this.switchDocuments(document);
  }

  @Action
  /**
   * Removes an existing document.
   */
  async removeDocument(document: ProjectDocument): Promise<void> {
    const remainingDocuments = this.allDocuments.filter(
      ({ documentId }) => documentId !== document.documentId
    );

    this.SET_ALL_DOCUMENTS(remainingDocuments);

    if (this.currentDocument.documentId === document.documentId) {
      await this.switchDocuments(remainingDocuments[0] || this.baseDocument);
    }
  }

  @Mutation
  /**
   * Sets the current document.
   */
  SET_ALL_DOCUMENTS(documents: ProjectDocument[]): void {
    this.allDocuments = documents;
  }

  @Mutation
  /**
   * Sets the current document.
   */
  SET_CURRENT_DOCUMENT(document: ProjectDocument): void {
    this.currentDocument = document;
  }

  @Mutation
  /**
   * Sets the current document.
   */
  SET_BASE_DOCUMENT(document: ProjectDocument): void {
    this.baseDocument = document;
  }

  /**
   * @return The current document.
   */
  get projectDocuments(): ProjectDocument[] {
    return [...this.allDocuments, this.baseDocument];
  }

  /**
   * @return The current document.
   */
  get document(): ProjectDocument {
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
  get defaultDocument(): ProjectDocument {
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
   * Returns whether the current document type is for rendering a table.
   * TODO: remove value override.
   */
  get isTableDocument(): boolean {
    return isTableDocument(this.currentDocument.type) || true;
  }

  /**
   * Returns the column definitions for a table document.
   * TODO: remove value override.
   */
  get tableColumns(): DocumentColumn[] {
    return this.isTableDocument
      ? this.currentDocument.columns || [
          {
            id: "1",
            name: "Text",
            dataType: ColumnDataType.FREE_TEXT,
          },
          {
            id: "2",
            name: "Relation",
            dataType: ColumnDataType.RELATION,
          },
          {
            id: "3",
            name: "Select",
            dataType: ColumnDataType.SELECT,
          },
        ]
      : [];
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

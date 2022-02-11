import { Module, VuexModule, Mutation, Action } from "vuex-module-decorators";

import type { Project, ProjectDocument } from "@/types";
import { createDocument } from "@/util";
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

    this.SET_ALL_DOCUMENTS([...documents, defaultDocument]);

    if (loadedDocument) {
      const currentArtifactIds = loadedDocument.artifactIds;

      this.SET_DOCUMENT(loadedDocument);
      artifactModule.initializeArtifacts({ artifacts, currentArtifactIds });
      traceModule.initializeTraces({ traces, currentArtifactIds });
    } else {
      this.SET_DOCUMENT(defaultDocument);
      artifactModule.initializeArtifacts({ artifacts });
      traceModule.initializeTraces({ traces });
    }
  }

  @Action
  /**
   * Sets the current document and initializes its artifacts and traces.
   */
  async switchDocuments(document: ProjectDocument): Promise<void> {
    const currentArtifactIds = document.artifactIds;

    appModule.onLoadStart();

    this.SET_DOCUMENT(document);
    artifactModule.initializeArtifacts({ currentArtifactIds });
    traceModule.initializeTraces({ currentArtifactIds });
    await resetGraphFocus();

    setTimeout(appModule.onLoadEnd, 1000);
  }

  @Action
  /**
   * Adds a new document.
   */
  addDocument(document: ProjectDocument): void {
    this.SET_ALL_DOCUMENTS([...this.allDocuments, document]);
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
  SET_DOCUMENT(document: ProjectDocument): void {
    this.currentDocument = document;
  }

  /**
   * @return The current document.
   */
  get projectDocuments(): ProjectDocument[] {
    return this.allDocuments;
  }

  /**
   * @return The current document.
   */
  get document(): ProjectDocument {
    return this.currentDocument;
  }

  /**
   * Returns whether the given document name already exists.
   */
  get doesDocumentExist(): (name: string) => boolean {
    return (newName) => {
      return !!this.projectDocuments.find(({ name }) => name === newName);
    };
  }
}

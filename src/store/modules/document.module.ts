import { Module, VuexModule, Mutation, Action } from "vuex-module-decorators";

import type { Project, ProjectDocument } from "@/types";
import { createDocument } from "@/util";
import { artifactModule, traceModule } from "@/store";

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

    const defaultDocument = createDocument(artifacts.map(({ id }) => id));
    const loadedDocument = documents.find(
      ({ documentId }) => documentId === currentDocumentId
    );

    this.SET_ALL_DOCUMENTS([...documents, defaultDocument]);

    if (loadedDocument) {
      this.SET_DOCUMENT(loadedDocument);
      artifactModule.initializeArtifacts({
        artifacts,
        currentArtifactIds: loadedDocument.artifactIds,
      });
      traceModule.initializeTraces({
        traces,
        currentArtifactIds: loadedDocument.artifactIds,
      });
    } else {
      this.SET_DOCUMENT(defaultDocument);
      artifactModule.initializeArtifacts({ artifacts });
      traceModule.initializeTraces({ traces });
    }
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

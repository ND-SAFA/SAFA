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

  @Action
  /**
   * Initializes the current artifacts and traces visible in the current document.
   */
  initializeProject(project: Project): void {
    const {
      currentDocumentId = "",
      documents = [],
      artifacts,
      traces,
    } = project;

    const loadedDocument = documents.find(
      ({ documentId }) => documentId === currentDocumentId
    );

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
      this.SET_DOCUMENT(createDocument(artifacts.map(({ id }) => id)));
      artifactModule.initializeArtifacts({ artifacts });
      traceModule.initializeTraces({ traces });
    }
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
  get document(): ProjectDocument {
    return this.currentDocument;
  }
}

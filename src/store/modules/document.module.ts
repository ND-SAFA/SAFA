import { Module, VuexModule, Mutation, Action } from "vuex-module-decorators";

import type { Artifact, TraceLink, Project } from "@/types";
import { ProjectDocument } from "@/types";
import { createDocument } from "@/util";

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
   * The currently visible artifacts.
   */
  private currentArtifacts: Artifact[] = [];
  /**
   * The currently visible traces.
   */
  private currentTraces: TraceLink[] = [];

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
      const { artifactIds } = loadedDocument;

      this.SET_DOCUMENT(loadedDocument);
      this.SET_ARTIFACTS(
        artifacts.filter(({ id }) => artifactIds.includes(id))
      );
      this.SET_TRACES(
        traces.filter(
          ({ sourceId, targetId }) =>
            artifactIds.includes(sourceId) && artifactIds.includes(targetId)
        )
      );
    } else {
      this.SET_DOCUMENT(createDocument(artifacts.map(({ id }) => id)));
      this.SET_ARTIFACTS(artifacts);
      this.SET_TRACES(traces);
    }
  }

  @Mutation
  /**
   * Sets the current document.
   */
  SET_DOCUMENT(document: ProjectDocument): void {
    this.currentDocument = document;
  }

  @Mutation
  /**
   * Sets the current artifacts.
   */
  SET_ARTIFACTS(artifacts: Artifact[]): void {
    this.currentArtifacts = artifacts;
  }

  @Mutation
  /**
   * Sets the current trace links.
   */
  SET_TRACES(traces: TraceLink[]): void {
    this.currentTraces = traces;
  }

  /**
   * @return The current document.
   */
  get document(): ProjectDocument {
    return this.currentDocument;
  }

  /**
   * @return The artifacts for the current document.
   */
  get artifacts(): Artifact[] {
    return this.currentArtifacts;
  }

  /**
   * @return The trace links for the current document.
   */
  get traces(): TraceLink[] {
    return this.currentTraces;
  }
}

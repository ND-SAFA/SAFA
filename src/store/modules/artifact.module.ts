import { Module, VuexModule, Mutation, Action } from "vuex-module-decorators";

import type { Artifact, DocumentArtifacts } from "@/types";

@Module({ namespaced: true, name: "artifact" })
/**
 * This module defines the state of the currently visible artifacts.
 */
export default class ArtifactModule extends VuexModule {
  /**
   * All artifacts in the project.
   */
  private projectArtifacts: Artifact[] = [];
  /**
   * The currently visible artifacts.
   */
  private currentArtifacts: Artifact[] = [];

  @Action
  /**
   * Initializes the artifacts visible in the current document.
   */
  initializeArtifacts(documentArtifacts: DocumentArtifacts): void {
    const { artifacts, currentArtifactIds } = documentArtifacts;

    this.SET_PROJECT_ARTIFACTS(artifacts);
    this.SET_CURRENT_ARTIFACTS(
      currentArtifactIds
        ? artifacts.filter(({ id }) => currentArtifactIds.includes(id))
        : artifacts
    );
  }

  @Mutation
  /**
   * Sets the project artifacts.
   */
  SET_PROJECT_ARTIFACTS(artifacts: Artifact[]): void {
    this.projectArtifacts = artifacts;
  }

  @Mutation
  /**
   * Sets the current artifacts.
   */
  SET_CURRENT_ARTIFACTS(artifacts: Artifact[]): void {
    this.currentArtifacts = artifacts;
  }

  /**
   * @return All artifacts in the project.
   */
  get allArtifacts(): Artifact[] {
    return this.projectArtifacts;
  }

  /**
   * @return The artifacts for the current document.
   */
  get artifacts(): Artifact[] {
    return this.currentArtifacts;
  }
}

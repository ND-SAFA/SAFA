import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";
import type { ArtifactPositions, LayoutPosition } from "@/types";
import { documentModule, projectModule } from "@/store";

@Module({ namespaced: true, name: "layout" })
/**
 * This module defines the state of the current user session.
 */
export default class LayoutModule extends VuexModule {
  /**
   * A mapping from artifact ID to its position.
   */
  private artifactPositions: ArtifactPositions = {};

  @Action
  /**
   * Updates the current layout based on the current project and document.
   */
  async updateLayout(): Promise<void> {
    const document = documentModule.document;
    const project = projectModule.getProject;

    if (document.documentId !== "") {
      await this.SET_ARTIFACT_POSITIONS(document.layout);
    } else {
      await this.SET_ARTIFACT_POSITIONS(project.layout);
    }
  }

  @Mutation
  /**
   * Sets the stored positions of artifacts.
   * @param artifactPositions - The artifact positions.
   */
  SET_ARTIFACT_POSITIONS(artifactPositions: ArtifactPositions): void {
    this.artifactPositions = artifactPositions;
  }

  /**
   * Returns the position of an artifact.
   */
  get getArtifactPosition(): (artifactId: string) => LayoutPosition {
    return (artifactId: string) =>
      this.artifactPositions[artifactId] || { x: 0, y: 0 };
  }
}

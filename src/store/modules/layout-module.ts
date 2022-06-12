import { Module, Mutation, VuexModule } from "vuex-module-decorators";
import { ArtifactPositions, LayoutPosition } from "@/types";

@Module({ namespaced: true, name: "layout" })
/**
 * This module defines the state of the current user session.
 */
export default class LayoutModule extends VuexModule {
  private artifactPositions: ArtifactPositions = {};

  @Mutation
  SET_ARTIFACT_POSITIONS(artifactPositions: ArtifactPositions): void {
    this.artifactPositions = artifactPositions;
  }

  get getArtifactPosition(): (aId: string) => LayoutPosition {
    return (artifactId: string) => this.artifactPositions[artifactId];
  }
}

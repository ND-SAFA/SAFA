import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";

import type { ArtifactTypeDirections, Project } from "@/types";
import { ArtifactDirection } from "@/types";
import { logModule, projectModule } from "@/store";

@Module({ namespaced: true, name: "linkDirections" })
/**
 * This module tracks the directions of links between artifacts that are allowed.
 */
export default class LinkDirectionsModule extends VuexModule {
  /**
   * A mapping of the allowed directions of links between artifacts.
   */
  private artifactTypeDirections: ArtifactTypeDirections = {};

  @Action
  /**
   * Updates what directions of trace links between artifacts are allowed.
   */
  setLinkDirections(project: Project): void {
    const allowedDirections: ArtifactTypeDirections = {};

    // Ensure that all artifact types appear in mapping.
    project.artifacts.forEach((artifact) => {
      allowedDirections[artifact.type] = [];
    });

    project.traces.forEach(({ sourceId, targetId }) => {
      try {
        const sourceType = projectModule.getArtifactById(sourceId).type;
        const targetType = projectModule.getArtifactById(targetId).type;

        if (!allowedDirections[sourceType].includes(targetType)) {
          allowedDirections[sourceType].push(targetType);
        }
      } catch (e) {
        logModule.onDevMessage(
          `Unable to calculate allowed trace directions: ${e}`
        );
      }
    });

    this.SET_LINK_DIRECTIONS(allowedDirections);
  }

  @Action
  /**
   * Changes what directions of trace links between artifacts are allowed.
   */
  updateLinkDirections({ type, allowedTypes }: ArtifactDirection): void {
    this.SET_LINK_DIRECTIONS({
      ...this.artifactTypeDirections,
      [type]: allowedTypes,
    });
  }

  @Mutation
  /**
   * Sets a new collection of allowed directions between artifact types.
   *
   * @param artifactTypeDirections - Directions between artifact types to allow.
   */
  SET_LINK_DIRECTIONS(artifactTypeDirections: ArtifactTypeDirections): void {
    this.artifactTypeDirections = artifactTypeDirections;
  }

  /**
   * Return the allowed directions of traces between artifacts.
   */
  get linkDirections(): ArtifactTypeDirections {
    return this.artifactTypeDirections;
  }

  /**
   * Returns all types of artifacts.
   */
  get artifactTypes(): string[] {
    return Object.keys(this.linkDirections);
  }

  /**
   * @return A function for determining if the trace link is allowed based on the type of the nodes.
   */
  get isLinkAllowedByType(): (
    sourceType: string,
    targetType: string
  ) => boolean {
    return (sourceType, targetType) => {
      return this.artifactTypeDirections[sourceType]?.includes(targetType);
    };
  }
}

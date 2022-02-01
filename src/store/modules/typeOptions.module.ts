import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";

import type { ArtifactTypeDirections, LabeledArtifactDirection } from "@/types";
import { ArtifactDirection, ArtifactTypeIcons } from "@/types";
import { createDefaultTypeIcons } from "@/util";

@Module({ namespaced: true, name: "typeOptions" })
/**
 * This module tracks the directions of links between artifacts that are allowed, and the icons for each type.
 */
export default class TypeOptionsModule extends VuexModule {
  /**
   * A mapping of the allowed directions of links between artifacts.
   */
  private artifactTypeDirections: ArtifactTypeDirections = {};
  /**
   * A mapping of the icons for each artifact type.
   */
  private artifactTypeIcons: ArtifactTypeIcons = createDefaultTypeIcons();

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

  @Action
  /**
   * Changes what icons each artifact uses.
   */
  updateArtifactIcon({ type, icon }: LabeledArtifactDirection): void {
    this.SET_TYPE_ICONS({
      ...this.artifactTypeIcons,
      [type]: icon,
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

  @Mutation
  /**
   * Sets a new collection of artifact type icons.
   *
   * @param artifactTypeIcons - The icons for each artifact type.
   */
  SET_TYPE_ICONS(artifactTypeIcons: ArtifactTypeIcons): void {
    this.artifactTypeIcons = artifactTypeIcons;
  }

  /**
   * @returns The allowed directions of traces between artifacts.
   */
  get linkDirections(): ArtifactTypeDirections {
    return this.artifactTypeDirections;
  }

  /**
   * @returns all types of artifacts.
   */
  get artifactTypes(): string[] {
    return Object.keys(this.linkDirections);
  }

  /**
   * @returns A function for determining if the trace link is allowed based on the type of the nodes.
   */
  get isLinkAllowedByType(): (
    sourceType: string,
    targetType: string
  ) => boolean {
    return (sourceType, targetType) => {
      return !this.artifactTypeDirections[targetType]?.includes(sourceType);
    };
  }

  /**
   * @returns All possible artifact type icons.
   */
  get allArtifactTypeIcons(): string[] {
    return Object.values(createDefaultTypeIcons());
  }

  /**
   * @returns The icon name for the given artifact type
   */
  get getArtifactTypeIcon(): (type: string) => string {
    return (type) =>
      this.artifactTypeIcons[type.toLowerCase()] ||
      this.artifactTypeIcons.default;
  }
}

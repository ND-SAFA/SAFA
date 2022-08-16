import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";

import type {
  ArtifactTypeModel,
  ArtifactTypeDirections,
  LabelledTraceDirectionModel,
  TraceDirectionModel,
  ArtifactTypeIcons,
} from "@/types";
import { createDefaultTypeIcons, getArtifactTypePrintName } from "@/util";
import {
  allowedSafetyCaseTypes,
  ArtifactModel,
  CreateLinkValidator,
  SafetyCaseType,
} from "@/types";
import { typeOptionsModule } from "@/store";

@Module({ namespaced: true, name: "typeOptions" })
/**
 * This module tracks the directions of links between artifacts that are
 * allowed, and the icons for each type.
 */
export default class TypeOptionsModule extends VuexModule {
  /**
   * A mapping of the allowed directions of links between artifacts.
   */
  private artifactTypeDirections: ArtifactTypeDirections = {};
  /**
   * A list of all artifact types.
   */
  private allArtifactTypes: ArtifactTypeModel[] = [];
  /**
   * A mapping of the icons for each artifact type.
   */
  private artifactTypeIcons: ArtifactTypeIcons = createDefaultTypeIcons([]);

  @Action
  /**
   * Clears all store data.
   */
  clearData(): void {
    this.SET_LINK_DIRECTIONS({});
    this.SET_TYPE_ICONS(createDefaultTypeIcons([]));
    this.SET_TYPES([]);
  }

  @Action
  /**
   * Changes what directions of trace links between artifacts are allowed.
   */
  initializeTypeIcons(artifactTypes: ArtifactTypeModel[]): void {
    this.SET_TYPE_ICONS(createDefaultTypeIcons(artifactTypes));
    this.SET_TYPES(artifactTypes);
  }

  @Action
  /**
   * Changes what directions of trace links between artifacts are allowed.
   */
  updateLinkDirections({ type, allowedTypes }: TraceDirectionModel): void {
    this.SET_LINK_DIRECTIONS({
      ...this.artifactTypeDirections,
      [type]: allowedTypes,
    });
  }

  @Action
  /**
   * Changes what icons each artifact uses.
   */
  updateArtifactIcon({ type, icon }: LabelledTraceDirectionModel): void {
    this.SET_TYPE_ICONS({
      ...this.artifactTypeIcons,
      [type]: icon,
    });
  }

  @Action
  /**
   * Adds a new artifact type if it does not yet exist.
   */
  addArtifactTypes(newArtifacts: ArtifactModel[]): void {
    newArtifacts.forEach(({ type }) => {
      if (this.artifactTypeDirections[type]) return;

      this.SET_TYPE_ICONS({
        ...this.artifactTypeIcons,
        [type]: "mdi-help",
      });
      this.SET_LINK_DIRECTIONS({
        ...this.artifactTypeDirections,
        [type]: [],
      });
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
   * Sets the artifact types.
   *
   * @param artifactTypes - The artifact types.
   */
  SET_TYPES(artifactTypes: ArtifactTypeModel[]): void {
    this.allArtifactTypes = artifactTypes;
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
    const safetyCaseTypes = Object.values(SafetyCaseType) as string[];

    return Object.keys(this.linkDirections).filter(
      (type) => !safetyCaseTypes.includes(type)
    );
  }

  /**
   * @returns A function for determining if the trace link is allowed based on the type of the nodes.
   */
  get isLinkAllowedByType(): CreateLinkValidator {
    return (source, target) => {
      const sourceType =
        "artifactType" in source ? source.artifactType : source.type;
      const targetType =
        "artifactType" in target ? target.artifactType : target.type;
      const isSourceDefaultArtifact =
        !source.safetyCaseType && !source.logicType;
      const isTargetDefaultArtifact =
        !target.safetyCaseType && !target.logicType;

      if (isSourceDefaultArtifact) {
        return !this.artifactTypeDirections[targetType]?.includes(sourceType);
      } else if (source.safetyCaseType) {
        if (isTargetDefaultArtifact) return true;
        if (target.logicType || !target.safetyCaseType) return false;

        return allowedSafetyCaseTypes[source.safetyCaseType].includes(
          target.safetyCaseType
        );
      } else if (source.logicType) {
        return isTargetDefaultArtifact;
      }

      return false;
    };
  }

  /**
   * @returns All possible artifact type icons.
   */
  get allArtifactTypeIcons(): string[] {
    return [
      "mdi-clipboard-text",
      "mdi-math-compass",
      "mdi-hazard-lights",
      "mdi-pine-tree-fire",
      "mdi-alpha-a-box-outline",
    ];
  }

  /**
   * @returns The icon name for the given artifact type
   */
  get getArtifactTypeIcon(): (type: string) => string {
    return (type) =>
      this.artifactTypeIcons[type] || this.artifactTypeIcons.default;
  }

  /**
   * @return Labeled artifact type directions.
   */
  get labeledTypeDirections(): () => LabelledTraceDirectionModel[] {
    return () =>
      Object.entries(this.linkDirections).map(([type, allowedTypes]) => {
        const icon = this.getArtifactTypeIcon(type);

        return {
          type,
          allowedTypes,
          label: getArtifactTypePrintName(type),
          icon,
          iconIndex: this.allArtifactTypeIcons.indexOf(icon),
        };
      });
  }
}

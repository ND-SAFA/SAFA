import { defineStore } from "pinia";

import {
  ArtifactCytoElementData,
  ArtifactSchema,
  ArtifactTypeDirections,
  ArtifactTypeSchema,
  ProjectSchema,
  SafetyCaseType,
  TimArtifactLevelSchema,
  TimTraceMatrixSchema,
} from "@/types";
import {
  allTypeIcons,
  createTIM,
  defaultTypeIcon,
  isLinkAllowedByType,
  preserveObjectKeys,
  removeMatches,
} from "@/util";
import { pinia } from "@/plugins";
import projectStore from "@/hooks/project/useProject";

/**
 * This module tracks the directions of links between artifacts that are
 * allowed, and the icons for each type.
 */
export const useTypeOptions = defineStore("typeOptions", {
  state: () => ({
    /**
     * A list of all artifact types.
     */
    allArtifactTypes: [] as ArtifactTypeSchema[],
    /**
     * Internal details stored for each artifact type and type matrix.
     */
    tim: createTIM(),
  }),
  getters: {
    /**
     * @return All levels of artifacts.
     */
    artifactLevels(): TimArtifactLevelSchema[] {
      return Object.values(this.tim.artifacts);
    },
    /**
     * @returns all types of artifacts.
     */
    artifactTypes(): string[] {
      const safetyCaseTypes = Object.values(SafetyCaseType) as string[];

      return Object.values(this.tim.artifacts)
        .map(({ name }) => name)
        .filter((name) => !safetyCaseTypes.includes(name));
    },
  },
  actions: {
    /**
     *Initializes project data.
     *
     * @param project - The project to load.
     */
    initializeProject(project: ProjectSchema): void {
      this.tim = createTIM(project);
      this.allArtifactTypes = project.artifactTypes;
      this.initializeTypeIcons(project.artifactTypes);
    },
    /**
     * Initializes the icons for artifact types.
     *
     * @param allArtifactTypes - The artifact types to set.
     */
    initializeTypeIcons(allArtifactTypes: ArtifactTypeSchema[]): void {
      allArtifactTypes.forEach((artifactType) => {
        const icon = artifactType.icon.replace("mdi-help", defaultTypeIcon);
        this.tim.artifacts[artifactType.name] = {
          ...this.tim.artifacts[artifactType.name],
          icon,
          iconIndex: allTypeIcons.indexOf(icon),
        };
      });
    },
    /**
     * Changes what directions of trace links between artifacts are allowed.
     *
     * @param directions - The artifact types to set.
     */
    initializeTypeDirections(directions: ArtifactTypeDirections): void {
      Object.entries(directions).forEach(([type, allowedTypes]) => {
        this.tim.artifacts[type] = {
          ...this.tim.artifacts[type],
          allowedTypes,
        };
      });
    },
    /**
     * Changes what directions of trace links between artifacts are allowed.
     *
     * @param type - The type to update.
     * @param allowedTypes - The allowed types to set.
     */
    updateLinkDirections({ name, allowedTypes }: TimArtifactLevelSchema): void {
      this.tim.artifacts[name] = {
        ...this.tim.artifacts[name],
        allowedTypes,
      };
    },
    /**
     * Changes what icons each artifact uses.
     *
     * @param type - The type to update.
     * @param icon - The icon to set.
     */
    updateArtifactIcon({ name, icon }: TimArtifactLevelSchema): void {
      this.tim.artifacts[name] = {
        ...this.tim.artifacts[name],
        icon,
        iconIndex: allTypeIcons.indexOf(icon),
      };
    },
    /**
     * Adds a new artifact types.
     *
     * @param artifactTypes - The artifact types to add.
     */
    addOrUpdateArtifactTypes(artifactTypes: ArtifactTypeSchema[]): void {
      const ids = artifactTypes.map(({ name }) => name);
      const allArtifactTypes = [
        ...removeMatches(this.allArtifactTypes, "name", ids),
        ...artifactTypes,
      ];

      this.initializeTypeIcons(artifactTypes);
      projectStore.updateProject({ artifactTypes: allArtifactTypes });
    },
    /**
     * Adds a new artifact type if it does not yet exist.
     *
     * @param newArtifacts - The artifact to add types from.
     */
    addTypesFromArtifacts(newArtifacts: ArtifactSchema[]): void {
      newArtifacts.forEach(({ type }) => {
        if (this.tim.artifacts[type]) return;

        this.tim.artifacts[type] = {
          ...this.tim.artifacts[type],
          icon: defaultTypeIcon,
          allowedTypes: [],
        };
      });
    },
    /**
     * Removes artifact types.
     *
     * @param removedTypeIds - The artifact type ids to remove.
     */
    removeArtifactTypes(removedTypeIds: string[]): void {
      const preservedTypes = removeMatches(
        this.allArtifactTypes,
        "typeId",
        removedTypeIds
      );
      const names = preservedTypes.map(({ name }) => name);
      const preservedLevels = preserveObjectKeys(this.tim.artifacts, names);

      this.$patch({
        allArtifactTypes: preservedTypes,
        tim: {
          ...this.tim,
          artifacts: preservedLevels,
        },
      });
      projectStore.updateProject({ artifactTypes: preservedTypes });
    },
    /**
     * Determines if the trace link is allowed based on the type of the nodes.
     *
     * @param source - The source artifact.
     * @param target - The target artifact.
     * @return Whether the link is allowed.
     */
    isLinkAllowedByType(
      source: ArtifactSchema | ArtifactCytoElementData,
      target: ArtifactSchema | ArtifactCytoElementData
    ): boolean {
      return isLinkAllowedByType(source, target, this.tim);
    },
    /**
     * Returns the display name for the given type.
     *
     * @param type - The artifact type.
     * @return The artifact type icon id.
     */
    getArtifactTypeDisplay(type: string): string {
      return this.tim.artifacts[type].name;
    },
    /**
     * Finds the icon id for the given artifact type.
     *
     * @param type - The artifact type.
     * @return The artifact type icon id.
     */
    getArtifactTypeIcon(type: string): string {
      return this.tim.artifacts[type].icon;
    },
    /**
     * Finds the artifact level info for an artifact type.
     *
     * @param type - The artifact type.
     * @return The artifact level, if one exists.
     */
    getArtifactLevel(type: string): TimArtifactLevelSchema | undefined {
      return this.tim.artifacts[type];
    },
    /**
     * Finds the artifact level info for an artifact type.
     *
     * @param source - The source artifact type.
     * @param target - The target artifact type.
     * @return The trace matrix, if one exists.
     */
    getTraceMatrix(
      source: string,
      target: string
    ): TimTraceMatrixSchema | undefined {
      return this.tim.traces.find(
        ({ sourceType, targetType }) =>
          sourceType === source && targetType === target
      );
    },
  },
});

export default useTypeOptions(pinia);

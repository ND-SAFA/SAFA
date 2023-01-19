import { defineStore } from "pinia";

import {
  ArtifactCytoElementData,
  ArtifactSchema,
  ArtifactTypeDirections,
  ArtifactTypeSchema,
  LabelledTraceDirectionSchema,
  ProjectSchema,
  SafetyCaseType,
  TraceDirectionSchema,
} from "@/types";
import {
  allTypeIcons,
  createDefaultTypeIcons,
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
     * A mapping of the allowed directions of links between artifacts.
     */
    artifactTypeDirections: {} as ArtifactTypeDirections,
    /**
     * A list of all artifact types.
     */
    allArtifactTypes: [] as ArtifactTypeSchema[],
    /**
     * A mapping of the icons for each artifact type.
     */
    artifactTypeIcons: createDefaultTypeIcons([]),
  }),
  getters: {
    /**
     * @returns all types of artifacts.
     */
    artifactTypes(): string[] {
      const safetyCaseTypes = Object.values(SafetyCaseType) as string[];

      return Object.keys(this.artifactTypeDirections).filter(
        (type) => !safetyCaseTypes.includes(type)
      );
    },
  },
  actions: {
    /**
     *Initializes project data.
     *
     * @param project - The project to load.
     */
    initializeProject(project: ProjectSchema): void {
      this.artifactTypeDirections = {};
      this.initializeTypeIcons(project.artifactTypes);
    },
    /**
     * Changes what directions of trace links between artifacts are allowed.
     *
     * @param allArtifactTypes - The artifact types to set.
     */
    initializeTypeIcons(allArtifactTypes: ArtifactTypeSchema[]): void {
      this.$patch({
        artifactTypeIcons: createDefaultTypeIcons(allArtifactTypes),
        allArtifactTypes,
      });
    },
    /**
     * Changes what directions of trace links between artifacts are allowed.
     *
     * @param type - The type to update.
     * @param allowedTypes - The allowed types to set.
     */
    updateLinkDirections({ type, allowedTypes }: TraceDirectionSchema): void {
      this.artifactTypeDirections = {
        ...this.artifactTypeDirections,
        [type]: allowedTypes,
      };
    },
    /**
     * Changes what icons each artifact uses.
     *
     * @param type - The type to update.
     * @param icon - The icon to set.
     */
    updateArtifactIcon({ type, icon }: LabelledTraceDirectionSchema): void {
      this.artifactTypeIcons = {
        ...this.artifactTypeIcons,
        [type]: icon,
      };
    },
    /**
     * Adds a new artifact types.
     *
     * @param artifactTypes - The artifact types to add.
     */
    addOrUpdateArtifactTypes(artifactTypes: ArtifactTypeSchema[]): void {
      const ids = artifactTypes.map(({ typeId }) => typeId);
      const allArtifactTypes = [
        ...removeMatches(this.allArtifactTypes, "typeId", ids),
        ...artifactTypes,
      ];

      this.initializeTypeIcons(allArtifactTypes);
      projectStore.updateProject({ artifactTypes: allArtifactTypes });
    },
    /**
     * Adds a new artifact type if it does not yet exist.
     *
     * @param newArtifacts - The artifact to add types from.
     */
    addTypesFromArtifacts(newArtifacts: ArtifactSchema[]): void {
      newArtifacts.forEach(({ type }) => {
        if (this.artifactTypeDirections[type]) return;

        this.$patch({
          artifactTypeIcons: {
            ...this.artifactTypeIcons,
            [type]: defaultTypeIcon,
          },
          artifactTypeDirections: {
            ...this.artifactTypeDirections,
            [type]: [],
          },
        });
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
      const artifactTypeIcons = preserveObjectKeys(
        this.artifactTypeIcons,
        names
      );
      const artifactTypeDirections = preserveObjectKeys(
        this.artifactTypeDirections,
        names
      );

      this.$patch((state) => {
        state.allArtifactTypes = preservedTypes;
        state.artifactTypeIcons = artifactTypeIcons;
        state.artifactTypeDirections = artifactTypeDirections;
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
      return isLinkAllowedByType(source, target, this.artifactTypeDirections);
    },
    /**
     * Returns the display name for the given type.
     *
     * @param type - The artifact type.
     * @return The artifact type icon id.
     */
    getArtifactTypeDisplay(type: string): string {
      return (
        this.allArtifactTypes.find(({ typeId }) => typeId === type)?.name ||
        type
      );
    },
    /**
     * Finds the icon id for the given artifact type.
     *
     * @param type - The artifact type.
     * @return The artifact type icon id.
     */
    getArtifactTypeIcon(type: string): string {
      return this.artifactTypeIcons[type] || this.artifactTypeIcons.default;
    },
    /**
     * Generates labeled artifact type directions.
     */
    typeDirections(): LabelledTraceDirectionSchema[] {
      return Object.entries(this.artifactTypeDirections).map(
        ([type, allowedTypes]) => {
          const icon = this.getArtifactTypeIcon(type);

          return {
            type,
            allowedTypes,
            label: type,
            icon,
            iconIndex: allTypeIcons.indexOf(icon),
          };
        }
      );
    },
  },
});

export default useTypeOptions(pinia);

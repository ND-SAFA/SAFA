import { defineStore } from "pinia";

import { pinia } from "@/plugins";
import {
  ArtifactData,
  ArtifactModel,
  ArtifactTypeDirections,
  ArtifactTypeModel,
  LabelledTraceDirectionModel,
  SafetyCaseType,
  TraceDirectionModel,
} from "@/types";
import {
  allTypeIcons,
  createDefaultTypeIcons,
  defaultTypeIcon,
  getArtifactTypePrintName,
  isLinkAllowedByType,
  preserveObjectKeys,
  removeMatches,
} from "@/util";
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
    allArtifactTypes: [] as ArtifactTypeModel[],
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
     * Changes what directions of trace links between artifacts are allowed.
     *
     * @param allArtifactTypes - The artifact types to set.
     */
    initializeTypeIcons(allArtifactTypes: ArtifactTypeModel[]): void {
      this.$patch({
        artifactTypeIcons: createDefaultTypeIcons(allArtifactTypes),
        allArtifactTypes,
        artifactTypeDirections: {},
      });
    },
    /**
     * Changes what directions of trace links between artifacts are allowed.
     *
     * @param type - The type to update.
     * @param allowedTypes - The allowed types to set.
     */
    updateLinkDirections({ type, allowedTypes }: TraceDirectionModel): void {
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
    updateArtifactIcon({ type, icon }: LabelledTraceDirectionModel): void {
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
    addOrUpdateArtifactTypes(artifactTypes: ArtifactTypeModel[]): void {
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
    addTypesFromArtifacts(newArtifacts: ArtifactModel[]): void {
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

      this.$patch({
        allArtifactTypes: preservedTypes,
        artifactTypeIcons: preserveObjectKeys(this.artifactTypeIcons, names),
        artifactTypeDirections: preserveObjectKeys(
          this.artifactTypeDirections,
          names
        ),
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
      source: ArtifactModel | ArtifactData,
      target: ArtifactModel | ArtifactData
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
      return getArtifactTypePrintName(type);
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
    typeDirections(): LabelledTraceDirectionModel[] {
      return Object.entries(this.artifactTypeDirections).map(
        ([type, allowedTypes]) => {
          const icon = this.getArtifactTypeIcon(type);

          return {
            type,
            allowedTypes,
            label: getArtifactTypePrintName(type),
            icon,
            iconIndex: allTypeIcons.indexOf(icon),
          };
        }
      );
    },
  },
});

export default useTypeOptions(pinia);

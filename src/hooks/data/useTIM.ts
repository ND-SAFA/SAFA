import { defineStore } from "pinia";

import {
  ArtifactCytoElementData,
  ArtifactSchema,
  ArtifactTypeSchema,
  ProjectSchema,
  TraceMatrixSchema,
} from "@/types";
import {
  convertTypeToColor,
  DefaultTypeIcon,
  isLinkAllowedByType,
  normalizeColorName,
  removeMatches,
  sanitizeNodeId,
  sortArtifactTypes,
} from "@/util";
import { selectionStore } from "@/hooks";
import { pinia } from "@/plugins";

/**
 * This store manages the state of project TIM data,
 * including artifact types and trace matrices.
 */
export const useTIM = defineStore("tim", {
  state: () => ({
    /**
     * The artifact types in the project.
     */
    artifactTypes: [] as ArtifactTypeSchema[],
    /**
     * The trace matrices in the project.
     */
    traceMatrices: [] as TraceMatrixSchema[],
  }),
  getters: {
    /**
     * @returns all type names of artifacts.
     */
    typeNames(): string[] {
      return this.artifactTypes.map(({ name }) => name);
    },
    /**
     * @return The currently selected artifact level.
     */
    selectedArtifactLevel(): ArtifactTypeSchema | undefined {
      return this.artifactTypes.find(
        (type) => type.name === selectionStore.selectedArtifactLevelType
      );
    },
    /**
     * @return The currently selected trace matrix.
     */
    selectedTraceMatrix(): TraceMatrixSchema | undefined {
      return this.traceMatrices.find(
        ({ sourceType, targetType }) =>
          sanitizeNodeId(sourceType) ===
            selectionStore.selectedTraceMatrixTypes[0] &&
          sanitizeNodeId(targetType) ===
            selectionStore.selectedTraceMatrixTypes[1]
      );
    },
  },
  actions: {
    /**
     * Initializes project data.
     *
     * @param project - The project to load.
     */
    initializeProject(project: ProjectSchema): void {
      this.artifactTypes = sortArtifactTypes(project);
      this.traceMatrices = project.traceMatrices;
    },
    /**
     * Adds new artifact types.
     *
     * @param artifactTypes - The artifact types to add.
     */
    addOrUpdateArtifactTypes(artifactTypes: ArtifactTypeSchema[]): void {
      const ids = artifactTypes.map(({ name }) => name);

      this.artifactTypes = [
        ...removeMatches(this.artifactTypes, "name", ids),
        ...artifactTypes,
      ];
    },
    /**
     * Adds a new placeholder artifact type if it does not yet exist.
     *
     * @param newArtifacts - The artifact to add types from.
     */
    addTypesFromArtifacts(newArtifacts: ArtifactSchema[]): void {
      newArtifacts.forEach(({ type }) => {
        if (this.artifactTypes.find(({ name }) => name === type)) return;

        this.artifactTypes = [
          ...this.artifactTypes,
          {
            typeId: "",
            name: type,
            icon: DefaultTypeIcon,
            color: "base",
            count: 1,
          },
        ];
      });
    },
    /**
     * Removes artifact types.
     *
     * @param removedTypeIds - The artifact type ids to remove.
     */
    deleteArtifactTypes(removedTypeIds: string[]): void {
      this.artifactTypes = removeMatches(
        this.artifactTypes,
        "typeId",
        removedTypeIds
      );
    },
    /**
     * Adds new trace matrices.
     *
     * @param traceMatrices - The trace matrices to add.
     */
    addOrUpdateTraceMatrices(traceMatrices: TraceMatrixSchema[]): void {
      const ids = traceMatrices.map(({ id }) => id);

      this.traceMatrices = [
        ...removeMatches(this.traceMatrices, "id", ids),
        ...traceMatrices,
      ];
    },
    /**
     * Adds a placeholder trace matrix between these types.
     * @param sourceType - The source type.
     * @param targetType - The target type.
     */
    addTraceMatrix(sourceType: string, targetType: string): void {
      this.addOrUpdateTraceMatrices([
        {
          id: "",
          sourceType,
          targetType,
          count: 1,
          generatedCount: 0,
          approvedCount: 0,
        },
      ]);
    },
    /**
     * Removes trace matrices.
     *
     * @param removedMatrixIds - The trace matrix ids to remove.
     */
    deleteTraceMatrices(removedMatrixIds: string[]): void {
      this.traceMatrices = removeMatches(
        this.traceMatrices,
        "id",
        removedMatrixIds
      );
    },
    /**
     * Removes a trace matrix between these types.
     *
     * @param sourceType - The source type.
     * @param targetType - The target type.
     */
    deleteTraceMatrix(sourceType: string, targetType: string): void {
      this.traceMatrices = this.traceMatrices.filter(
        (matrix) =>
          matrix.sourceType !== sourceType || matrix.targetType !== targetType
      );
    },
    /**
     * Gets the artifact type with the given name.
     *
     * @param name - The name of the artifact type to get.
     * @returns The artifact type with the given name, or undefined if it does not exist.
     */
    getType(name: string): ArtifactTypeSchema | undefined {
      return this.artifactTypes.find((type) => type.name === name);
    },
    /**
     * TODO: This is a placeholder for when we use the type id as the reference, instead of the name.
     * Returns the display name for a given artifact type.
     *
     * @param name - The name of the artifact type to get the display name
     * @returns An icon id to display for the type.
     */
    getTypeName(name: string): string {
      return name;
    },
    /**
     * Returns the color code for a given artifact type.
     *
     * @param name - The name of the artifact type to get the color of.
     * @param dontConvert - If true, the color will not be converted to a hex code.
     * @returns A color code to display for the type.
     */
    getTypeColor(name: string, dontConvert?: boolean): string {
      const artifactType = this.getType(name);
      const themeColor = normalizeColorName(artifactType?.color || "primary");

      return dontConvert ? themeColor : convertTypeToColor(themeColor);
    },
    /**
     * Returns the icon id for a given artifact type.
     *
     * @param name - The name of the artifact type to get the icon of.
     * @returns An icon id to display for the type.
     */
    getTypeIcon(name: string): string {
      const artifactType = this.getType(name);

      return artifactType?.icon.includes("help")
        ? DefaultTypeIcon
        : artifactType?.icon || DefaultTypeIcon;
    },
    /**
     * Gets the trace matrix with the given source and target types.
     *
     * @param sourceName - The source artifact type name.
     * @param targetName - The target artifact type name.
     * @returns The matching trace matrix, or undefined if it does not exist.
     */
    getMatrix(
      sourceName: string,
      targetName: string
    ): TraceMatrixSchema | undefined {
      return this.traceMatrices.find(
        ({ sourceType, targetType }) =>
          sanitizeNodeId(sourceType) === sourceName &&
          sanitizeNodeId(targetType) === targetName
      );
    },
    /**
     * Gets all trace matrices that are a parent of the given one.
     *
     * @param sourceName - The source artifact type name.
     * @returns All  artifact types that are a parent to this type.
     */
    getParentMatrices(sourceName: string): ArtifactTypeSchema[] {
      return this.traceMatrices
        .filter(({ sourceType }) => sourceType === sourceName)
        .map(({ targetType }) => this.getType(targetType))
        .filter((type) => type !== undefined) as ArtifactTypeSchema[];
    },
    /**
     * Gets all trace matrices that are a child of the given one.
     *
     * @param targetName - The target artifact type name.
     * @returns All artifact types that are a child to this type.
     */
    getChildMatrices(targetName: string): ArtifactTypeSchema[] {
      return this.traceMatrices
        .filter(({ targetType }) => targetType === targetName)
        .map(({ sourceType }) => this.getType(sourceType))
        .filter((type) => type !== undefined) as ArtifactTypeSchema[];
    },
    /**
     * Determines if the trace link is allowed based on the type of the nodes.
     *
     * @param source - The source artifact.
     * @param target - The target artifact.
     * @return Whether the link is allowed.
     */
    canBeTraced(
      source: ArtifactSchema | ArtifactCytoElementData,
      target: ArtifactSchema | ArtifactCytoElementData
    ): boolean {
      return isLinkAllowedByType(source, target, this.traceMatrices);
    },
  },
});

export default useTIM(pinia);

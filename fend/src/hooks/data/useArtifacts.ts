import { defineStore } from "pinia";

import { ArtifactSchema, DocumentArtifacts, FlatArtifact } from "@/types";
import {
  collectByField,
  flattenArtifact,
  LARGE_NODE_COUNT,
  preserveMatches,
  removeMatches,
  standardizeValueArray,
} from "@/util";
import { layoutStore, selectionStore, timStore, traceStore } from "@/hooks";
import { pinia } from "@/plugins";

/**
 * This module defines the state of the current project's artifacts.
 */
export const useArtifacts = defineStore("artifacts", {
  state: () => ({
    /**
     * All artifacts in the project.
     */
    allArtifacts: [] as ArtifactSchema[],
    /**
     * The artifacts visible in the current document.
     */
    currentArtifacts: [] as ArtifactSchema[],
    /**
     * A map of artifacts by id.
     */
    artifactsById: new Map<string, ArtifactSchema>(),
    /**
     * A map of artifacts by name.
     */
    artifactsByName: new Map<string, ArtifactSchema>(),
    /**
     * A map of artifacts by type.
     */
    artifactsByType: new Map<string, ArtifactSchema[]>(),
  }),
  getters: {
    /**
     * @return Whether the current document has a large number of artifacts,
     * in which case certain graph features are optimized and disabled.
     */
    largeNodeCount(): boolean {
      return this.currentArtifacts.length > LARGE_NODE_COUNT;
    },
    /**
     * @return The IDs of all current artifacts that have a parent and no children.
     */
    leaves(): string[] {
      const withParents = new Set();
      const withChildren = new Set();
      const leaves: string[] = [];

      traceStore.currentTraces.forEach(({ sourceId, targetId }) => {
        withParents.add(sourceId);
        withChildren.add(targetId);
      });

      this.currentArtifacts.forEach(({ id }) => {
        if (withParents.has(id) && !withChildren.has(id)) {
          leaves.push(id);
        }
      });

      return leaves;
    },
    /**
     * @return The currently selected artifact.
     */
    selectedArtifact(): ArtifactSchema | undefined {
      return this.artifactsById.get(selectionStore.selectedArtifactId);
    },
    /**
     * @return The ids of artifacts that are in the viewport.
     */
    artifactsInView(): string[] {
      return this.currentArtifacts
        .filter((artifact) => selectionStore.isArtifactInView(artifact))
        .map(({ id }) => id);
    },
  },
  actions: {
    /**
     * Initializes the artifacts visible in the current document.
     */
    initializeArtifacts(documentArtifacts: DocumentArtifacts): void {
      const { artifacts = this.allArtifacts, currentArtifactIds } =
        documentArtifacts;

      this.$patch({
        allArtifacts: artifacts,
        currentArtifacts: currentArtifactIds
          ? preserveMatches(artifacts, "id", currentArtifactIds)
          : artifacts,
        artifactsById: new Map(
          artifacts.map((artifact) => [artifact.id, artifact])
        ),
        artifactsByName: new Map(
          artifacts.map((artifact) => [artifact.name, artifact])
        ),
        artifactsByType: new Map(
          Object.entries(collectByField(artifacts, "type"))
        ),
      });
    },
    /**
     * Updates the current artifacts in the project, preserving any that already existed.
     *
     * @param newArtifacts - The new artifacts to add.
     */
    addOrUpdateArtifacts(newArtifacts: ArtifactSchema[]): void {
      const newIds = newArtifacts.map(({ id }) => id);
      const updatedArtifacts = [
        ...removeMatches(this.allArtifacts, "id", newIds),
        ...newArtifacts,
      ];

      this.$patch({
        allArtifacts: updatedArtifacts,
        currentArtifacts: [
          ...removeMatches(this.currentArtifacts, "id", newIds),
          ...newArtifacts,
        ],
        artifactsById: new Map(
          updatedArtifacts.map((artifact) => [artifact.id, artifact])
        ),
        artifactsByName: new Map(
          updatedArtifacts.map((artifact) => [artifact.name, artifact])
        ),
        artifactsByType: new Map(
          Object.entries(collectByField(updatedArtifacts, "type"))
        ),
      });
    },
    /**
     * Adds a created artifact and updates the layout.
     *
     * @param artifact - The newly created artifact.
     */
    addCreatedArtifact(artifact: ArtifactSchema): void {
      layoutStore.setArtifactToSavedPosition(artifact.id);
      this.addOrUpdateArtifacts([artifact]);
      timStore.addTypesFromArtifacts([artifact]);
    },
    /**
     * Deletes the artifacts with the given names.
     *
     * @param deletedArtifacts - The artifacts, or ids, to delete.
     */
    deleteArtifacts(deletedArtifacts: ArtifactSchema[] | string[]): void {
      if (deletedArtifacts.length === 0) return;

      const ids = standardizeValueArray(deletedArtifacts, "id");
      const allArtifacts = removeMatches(this.allArtifacts, "id", ids);

      this.$patch({
        allArtifacts,
        currentArtifacts: removeMatches(this.currentArtifacts, "id", ids),
        artifactsById: new Map(
          allArtifacts.map((artifact) => [artifact.id, artifact])
        ),
        artifactsByName: new Map(
          allArtifacts.map((artifact) => [artifact.name, artifact])
        ),
        artifactsByType: new Map(
          Object.entries(collectByField(allArtifacts, "type"))
        ),
      });
    },
    /**
     * Finds the given artifact by name.
     *
     * @param name - The name to find.
     * @return The matching artifact, if one exists.
     */
    getArtifactByName(name: string): ArtifactSchema | undefined {
      return this.artifactsByName.get(name);
    },
    /**
     * Finds the given artifact by id.
     *
     * @param id - The id to find.
     * @return The matching artifact, if one exists.
     */
    getArtifactById(id: string): ArtifactSchema | undefined {
      return this.artifactsById.get(id);
    },
    /**
     * Finds all artifacts of the given type.
     *
     * @param type - The type to find.
     * @return The matching artifacts.
     */
    getArtifactsByType(type: string): ArtifactSchema[] {
      return this.artifactsByType.get(type) || [];
    },
    /**
     * Returns flattened artifacts for display.
     * @param allArtifacts - Whether to return all artifacts, or just the current document's.
     * @return The flattened artifacts.
     */
    getFlatArtifacts(allArtifacts?: boolean): FlatArtifact[] {
      return allArtifacts
        ? this.allArtifacts.map(flattenArtifact)
        : this.currentArtifacts.map(flattenArtifact);
    },
  },
});

export default useArtifacts(pinia);

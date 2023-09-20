import { defineStore } from "pinia";

import { ArtifactSchema, DocumentArtifacts, FlatArtifact } from "@/types";
import {
  standardizeValueArray,
  flattenArtifact,
  preserveMatches,
  removeMatches,
  collectByField,
} from "@/util";
import {
  timStore,
  documentStore,
  projectStore,
  layoutStore,
  selectionStore,
} from "@/hooks";
import { pinia } from "@/plugins";

/**
 * This module defines the state of the current project's artifacts.
 */
export const useArtifacts = defineStore("artifacts", {
  state: () => ({
    allArtifacts: [] as ArtifactSchema[],
    currentArtifacts: [] as ArtifactSchema[],
  }),
  getters: {
    /**
     * @return The flattened artifacts for the current document.
     */
    flatArtifacts(): FlatArtifact[] {
      return this.currentArtifacts.map(flattenArtifact);
    },
    /**
     * @return A collection of current artifact lists, keyed by their type.
     */
    allArtifactsByType(): Record<string, ArtifactSchema[]> {
      return collectByField(this.allArtifacts, "type");
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

      documentStore.addDocumentArtifacts(newIds);
      this.initializeArtifacts({
        artifacts: updatedArtifacts,
        currentArtifactIds: documentStore.currentArtifactIds,
      });
      projectStore.updateProject({
        artifacts: updatedArtifacts,
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
      selectionStore.selectArtifact(artifact.id);
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
      });
      projectStore.updateProject({ artifacts: allArtifacts });

      if (ids.includes(selectionStore.selectedArtifact?.id || "")) {
        selectionStore.clearSelections();
      }
    },
    /**
     * Finds the given artifact by name.
     *
     * @param name - The name to find.
     * @return The matching artifact, if one exists.
     */
    getArtifactByName(name: string): ArtifactSchema | undefined {
      return this.allArtifacts.find((artifact) => artifact.name === name);
    },
    /**
     * Finds the given artifact by id.
     *
     * @param id - The id to find.
     * @return The matching artifact, if one exists.
     */
    getArtifactById(id: string): ArtifactSchema | undefined {
      return this.allArtifacts.find((artifact) => artifact.id === id);
    },
    /**
     * Finds all artifacts of the given type.
     *
     * @param type - The type to find.
     * @return The matching artifacts.
     */
    getArtifactsByType(type: string): ArtifactSchema[] {
      return this.allArtifacts.filter((artifact) => artifact.type === type);
    },
  },
});

export default useArtifacts(pinia);

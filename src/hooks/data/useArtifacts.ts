import { defineStore } from "pinia";

import { ArtifactSchema, DocumentArtifacts, FlatArtifact } from "@/types";
import {
  collectByField,
  flattenArtifact,
  preserveMatches,
  removeMatches,
  standardizeValueArray,
} from "@/util";
import {
  documentStore,
  layoutStore,
  projectStore,
  selectionStore,
  timStore,
} from "@/hooks";
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
     * @return The flattened artifacts for the current document.
     */
    flatArtifacts(): FlatArtifact[] {
      return this.currentArtifacts.map(flattenArtifact);
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
  },
});

export default useArtifacts(pinia);

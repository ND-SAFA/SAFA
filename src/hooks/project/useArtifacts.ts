import { defineStore } from "pinia";

import { pinia } from "@/plugins";
import { ArtifactModel, DocumentArtifacts, FlatArtifact } from "@/types";

/**
 * This module defines the state of the current project's artifacts.
 */
export const useArtifacts = defineStore("artifacts", {
  state: () => ({
    allArtifacts: [] as ArtifactModel[],
    currentArtifacts: [] as ArtifactModel[],
  }),
  getters: {
    /**
     * @return The flattened artifacts for the current document.
     */
    flatArtifacts(): FlatArtifact[] {
      return this.currentArtifacts.map(
        ({ customFields, ...artifact }) =>
          ({
            ...artifact,
            ...customFields,
          } as FlatArtifact)
      );
    },
    /**
     * @return A collection of current artifact lists, keyed by their type.
     */
    getArtifactsByType(): Record<string, ArtifactModel[]> {
      const artifactsByType: Record<string, ArtifactModel[]> = {};

      this.currentArtifacts.forEach((artifact) => {
        if (!artifactsByType[artifact.type]) {
          artifactsByType[artifact.type] = [];
        }

        artifactsByType[artifact.type].push(artifact);
      });

      return artifactsByType;
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
          ? artifacts.filter(({ id }) => currentArtifactIds.includes(id))
          : artifacts,
      });
    },
    /**
     * DO NOT CALL THIS OUTSIDE OF THE STORES.
     * Deletes the artifacts with the given names.
     *
     * @param artifacts - The artifacts to delete.
     */
    deleteArtifacts(artifacts: ArtifactModel[]): void {
      const deletedNames = artifacts.map(({ name }) => name);
      const removeArtifact = (currentArtifacts: ArtifactModel[]) =>
        currentArtifacts.filter(({ name }) => !deletedNames.includes(name));

      this.$patch({
        allArtifacts: removeArtifact(this.allArtifacts),
        currentArtifacts: removeArtifact(this.currentArtifacts),
      });
    },
    /**
     * Finds the given artifact by name.
     *
     * @param name - The name to find.
     * @return The matching artifact, if one exists.
     */
    getArtifactByName(name: string): ArtifactModel | undefined {
      return this.allArtifacts.find((artifact) => artifact.name === name);
    },
    /**
     * Finds the given artifact by id.
     *
     * @param id - The id to find.
     * @return The matching artifact, if one exists.
     */
    getArtifactById(id: string): ArtifactModel | undefined {
      return this.allArtifacts.find((artifact) => artifact.id === id);
    },
  },
});

export default useArtifacts(pinia);

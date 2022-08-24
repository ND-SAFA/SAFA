import { defineStore } from "pinia";

import { pinia } from "@/plugins";
import { ArtifactModel, DocumentArtifacts, FlatArtifact } from "@/types";
import documentStore from "@/hooks/project/useDocuments";
import typeOptionsStore from "@/hooks/project/useTypeOptions";
import subtreeStore from "@/hooks/project/useSubtree";
import projectStore from "@/hooks/project/useProject";

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
     * Updates the current artifacts in the project, preserving any that already existed.
     *
     * @param newArtifacts - The new artifacts to add.
     */
    addOrUpdateArtifacts(newArtifacts: ArtifactModel[]): void {
      const newIds = newArtifacts.map(({ id }) => id);
      const updatedArtifacts = [
        ...this.allArtifacts.filter(({ id }) => !newIds.includes(id)),
        ...newArtifacts,
      ];

      this.initializeArtifacts({
        artifacts: updatedArtifacts,
        currentArtifactIds: documentStore.currentDocument.artifactIds,
      });
      projectStore.updateProject({
        artifacts: updatedArtifacts,
      });
      typeOptionsStore.addTypesFromArtifacts(newArtifacts);
      subtreeStore.updateSubtreeMap();
    },
    /**
     * Deletes the artifacts with the given names.
     *
     * @param deletedArtifacts - The artifacts, or ids, to delete.
     */
    deleteArtifacts(deletedArtifacts: ArtifactModel[] | string[]): void {
      if (deletedArtifacts.length === 0) return;

      const deletedIds = deletedArtifacts.map((artifact) =>
        typeof artifact === "string" ? artifact : artifact.id
      );
      const removeArtifacts = (currentArtifacts: ArtifactModel[]) =>
        currentArtifacts.filter(({ id }) => !deletedIds.includes(id));
      const allArtifacts = removeArtifacts(this.allArtifacts);

      this.$patch({
        allArtifacts,
        currentArtifacts: removeArtifacts(this.currentArtifacts),
      });
      projectStore.updateProject({ artifacts: allArtifacts });
      subtreeStore.updateSubtreeMap();
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

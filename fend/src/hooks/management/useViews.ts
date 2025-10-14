import { defineStore } from "pinia";

import { ArtifactSchema } from "@/types";
import { buildDocument, LARGE_NODE_LAYOUT_COUNT } from "@/util";
import {
  artifactStore,
  documentStore,
  layoutStore,
  projectStore,
  selectionStore,
  subtreeStore,
} from "@/hooks";
import { QueryParams, updateParam } from "@/router";
import { pinia } from "@/plugins";

/**
 * The Views store is tightly coupled with the document store, as both manage what artifacts are currently displayed.
 * - Documents focuses on the storage of the document itself.
 * - Views focuses on building custom documents locally, that can optionally be saved.
 */
export const useViews = defineStore("useViews", {
  state: () => ({}),
  getters: {},
  actions: {
    /**
     * Creates and adds a new document based on the neighborhood of an artifact.
     * - If the neighborhood is too large, the document will instead include the parents and children, and
     *   hide the child subtrees.
     * @param artifact - The artifact to display the neighborhood of.
     */
    async addDocumentOfNeighborhood(
      artifact: Pick<ArtifactSchema, "name" | "id">
    ): Promise<void> {
      const hideSubtrees =
        subtreeStore.getNeighbors(artifact.id).length > LARGE_NODE_LAYOUT_COUNT;
      const neighbors = hideSubtrees
        ? subtreeStore.getParentsAndChildren(artifact.id)
        : subtreeStore.getNeighbors(artifact.id);
      const visibleNeighbors =
        selectionStore.ignoreTypes.length === 0
          ? neighbors
          : neighbors.filter(
              (id) =>
                !selectionStore.ignoreTypes.includes(
                  artifactStore.getArtifactById(id)?.type || ""
                )
            );

      const document = buildDocument({
        project: projectStore.projectIdentifier,
        name: artifact.name,
        artifactIds: [artifact.id, ...visibleNeighbors],
      });

      await documentStore.addDocument(document);

      if (hideSubtrees) {
        subtreeStore.hideChildSubtrees(artifact.id);
      }

      layoutStore.mode = "tree";

      await updateParam(QueryParams.VIEW, artifact.id, true);
    },
    /**
     * Shows the subtree of an artifact in the current document.
     * - If the subtree is at all missing from the current document, it will be added.
     * - All child nodes added will also have their subtrees hidden.
     * @param artifact - The artifact to show the subtree of.
     */
    async extendDocumentSubtree(artifact: ArtifactSchema): Promise<void> {
      const documentArtifactsWithSubtree = new Set([
        ...subtreeStore.getChildren(artifact.id),
        ...documentStore.currentDocument.artifactIds,
      ]);

      if (
        documentStore.currentDocument.artifactIds.length <
        documentArtifactsWithSubtree.size
      ) {
        await documentStore.addDocument(
          buildDocument({
            project: projectStore.projectIdentifier,
            name: documentStore.currentDocument.name,
            artifactIds: Array.from(documentArtifactsWithSubtree),
          })
        );
      }

      await subtreeStore.showSubtree(artifact.id);
      await subtreeStore.hideChildSubtrees(artifact.id);
    },
    /**
     * Creates and adds a new document for multiple types of artifacts.
     * @param types - The artifact types to include in the document.
     */
    async addDocumentOfTypes(types: string[]): Promise<void> {
      const document = buildDocument({
        project: projectStore.projectIdentifier,
        name: types.join(", "),
        artifactIds: types.flatMap((type) =>
          artifactStore.getArtifactsByType(type).map(({ id }) => id)
        ),
      });

      await documentStore.addDocument(document);
      layoutStore.mode = types.length > 1 ? "tree" : "table";
    },
  },
});

export default useViews(pinia);

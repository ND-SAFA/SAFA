import { defineStore } from "pinia";

import { pinia } from "@/plugins";
import {
  ArtifactModel,
  SubtreeLinkModel,
  SubtreeMap,
  TraceLinkModel,
} from "@/types";
import { artifactModule, traceModule } from "@/store";
import { createSubtreeMap } from "@/util";
import { cyDisplayAll } from "@/cytoscape";

/**
 * This module keeps track of the tree of artifacts.
 */
export const useSubtree = defineStore("subtrees", {
  state: () => ({
    /**
     * A map containing root artifact names as keys and children names are values.
     */
    subtreeMap: {} as SubtreeMap,
    /**
     * List of phantom links used when hiding subtrees.
     */
    subtreeLinks: [] as SubtreeLinkModel[],
    /**
     * List of nodes currently hidden within subtrees.
     */
    hiddenSubtreeNodes: [] as string[],
    /**
     * List of nodes whose children are currently hidden.
     */
    collapsedParentNodes: [] as string[],
  }),
  getters: {},
  actions: {
    /**
     * Recalculates the subtree map of project artifacts and updates store.
     *
     * @param artifacts - The artifacts to create the subtree for.
     * @param traces - The traces to create the subtree for.
     */
    updateSubtreeMap(
      artifacts: ArtifactModel[] = artifactModule.allArtifacts,
      traces: TraceLinkModel[] = traceModule.allTraces
    ): void {
      this.subtreeMap = createSubtreeMap(artifacts, traces);
    },
    /**
     * Resets all hidden nodes.
     */
    resetHiddenNodes(): void {
      this.collapsedParentNodes = [];
      this.hiddenSubtreeNodes = [];
      cyDisplayAll();
    },
  },
});

export default useSubtree(pinia);

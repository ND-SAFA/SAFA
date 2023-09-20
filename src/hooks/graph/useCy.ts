import { defineStore } from "pinia";

import { CyPromise, CytoCoreGraph, ResolveCy } from "@/types";
import { layoutStore } from "@/hooks";
import { GRAPH_CONFIG, CREATOR_PLUGINS } from "@/cytoscape";
import { pinia } from "@/plugins";

/**
 * Transferring the state of the cytoscape instances behaves weirdly asynchronously,
 * so this is a temporary solution to get the cytoscape instances.
 */

/**
 * Wraps cytoscape instance in a promise.
 */
let creatorResolveCy: ResolveCy = null;
const creatorCy: CyPromise = new Promise((resolve) => {
  creatorResolveCy = resolve;
});

/**
 * This hook manages the state of all cytoscape graphs.
 */
export const useCy = defineStore("cy", {
  state: () => ({}),
  getters: {
    /**
     * @return A promise for using the project creator cy instance.
     */
    creatorCy(): CyPromise {
      return creatorCy;
    },
    /**
     * @return The configuration for the creator graph.
     */
    creatorGraph(): CytoCoreGraph {
      return {
        name: "tim-tree-graph",
        config: GRAPH_CONFIG,
        saveCy: creatorResolveCy,
        plugins: CREATOR_PLUGINS,
        afterInit() {
          // Wait for initialized nodes to be added.
          setTimeout(() => {
            layoutStore.setTimTreeLayout();
          }, 100);
        },
      };
    },
  },
  actions: {
    /**
     * Resets the graph window.
     * @param type - The type of graph to reset.
     */
    resetWindow(type: "project" | "creator") {
      if (type === "creator") {
        creatorCy.then((cy) => {
          cy.fit(cy.nodes(), 150);
        });
      }
    },
  },
});

export default useCy(pinia);

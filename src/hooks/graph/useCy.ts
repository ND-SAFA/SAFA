import { defineStore } from "pinia";

import { CyPromise, CytoCoreGraph, ResolveCy } from "@/types";
import { layoutStore } from "@/hooks";
import { GRAPH_CONFIG, CREATOR_PLUGINS } from "@/cytoscape";
import { pinia } from "@/plugins";

/**
 * This hook manages the state of all cytoscape graphs.
 */
export const useCy = defineStore("cy", {
  state: () => ({
    /**
     * A promise that resolves to the project creator cy instance.
     */
    creatorResolveCy: null as ResolveCy,
  }),
  getters: {
    /**
     * @return A promise for using the project creator cy instance.
     */
    creatorCy(): CyPromise {
      return new Promise((resolve) => (this.creatorResolveCy = resolve));
    },
    /**
     * @return The configuration for the creator graph.
     */
    creatorGraph(): CytoCoreGraph {
      return {
        name: "tim-tree-graph",
        config: GRAPH_CONFIG,
        saveCy: this.creatorResolveCy,
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
        this.creatorCy.then((cy) => {
          cy.fit(cy.nodes(), 150);
        });
      }
    },
  },
});

export default useCy(pinia);

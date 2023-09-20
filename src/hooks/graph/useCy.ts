import { defineStore } from "pinia";

import { CyPromise, CytoCoreGraph, ResolveCy } from "@/types";
import { layoutStore } from "@/hooks";
import { GRAPH_CONFIG, CREATOR_PLUGINS, PROJECT_PLUGINS } from "@/cytoscape";
import { pinia } from "@/plugins";

/**
 * This hook manages the state of all cytoscape graphs.
 */
export const useCy = defineStore("cy", {
  state() {
    let creatorResolveCy: ResolveCy = null;

    const creatorCy: CyPromise = new Promise((resolve) => {
      creatorResolveCy = resolve;
    });

    let projectResolveCy: ResolveCy = null;

    const projectCy: CyPromise = new Promise((resolve) => {
      projectResolveCy = resolve;
    });

    return {
      /**
       * Wraps creator cytoscape instance in a promise until it is created.
       */
      creatorResolveCy,
      /**
       * A promise for using the creator cy instance.
       */
      creatorCy,
      /**
       * Wraps project cytoscape instance in a promise until it is created.
       */
      projectResolveCy,
      /**
       * A promise for using the project cy instance.
       */
      projectCy,
    };
  },
  getters: {
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
            layoutStore.setCreatorLayout();
          }, 100);
        },
      };
    },
    /**
     * @return The configuration for the project graph.
     */
    projectGraph(): CytoCoreGraph {
      return {
        name: "artifact-tree-graph",
        config: GRAPH_CONFIG,
        saveCy: this.projectResolveCy,
        plugins: PROJECT_PLUGINS,
        afterInit: () => undefined,
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

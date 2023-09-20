import klay from "cytoscape-klay";
import automove from "cytoscape-automove";
import edgehandles from "cytoscape-edgehandles";
import { CytoCore } from "@/types";
import { cyStore } from "@/hooks";
import { artifactTreeEdgeHandleOptions, setEdgeHandlesCore } from "@/cytoscape";

/**
 * Plugins used on the creator graph.
 */
export const CREATOR_PLUGINS = [
  {
    initialize: klay,
    afterInit: () => undefined,
  },
];

/**
 * Plugins used on the project graph.
 */
export const PROJECT_PLUGINS = [
  {
    initialize: klay,
    afterInit: () => undefined,
  },
  {
    initialize: automove,
    afterInit: () => undefined,
  },
  {
    initialize: edgehandles,
    afterInit(cy: CytoCore): Promise<void> {
      return setEdgeHandlesCore(
        cyStore.projectCy,
        cy.edgehandles(artifactTreeEdgeHandleOptions)
      );
    },
  },
];

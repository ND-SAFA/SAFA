import nodeHtmlLabel from "cytoscape-node-html-label";
import klay from "cytoscape-klay";
import automove from "cytoscape-automove";
import contextMenus from "cytoscape-context-menus";
import edgehandles from "cytoscape-edgehandles";

import { CytoCore, CytoCoreGraph } from "@/types";
import { artifactTreeCyPromise, artifactTreeResolveCy } from "@/cytoscape/cy";
import {
  artifactTreeContextMenuOptions,
  artifactTreeEdgeHandleOptions,
  setEdgeHandlesCore,
} from "@/cytoscape/plugins";
import {
  DEFAULT_ARTIFACT_TREE_ZOOM,
  edgeStyles,
  nodeStyles,
  USE_MOTION_BLUR,
} from "@/cytoscape/styles";

/**
 * Defines the initialization of the artifact tree graph.
 */
export const artifactTreeGraph: CytoCoreGraph = {
  name: "artifact-tree-graph",
  config: {
    style: [...nodeStyles, ...edgeStyles],
    motionBlur: USE_MOTION_BLUR,
    zoom: DEFAULT_ARTIFACT_TREE_ZOOM,
    boxSelectionEnabled: true,
  },
  saveCy: artifactTreeResolveCy,
  plugins: [
    {
      initialize: nodeHtmlLabel,
      afterInit: () => undefined,
    },
    {
      initialize: klay,
      afterInit: () => undefined,
    },
    {
      initialize: automove,
      afterInit: () => undefined,
    },
    {
      initialize: contextMenus,
      afterInit(cy: CytoCore): void {
        cy.contextMenus(artifactTreeContextMenuOptions);
      },
    },
    {
      initialize: edgehandles,
      afterInit(cy: CytoCore): Promise<void> {
        return setEdgeHandlesCore(
          artifactTreeCyPromise,
          cy.edgehandles(artifactTreeEdgeHandleOptions)
        );
      },
    },
  ],
  afterInit: () => undefined,
};

import { CytoscapeOptions } from "cytoscape";
import nodeHtmlLabel from "cytoscape-node-html-label";
import klay from "cytoscape-klay";
import automove from "cytoscape-automove";
import contextMenus from "cytoscape-context-menus";
import edgehandles from "cytoscape-edgehandles";
import { CytoCore, IGraphLayout, CytoCoreGraph } from "@/types";
import { artifactTreeContextMenuOptions } from "@/cytoscape/context-menu";
import {
  artifactTreeEdgeHandleOptions,
  setEdgeHandlesCore,
} from "@/cytoscape/edge-handles";
import {
  DEFAULT_ZOOM,
  GraphStyle,
  MOTION_BLUE_OPACITY,
  USE_MOTION_BLUR,
} from "@/cytoscape/styles";
import { GraphLayout } from "@/cytoscape/layout";
import { viewportModule } from "@/store";
import {
  artifactTreeResolveCy,
  artifactTreeCyPromise,
} from "./artifact-tree-cy";

const artifactTreeConfig: CytoscapeOptions = {
  style: GraphStyle,
  motionBlur: USE_MOTION_BLUR,
  motionBlurOpacity: MOTION_BLUE_OPACITY,
  zoom: DEFAULT_ZOOM,
};

export const artifactTreeGraph: CytoCoreGraph = {
  name: "artifact-tree-graph",
  config: artifactTreeConfig,
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
      afterInit: async (cy: CytoCore) =>
        await setEdgeHandlesCore(
          artifactTreeCyPromise,
          cy.edgehandles(artifactTreeEdgeHandleOptions)
        ),
    },
  ],
  async afterInit(cy) {
    const cyPromise: Promise<CytoCore> = new Promise((resolve) => resolve(cy));
    const layout = new GraphLayout();
    await viewportModule.setGraphLayout(cyPromise, layout as IGraphLayout);
  },
};

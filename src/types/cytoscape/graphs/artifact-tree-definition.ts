import { CytoCore, IGraphLayout } from "@/types/cytoscape";
import nodeHtmlLabel from "cytoscape-node-html-label";
import klay from "cytoscape-klay";
import automove from "cytoscape-automove";
import contextMenus from "cytoscape-context-menus";
import {
  artifactTreeContextMenuOptions,
  artifactTreeCyPromise,
  artifactTreeEdgeHandleOptions,
  artifactTreeResolveCy,
  DEFAULT_ZOOM,
  GraphStyle,
  MOTION_BLUE_OPACITY,
  setEdgeHandlesCore,
  USE_MOTION_BLUR,
} from "@/cytoscape";
import edgehandles from "cytoscape-edgehandles";
import { viewportModule } from "@/store";
import ArtifactTreeGraphLayout from "@/cytoscape/layout/artifact-tree-graph-layout";
import { CytoscapeOptions } from "cytoscape";
import { CytoCoreGraph } from "@/types/cytoscape/core/cyto-core-graph";

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
      plugin: nodeHtmlLabel,
      afterInit: () => undefined,
    },
    {
      plugin: klay,
      afterInit: () => undefined,
    },
    {
      plugin: automove,
      afterInit: () => undefined,
    },
    {
      plugin: contextMenus,
      afterInit(cy: CytoCore): void {
        cy.contextMenus(artifactTreeContextMenuOptions);
      },
    },
    {
      plugin: edgehandles,
      afterInit: async (cy: CytoCore) =>
        await setEdgeHandlesCore(
          artifactTreeCyPromise,
          cy.edgehandles(artifactTreeEdgeHandleOptions)
        ),
    },
  ],
  async afterInit(cy) {
    const cyPromise: Promise<CytoCore> = new Promise((resolve) => resolve(cy));
    const layout = new ArtifactTreeGraphLayout();
    await viewportModule.setGraphLayout(cyPromise, layout as IGraphLayout);
  },
};

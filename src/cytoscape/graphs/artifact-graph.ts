import { CytoscapeOptions } from "cytoscape";
import nodeHtmlLabel from "cytoscape-node-html-label";
import klay from "cytoscape-klay";
import automove from "cytoscape-automove";
import contextMenus from "cytoscape-context-menus";
import edgehandles from "cytoscape-edgehandles";
import { CytoCore, CytoCoreGraph } from "@/types";
import { viewportModule } from "@/store";
import {
  artifactTreeContextMenuOptions,
  artifactTreeEdgeHandleOptions,
  setEdgeHandlesCore,
} from "@/cytoscape/plugins";
import {
  DEFAULT_ARTIFACT_TREE_ZOOM,
  GraphStyle,
  MOTION_BLUE_OPACITY,
  USE_MOTION_BLUR,
} from "@/cytoscape/styles";
import { artifactTreeCyPromise, artifactTreeResolveCy } from "@/cytoscape/cy";

const artifactTreeConfig: CytoscapeOptions = {
  style: GraphStyle,
  motionBlur: USE_MOTION_BLUR,
  motionBlurOpacity: MOTION_BLUE_OPACITY,
  zoom: DEFAULT_ARTIFACT_TREE_ZOOM,
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
  async afterInit() {
    await viewportModule.setArtifactTreeLayout();
  },
};

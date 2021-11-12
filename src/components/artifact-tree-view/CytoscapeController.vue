<template>
  <cytoscape
    id="cy-container"
    :config="config"
    :preConfig="preConfig"
    :afterCreated="afterCreated"
  >
    <slot name="elements" />
  </cytoscape>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import contextMenus from "cytoscape-context-menus";
import nodeHtmlLabel from "cytoscape-node-html-label";
import klay from "cytoscape-klay";
import automove from "cytoscape-automove";
import edgehandles from "cytoscape-edgehandles";
import {
  resolveCy,
  contextMenuOptions,
  edgeHandleOptions,
  setEdgeHandlesCore,
  GRAPH_CONFIG,
} from "@/cytoscape";
import { viewportModule } from "@/store";
import { CytoCore, EdgeHandlersOptions, IGraphLayout } from "@/types";
import GraphLayout from "@/cytoscape/layout/graph-layout";

export default Vue.extend({
  props: {
    layout: {
      type: Object as PropType<IGraphLayout>,
      default: GraphLayout,
    },
    menuOptions: {
      type: Object,
      default: contextMenuOptions,
    },
    edgeHandleOptions: {
      type: Object as PropType<EdgeHandlersOptions>,
      default: edgeHandleOptions,
    },
  },
  data: () => {
    return {
      config: GRAPH_CONFIG,
    };
  },
  methods: {
    preConfig(cy: CytoCore) {
      try {
        nodeHtmlLabel(cy);
        klay(cy);
        automove(cy);
        contextMenus(cy);
        edgehandles(cy);
      } catch (e) {
        console.log("plugin already installed");
      }
    },
    async afterCreated(cy: CytoCore) {
      // waits for elements to be added
      // see: https://github.com/rcarcasses/vue-cytoscape/issues/50
      resolveCy(cy);
      const cyPromise: Promise<CytoCore> = new Promise((resolve) =>
        resolve(cy)
      );
      await viewportModule.setGraphLayout(
        cyPromise,
        this.layout as IGraphLayout
      );
      cy.contextMenus(this.menuOptions);
      await setEdgeHandlesCore(cy.edgehandles(this.edgeHandleOptions));
    },
  },
});
</script>

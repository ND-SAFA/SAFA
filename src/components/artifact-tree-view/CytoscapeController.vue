<template>
  <cytoscape
    :config="config"
    :preConfig="preConfig"
    :afterCreated="afterCreated"
    style="max-height: 300px"
  >
    <slot name="elements" />
  </cytoscape>
</template>

<script lang="ts">
import { GRAPH_CONFIG } from "@/cytoscape/styles/config/graph";
import { CytoCore } from "@/types/cytoscape";
import { edgeHandleOptions } from "@/cytoscape/edge-handles/options";
import { setEdgeHandlesCore } from "@/cytoscape/edge-handles/index";
import Vue from "vue";
import contextMenus from "cytoscape-context-menus";
import nodeHtmlLabel from "cytoscape-node-html-label";
import klay from "cytoscape-klay";
import automove from "cytoscape-automove";
import edgehandles from "cytoscape-edgehandles";
import { contextMenuOptions } from "@/cytoscape/context-menu";
import { resolveCy } from "@/cytoscape/cytoscape";
import { viewportModule } from "@/store";

export default Vue.extend({
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
      await viewportModule.setGraphLayout();
      cy.contextMenus(contextMenuOptions);
      await setEdgeHandlesCore(cy.edgehandles(edgeHandleOptions));
    },
  },
});
</script>

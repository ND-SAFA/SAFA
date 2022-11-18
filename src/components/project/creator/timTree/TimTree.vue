<template>
  <v-container>
    <flex-box justify="end">
      <v-btn text @click="handleResetGraph"> Reset Graph </v-btn>
    </flex-box>
    <generic-cytoscape-controller
      id="cytoscape-tim"
      :cyto-core-graph="cytoCoreGraph"
      :class="className"
    >
      <template v-slot:elements>
        <artifact-type-node
          v-for="artifactPanel in artifactPanels"
          :artifact-panel="artifactPanel"
          :key="artifactPanel.title"
        />
        <generic-graph-link
          v-for="tracePanel in tracePanels"
          :key="getTraceId(tracePanel)"
          :trace-definition="tracePanel.projectFile"
          :count="tracePanel.projectFile.traces.length"
          graph="tim"
        />
      </template>
    </generic-cytoscape-controller>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { TracePanel, CytoCoreGraph, ArtifactPanel } from "@/types";
import { getTraceId } from "@/util";
import { appStore, layoutStore } from "@/hooks";
import { timGraph, cyResetTim } from "@/cytoscape";
import {
  GenericGraphLink,
  GenericCytoscapeController,
  FlexBox,
} from "@/components/common";
import ArtifactTypeNode from "./ArtifactTypeNode.vue";

/**
 * Creates a Cytoscape graph containing artifact types are nodes
 * and links between them as edges.
 */
export default Vue.extend({
  name: "TimTree",
  components: {
    FlexBox,
    ArtifactTypeNode,
    GenericCytoscapeController,
    GenericGraphLink,
  },
  props: {
    tracePanels: {
      type: Array as PropType<TracePanel[]>,
      required: true,
    },
    artifactPanels: {
      type: Array as PropType<ArtifactPanel[]>,
      required: true,
    },
    inView: {
      type: Boolean,
      required: true,
    },
  },
  methods: {
    /**
     * Returns the trace id for a panel.
     * @param tracePanel - The panel to return the id for.
     */
    getTraceId(tracePanel: TracePanel): string {
      const traceFile = tracePanel.projectFile;
      return getTraceId(traceFile.sourceId, traceFile.targetId);
    },
    /**
     * Resets the cytoscape viewport and centers artifacts.
     */
    async handleResetGraph(): Promise<void> {
      cyResetTim();
    },
  },
  computed: {
    /**
     * @return The tim graph.
     */
    cytoCoreGraph(): CytoCoreGraph {
      return timGraph;
    },
    /**
     * @return The class name for the tim tree.
     */
    className(): string {
      if (!this.inView) {
        return "artifact-view disabled";
      } else if (!appStore.isLoading) {
        return "artifact-view visible elevation-3";
      } else {
        return "artifact-view";
      }
    },
  },
  watch: {
    /**
     * When in view, reset the tim graph.
     */
    async inView(inView: boolean): Promise<void> {
      if (!inView) return;

      await layoutStore.setTimTreeLayout();
    },
  },
});
</script>

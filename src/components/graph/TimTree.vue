<template>
  <v-container>
    <flex-box justify="end">
      <v-btn text @click="handleResetGraph"> Reset Graph </v-btn>
    </flex-box>
    <cytoscape-controller
      id="cytoscape-tim"
      :cyto-core-graph="cytoCoreGraph"
      :class="className"
    >
      <template v-slot:elements>
        <tim-node
          v-for="panel in artifactPanels"
          :key="panel.title"
          :count="panel.projectFile.artifacts.length"
          :artifact-type="panel.projectFile.type"
        />
        <tim-link
          v-for="panel in tracePanels"
          :key="panel.projectFile.sourceId + panel.projectFile.targetId"
          :count="panel.projectFile.traces.length"
          :target-type="panel.projectFile.targetId"
          :source-type="panel.projectFile.sourceId"
          :generated="panel.projectFile.isGenerated"
        />
      </template>
    </cytoscape-controller>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { TracePanel, CytoCoreGraph, ArtifactPanel } from "@/types";
import { appStore, layoutStore } from "@/hooks";
import { timGraph, cyResetTim } from "@/cytoscape";
import { FlexBox } from "@/components/common/layout";
import CytoscapeController from "./CytoscapeController.vue";
import { TimNode, TimLink } from "./tim";

/**
 * Creates a Cytoscape graph containing artifact types are nodes
 * and links between them as edges.
 */
export default Vue.extend({
  name: "TimTree",
  components: {
    FlexBox,
    CytoscapeController,
    TimNode,
    TimLink,
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

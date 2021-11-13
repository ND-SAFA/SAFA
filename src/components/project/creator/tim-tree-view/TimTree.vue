<template>
  <v-container class="elevation-3">
    <generic-cytoscape-controller :cytoCoreGraph="cytoCoreGraph">
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
        />
      </template>
    </generic-cytoscape-controller>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { TracePanel } from "@/types";
import { ArtifactPanel } from "@/components";
import { timGraph } from "@/cytoscape/graphs";
import { CytoCoreGraph } from "@/types/cytoscape";
import ArtifactTypeNode from "./ArtifactTypeNode.vue";
import {
  GenericGraphLink,
  GenericCytoscapeController,
} from "@/components/common";
import {
  ANIMATION_DURATION,
  TimGraphLayout,
  timTreeCyPromise,
} from "@/cytoscape";
import { appModule, viewportModule } from "@/store";

/**
 * Creates a Cytoscape graph containing artifact types are nodes
 * and links between them as edges.
 */
export default Vue.extend({
  components: {
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
    getTraceId(tracePanel: TracePanel): string {
      const traceFile = tracePanel.projectFile;
      return `${traceFile.source}-${traceFile.target}`;
    },
  },
  computed: {
    cytoCoreGraph(): CytoCoreGraph {
      return timGraph;
    },
  },
  watch: {
    async inView(inView: boolean): Promise<void> {
      if (inView) {
        await viewportModule.setTimTreeLayout();
      }
    },
  },
});
</script>

<template>
  <v-container class="elevation-3" style="width: 500px; height: 300px">
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
        />
      </template>
    </generic-cytoscape-controller>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { TracePanel } from "@/types";
import { ArtifactPanel } from "@/components";
import GenericCytoscapeController from "@/components/common/generic/GenericCytoscapeController.vue";
import GenericGraphLink from "@/components/common/generic/GenericGraphLink.vue";
import { timTreeDefinition } from "@/cytoscape/graphs";
import { CytoCoreGraph } from "@/types/cytoscape";
import ArtifactTypeNode from "./ArtifactTypeNode.vue";

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
  },
  methods: {
    getTraceId(tracePanel: TracePanel): string {
      const traceFile = tracePanel.projectFile;
      return `${traceFile.source}-${traceFile.target}`;
    },
  },
  computed: {
    cytoCoreGraph(): CytoCoreGraph {
      return timTreeDefinition;
    },
  },
});
</script>

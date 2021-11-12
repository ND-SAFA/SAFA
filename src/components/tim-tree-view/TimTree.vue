<template>
  <v-container class="elevation-3" style="width: 500px; height: 300px">
    <GenericCytoscapeController :graph-definition="graphDefinition">
      <template v-slot:elements>
        <ArtifactTypeNode
          v-for="artifactPanel in artifactPanels"
          :key="artifactPanel.title"
          :type="artifactPanel.title"
          :artifacts="artifactPanel.projectFile.artifacts"
        />
        <GenericGraphLink
          v-for="tracePanel in tracePanels"
          :key="getTraceId(tracePanel)"
          :trace-definition="tracePanel.projectFile"
        />
      </template>
    </GenericCytoscapeController>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { TracePanel } from "@/types";
import { ArtifactPanel } from "@/components";
import GenericCytoscapeController from "@/components/common/generic/GenericCytoscapeController.vue";
import ArtifactTypeNode from "./ArtifactTypeNode.vue";
import GenericGraphLink from "@/components/common/generic/GenericGraphLink.vue";
import { timTreeDefinition } from "@/types/cytoscape/graphs";
import { CytoCoreGraph } from "@/types/cytoscape";

export default Vue.extend({
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
    graphDefinition(): CytoCoreGraph {
      return timTreeDefinition;
    },
  },
  components: {
    ArtifactTypeNode,
    GenericCytoscapeController,
    GenericGraphLink,
  },
});
</script>

<template>
  <generic-cytoscape-controller :cyto-core-graph="cytoCoreGraph">
    <template v-slot:elements>
      <artifact-node
        v-for="artifact in artifacts"
        :key="artifact.id"
        :artifact-definition="artifact"
        :opacity="getArtifactOpacity(artifact.id)"
      />
      <generic-graph-link
        v-for="traceLink in traces"
        :key="traceLink.traceLinkId"
        :trace-definition="traceLink"
        @click:right="onLinkRightClick"
      />
      <generic-graph-link
        v-for="traceLink in subtreeLinks"
        :key="traceLink.traceLinkId"
        :trace-definition="traceLink"
      />
      <trace-link-approval-modal
        v-if="selectedLink !== undefined"
        :is-open="isTraceModalOpen"
        :link="selectedLink"
        @close="onTraceModalClose"
      />
    </template>
  </generic-cytoscape-controller>
</template>

<script lang="ts">
import Vue from "vue";
import {
  TraceLink,
  TraceLinkDisplayData,
  Artifact,
  CytoCoreGraph,
} from "@/types";
import {
  artifactModule,
  artifactSelectionModule,
  subtreeModule,
  traceModule,
  viewportModule,
} from "@/store";
import { artifactTreeGraph } from "@/cytoscape";
import {
  GenericGraphLink,
  GenericCytoscapeController,
} from "@/components/common";
import { TraceLinkApprovalModal } from "@/components/approve-links-view";
import ArtifactNode from "./ArtifactNode.vue";

export default Vue.extend({
  name: "artifact-tree",
  components: {
    ArtifactNode,
    GenericGraphLink,
    TraceLinkApprovalModal,
    GenericCytoscapeController,
  },
  data: () => {
    return {
      isTraceModalOpen: false,
      selectedLink: undefined as TraceLinkDisplayData | undefined,
      artifactsInView: [] as string[],
    };
  },
  computed: {
    cytoCoreGraph(): CytoCoreGraph {
      return artifactTreeGraph;
    },
    artifactHashMap(): Record<string, Artifact> {
      return artifactModule.getArtifactsById;
    },
    artifacts(): Artifact[] {
      return artifactModule.artifacts;
    },
    traces(): TraceLink[] {
      return traceModule.traces;
    },
    subtreeLinks() {
      return subtreeModule.getSubtreeLinks;
    },
    nodesInView(): string[] {
      return viewportModule.getNodesInView;
    },
    unselectedNodeOpacity(): number {
      return artifactSelectionModule.getUnselectedNodeOpacity;
    },
    hiddenSubtreeIds(): string[] {
      return subtreeModule.getHiddenSubtreeIds;
    },
  },
  mounted() {
    this.artifactsInView = this.nodesInView;
  },
  watch: {
    nodesInView(): void {
      this.setNodesInView();
    },
  },
  methods: {
    setNodesInView(): void {
      this.artifactsInView = this.nodesInView;
    },
    getArtifactOpacity(id: string): number {
      if (this.hiddenSubtreeIds.includes(id)) {
        return 0;
      } else if (this.artifactsInView.includes(id)) {
        return 1;
      } else {
        return this.unselectedNodeOpacity;
      }
    },
    onLinkRightClick(traceLink: TraceLink): void {
      this.selectedLink = {
        ...traceLink,
        sourceBody: this.artifactHashMap[traceLink.sourceId].body,
        targetBody: this.artifactHashMap[traceLink.targetId].body,
      };
      this.isTraceModalOpen = true;
    },
    onTraceModalClose(): void {
      this.selectedLink = undefined;
      this.isTraceModalOpen = false;
    },
  },
});
</script>

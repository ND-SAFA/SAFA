<template>
  <generic-cytoscape-controller
    :cyto-core-graph="cytoCoreGraph"
    :class="isVisible ? 'artifact-tree visible' : 'artifact-tree'"
  >
    <template v-slot:elements>
      <artifact-node
        v-for="artifact in artifacts"
        :key="artifact.id"
        :artifact-definition="artifact"
        :opacity="getArtifactOpacity(artifact.id)"
      />
      <generic-graph-link
        v-for="traceLink in traceLinks"
        :key="traceLink.traceLinkId"
        :trace-definition="traceLink"
        @click:right="handleLinkRightClick"
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
        @close="handleTraceModalClose"
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
  appModule,
  artifactModule,
  artifactSelectionModule,
  deltaModule,
  documentModule,
  subtreeModule,
  traceModule,
  viewportModule,
} from "@/store";
import { artifactTreeGraph } from "@/cytoscape";
import {
  GenericGraphLink,
  GenericCytoscapeController,
  TraceLinkApprovalModal,
} from "@/components/common";
import ArtifactNode from "./ArtifactNode.vue";

export default Vue.extend({
  name: "ArtifactTree",
  components: {
    ArtifactNode,
    GenericGraphLink,
    TraceLinkApprovalModal,
    GenericCytoscapeController,
  },
  data() {
    return {
      isTraceModalOpen: false,
      selectedLink: undefined as TraceLinkDisplayData | undefined,
      artifactsInView: [] as string[],
    };
  },
  computed: {
    /**
     * @return Whether the app is currently loading.
     */
    isLoading(): boolean {
      return appModule.getIsLoading;
    },
    /**
     * @return The artifact tree graph.
     */
    cytoCoreGraph(): CytoCoreGraph {
      return artifactTreeGraph;
    },
    /**
     * @return All visible artifacts.
     */
    artifacts(): Artifact[] {
      return artifactModule.artifacts;
    },
    /**
     * @return All visible trace links.
     */
    traceLinks(): TraceLink[] {
      return deltaModule.inDeltaView
        ? traceModule.traces
        : traceModule.nonDeclinedTraces;
    },
    /**
     * @return All subtree trace links.
     */
    subtreeLinks() {
      return subtreeModule.getSubtreeLinks;
    },

    /**
     * @return The artifact ids currently in view.
     */
    nodesInView(): string[] {
      return viewportModule.getNodesInView;
    },
    /**
     * @return The opacity of unselected nodes.
     */
    unselectedNodeOpacity(): number {
      return artifactSelectionModule.getUnselectedNodeOpacity;
    },
    /**
     * @return The artifact ids that are currently hidden in closed subtrees.
     */
    hiddenSubtreeIds(): string[] {
      return subtreeModule.getHiddenSubtreeIds;
    },
    /**
     * @return Whether to render the artifact tree.
     */
    isVisible(): boolean {
      return !this.isLoading && !documentModule.isTableDocument;
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
    /**
     * Sets whether the artifacts are in view.
     */
    setNodesInView(): void {
      this.artifactsInView = this.nodesInView;
    },
    /**
     * Returns the opacity of an artifact.
     * @param id - The artifact to get the opacity for.
     * @return The artifact's opacity.
     */
    getArtifactOpacity(id: string): number {
      if (this.hiddenSubtreeIds.includes(id)) {
        return 0;
      } else if (this.artifactsInView.includes(id)) {
        return 1;
      } else {
        return this.unselectedNodeOpacity;
      }
    },
    /**
     * Selects a clicked trace link and opens the link modal.
     * @param traceLink - The trace link to select.
     */
    handleLinkRightClick(traceLink: TraceLink): void {
      const artifactsById = artifactModule.getArtifactsById;

      this.selectedLink = {
        ...traceLink,
        sourceBody: artifactsById[traceLink.sourceId].body,
        targetBody: artifactsById[traceLink.targetId].body,
      };
      this.isTraceModalOpen = true;
    },
    /**
     * Closes the trace link modal.
     */
    handleTraceModalClose(): void {
      this.selectedLink = undefined;
      this.isTraceModalOpen = false;
    },
  },
});
</script>

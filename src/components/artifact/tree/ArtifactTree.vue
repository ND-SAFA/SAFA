<template>
  <generic-cytoscape-controller
    id="cytoscape-artifact"
    :cyto-core-graph="cytoCoreGraph"
    :class="className"
    data-cy="view-artifact-tree"
  >
    <template v-slot:elements>
      <artifact-node
        v-for="artifact in artifacts"
        :key="artifact.id"
        :artifact-definition="artifact"
        :hidden="isArtifactHidden(artifact.id)"
        :faded="isArtifactFaded(artifact.id)"
      />
      <generic-graph-link
        v-for="traceLink in traceLinks"
        :key="traceLink.traceLinkId"
        :trace-definition="traceLink"
        :faded="isTraceLinkFaded(traceLink)"
        @click:right="handleLinkRightClick"
        graph="artifact"
      />
      <generic-graph-link
        v-for="traceLink in subtreeLinks"
        :key="traceLink.traceLinkId"
        :trace-definition="traceLink"
        graph="artifact"
      />
    </template>
  </generic-cytoscape-controller>
</template>

<script lang="ts">
import Vue from "vue";
import { Route } from "vue-router";
import { TraceLinkModel, ArtifactModel, CytoCoreGraph } from "@/types";
import {
  appStore,
  artifactStore,
  traceStore,
  documentStore,
  deltaStore,
  subtreeStore,
  selectionStore,
  layoutStore,
} from "@/hooks";
import { Routes } from "@/router";
import { artifactTreeGraph, cyResetTree } from "@/cytoscape";
import {
  GenericGraphLink,
  GenericCytoscapeController,
} from "@/components/common";
import ArtifactNode from "./ArtifactNode.vue";

export default Vue.extend({
  name: "ArtifactTree",
  components: {
    ArtifactNode,
    GenericGraphLink,
    GenericCytoscapeController,
  },
  data() {
    return {
      artifactsInView: [] as string[],
    };
  },
  computed: {
    /**
     * @return Whether the tree should be rendered at all.
     */
    isInView(): boolean {
      return !documentStore.isTableDocument;
    },
    /**
     * @return The class name for the artifact tree.
     */
    className(): string {
      if (!this.isInView) {
        return "artifact-view disabled";
      } else if (!appStore.isLoading) {
        return "artifact-view visible";
      } else {
        return "artifact-view";
      }
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
    artifacts(): ArtifactModel[] {
      return artifactStore.currentArtifacts;
    },
    /**
     * @return All visible trace links.
     */
    traceLinks(): TraceLinkModel[] {
      return deltaStore.inDeltaView
        ? traceStore.currentTraces
        : traceStore.visibleTraces;
    },
    /**
     * @return All subtree trace links.
     */
    subtreeLinks() {
      return subtreeStore.subtreeLinks;
    },
    /**
     * @return The artifact ids currently in view.
     */
    nodesInView(): string[] {
      return selectionStore.artifactsInView;
    },
    /**
     * @return The artifact ids that are currently hidden in closed subtrees.
     */
    hiddenSubtreeIds(): string[] {
      return subtreeStore.hiddenSubtreeNodes;
    },
  },
  mounted() {
    this.artifactsInView = this.nodesInView;
    layoutStore.resetLayout();
  },
  watch: {
    nodesInView(): void {
      this.artifactsInView = this.nodesInView;
    },
    /**
     * Re-centers the graph when switching from the table to the tree.
     */
    isInView(inView: boolean): void {
      if (!inView) return;

      appStore.onLoadStart();

      setTimeout(() => {
        cyResetTree();
        appStore.onLoadEnd();
      }, 200);
    },
    /**
     * Resets the layout when the route changes.
     */
    $route(to: Route) {
      if (to.path !== Routes.ARTIFACT) return;

      layoutStore.resetLayout();
    },
  },
  methods: {
    /**
     * Returns whether to fade an artifact.
     * @param id - The artifact to check.
     * @return Whether to fade.
     */
    isArtifactFaded(id: string): boolean {
      return !this.artifactsInView.includes(id);
    },
    /**
     * Returns whether to hide an artifact.
     * @param id - The artifact to check.
     * @return Whether to hide.
     */
    isArtifactHidden(id: string): boolean {
      return this.hiddenSubtreeIds.includes(id);
    },
    /**
     * Returns whether to fade a trace link.
     * @param link - The trace link to check.
     * @return Whether to fade.
     */
    isTraceLinkFaded(link: TraceLinkModel): boolean {
      return (
        !this.artifactsInView.includes(link.targetId) ||
        !this.artifactsInView.includes(link.sourceId)
      );
    },
    /**
     * Selects a clicked trace link and opens the link modal.
     * @param traceLink - The trace link to select.
     */
    handleLinkRightClick(traceLink: TraceLinkModel): void {
      selectionStore.selectTraceLink(traceLink);
    },
  },
});
</script>

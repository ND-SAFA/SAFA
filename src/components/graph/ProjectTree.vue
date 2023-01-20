<template>
  <cytoscape-controller
    id="cytoscape-artifact"
    :cyto-core-graph="cytoCoreGraph"
    :class="className"
    data-cy="view-artifact-tree"
  >
    <template v-slot:elements v-if="isTreeMode">
      <artifact-node
        v-for="artifact in artifacts"
        :key="artifact.id"
        :artifact="artifact"
        :hidden="isArtifactHidden(artifact.id)"
        :faded="isArtifactFaded(artifact.id)"
      />
      <trace-link
        v-for="traceLink in traceLinks"
        :key="traceLink.traceLinkId"
        :trace="traceLink"
        :faded="isTraceLinkFaded(traceLink)"
      />
      <trace-link
        v-for="traceLink in subtreeLinks"
        :key="traceLink.traceLinkId"
        :trace="traceLink"
      />
    </template>
    <template v-slot:elements v-else>
      <tim-node
        v-for="level in tim.artifacts"
        :key="level.artifactType"
        :count="level.count"
        :artifact-type="level.artifactType"
      />
      <tim-link
        v-for="matrix in tim.traces"
        :key="matrix.sourceType + matrix.targetType"
        :count="matrix.count"
        :target-type="matrix.targetType"
        :source-type="matrix.sourceType"
      />
    </template>
  </cytoscape-controller>
</template>

<script lang="ts">
import Vue from "vue";
import { Route } from "vue-router";
import {
  TraceLinkSchema,
  ArtifactSchema,
  CytoCoreGraph,
  TimSchema,
} from "@/types";
import {
  appStore,
  artifactStore,
  traceStore,
  deltaStore,
  subtreeStore,
  selectionStore,
  layoutStore,
  typeOptionsStore,
} from "@/hooks";
import { Routes } from "@/router";
import { artifactTreeGraph, cyResetTree } from "@/cytoscape";
import CytoscapeController from "./CytoscapeController.vue";
import { ArtifactNode, TraceLink } from "./tree";
import { TimNode, TimLink } from "./tim";

/**
 * Renders a tree of project data.
 * Will either render the TIM tree, or artifacts and trace links, depending on the graph mode.
 */
export default Vue.extend({
  name: "ProjectTree",
  components: {
    CytoscapeController,
    ArtifactNode,
    TraceLink,
    TimNode,
    TimLink,
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
      return !layoutStore.isTableMode;
    },
    /**
     * @return Whether the tree is in tree mode, rather than TIM mode.
     */
    isTreeMode(): boolean {
      return layoutStore.isTreeMode;
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
    artifacts(): ArtifactSchema[] {
      return artifactStore.currentArtifacts;
    },
    /**
     * @return All visible trace links.
     */
    traceLinks(): TraceLinkSchema[] {
      return deltaStore.inDeltaView
        ? traceStore.currentTraces
        : traceStore.visibleTraces;
    },
    /**
     * @return All subtree trace links.
     */
    subtreeLinks(): TraceLinkSchema[] {
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
    /**
     * @return The TIM structure of this project.
     */
    tim(): TimSchema {
      return typeOptionsStore.tim;
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
     * Resets the layout when the mode changes.
     */
    isTreeMode() {
      layoutStore.resetLayout();
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
    isTraceLinkFaded(link: TraceLinkSchema): boolean {
      return (
        !this.artifactsInView.includes(link.targetId) ||
        !this.artifactsInView.includes(link.sourceId)
      );
    },
  },
});
</script>

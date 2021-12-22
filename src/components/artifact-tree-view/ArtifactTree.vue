<template>
  <generic-cytoscape-controller :cyto-core-graph="cytoCoreGraph">
    <template v-slot:elements>
      <artifact-node
        v-for="artifact in artifacts"
        :key="artifact.name"
        :artifact-definition="artifact"
        :opacity="getArtifactOpacity(artifact.name, artifact.id)"
      />
      <generic-graph-link
        v-for="traceLink in traces"
        :key="`${traceLink.source}-${traceLink.target}`"
        :trace-definition="traceLink"
        @click:right="onLinkRightClick"
      />
      <generic-graph-link
        v-for="traceLink in subtreeLinks"
        :key="`${traceLink.source}-${traceLink.target}`"
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
import { TraceLink, TraceLinkDisplayData, Artifact } from "@/types";
import { CytoCoreGraph } from "@/types/cytoscape/core";
import {
  artifactSelectionModule,
  projectModule,
  subtreeModule,
  viewportModule,
} from "@/store";
import {
  GenericGraphLink,
  GenericCytoscapeController,
} from "@/components/common";
import { TraceLinkApprovalModal } from "@/components/approve-links-view";
import ArtifactNode from "./ArtifactNode.vue";
import { artifactTreeGraph } from "@/cytoscape";

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
      return projectModule.getArtifactHashmap;
    },
    artifacts(): Artifact[] {
      return projectModule.artifacts;
    },
    traces() {
      return projectModule.getProject.traces;
    },
    subtreeLinks() {
      return subtreeModule.getSubtreeLinks;
    },
    project() {
      return projectModule.getProject;
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
    getArtifactOpacity(name: string, id: string): number {
      if (this.hiddenSubtreeIds.includes(id)) {
        return 0;
      } else if (this.artifactsInView.includes(name)) {
        return 1;
      } else {
        return this.unselectedNodeOpacity;
      }
    },
    onLinkRightClick(traceLink: TraceLink): void {
      this.selectedLink = {
        ...traceLink,
        sourceBody: this.artifactHashMap[traceLink.source].body,
        targetBody: this.artifactHashMap[traceLink.target].body,
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

<template>
  <v-container class="elevation-3">
    <GenericCytoscapeController :cytoCoreGraph="cytoCoreGraph">
      <template v-slot:elements>
        <ArtifactNode
          v-for="artifact in artifacts"
          :key="artifact.name"
          :artifact-definition="artifact"
          :opacity="getArtifactOpacity(artifact.name)"
        />
        <GenericGraphLink
          v-for="traceLink in traces"
          :key="`${traceLink.source}-${traceLink.target}`"
          :trace-definition="traceLink"
          @right-click="onLinkRightClick"
        />
      </template>
    </GenericCytoscapeController>
    <TraceLinkApprovalModal
      v-if="selectedLink !== undefined"
      :is-open="isTraceModalOpen"
      :link="selectedLink"
      @close="onTraceModalClose"
    />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { TraceLink, TraceLinkDisplayData, Artifact } from "@/types";
import { CytoCoreGraph } from "@/types/cytoscape/core";
import {
  artifactSelectionModule,
  projectModule,
  viewportModule,
} from "@/store";
import {
  TraceLinkApprovalModal,
  GenericGraphLink,
  GenericCytoscapeController,
} from "@/components";
import ArtifactNode from "./ArtifactNode.vue";
import { artifactTreeGraph } from "@/cytoscape/graphs/artifact-tree-definition";

export default Vue.extend({
  name: "artifact-view",
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
      return projectModule.getArtifacts;
    },
    traces() {
      return projectModule.getProject.traces;
    },
    project() {
      return projectModule.getProject;
    },
    nodesInView(): Promise<string[]> {
      return viewportModule.getNodesInView;
    },
    unselectedNodeOpacity(): number {
      return artifactSelectionModule.getUnselectedNodeOpacity;
    },
  },
  mounted() {
    this.nodesInView.then((artifactIds: string[]) => {
      this.artifactsInView = artifactIds;
    });
  },
  watch: {
    nodesInView(): void {
      this.setNodesInView();
    },
  },
  methods: {
    setNodesInView(): void {
      this.nodesInView.then((artifactIds: string[]) => {
        this.artifactsInView = artifactIds;
      });
    },
    getArtifactOpacity(name: string): number {
      if (this.artifactsInView.includes(name)) {
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

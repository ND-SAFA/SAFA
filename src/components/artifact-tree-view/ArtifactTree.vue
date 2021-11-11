<template>
  <v-container class="elevation-3">
    <CytoscapeController>
      <template v-slot:elements>
        <ArtifactNode
          v-for="artifact in artifacts"
          :key="artifact.name"
          :artifact-definition="artifact"
          :opacity="getArtifactOpacity(artifact.name)"
        />
        <TraceLinkEdge
          v-for="traceLink in traces"
          :key="`${traceLink.source}-${traceLink.target}`"
          :trace-definition="traceLink"
          @right-click="onLinkRightClick"
        />
      </template>
    </CytoscapeController>
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
import {
  artifactSelectionModule,
  projectModule,
  viewportModule,
} from "@/store";
import { TraceLinkApprovalModal } from "@/components";
import CytoscapeController from "./CytoscapeController.vue";
import TraceLinkEdge from "./TraceLinkEdge.vue";
import ArtifactNode from "./ArtifactNode.vue";

export default Vue.extend({
  name: "artifact-view",
  components: {
    ArtifactNode,
    TraceLinkEdge,
    TraceLinkApprovalModal,
    CytoscapeController,
  },
  data: () => {
    return {
      isTraceModalOpen: false,
      selectedLink: undefined as TraceLinkDisplayData | undefined,
      artifactsInView: [] as string[],
    };
  },
  computed: {
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
  watch: {
    nodesInView(artifactIdsPromise: Promise<string[]>): void {
      artifactIdsPromise.then((artifactIds: string[]) => {
        this.artifactsInView = artifactIds;
      });
    },
  },
  methods: {
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

<template>
  <cytoscape-controller
    id="cytoscape-artifact"
    :cyto-core-graph="artifactTreeGraph"
    :class="className"
    data-cy="view-artifact-tree"
  >
    <template v-if="isTreeMode" #elements>
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
    <template v-else #elements>
      <tim-node
        v-for="level in tim.artifacts"
        :key="level.typeId"
        :count="level.count"
        :artifact-type="level.name"
      />
      <tim-link
        v-for="matrix in tim.traces"
        :key="matrix.sourceType + matrix.targetType"
        :count="matrix.count"
        :target-type="matrix.targetType"
        :source-type="matrix.sourceType"
        :generated="matrix.generatedCount > 0"
      />
    </template>
  </cytoscape-controller>
</template>

<script lang="ts">
/**
 * Renders a tree of project data.
 * Will either render the TIM tree, or artifacts and trace links, depending on the graph mode.
 */
export default {
  name: "ProjectTree",
};
</script>

<script setup lang="ts">
import { watch, ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import { TraceLinkSchema } from "@/types";
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

const currentRoute = useRoute();
const artifactsInView = ref<string[]>([]);

const isInView = computed(() => !layoutStore.isTableMode);
const isTreeMode = computed(() => layoutStore.isTreeMode);

const artifacts = computed(() => artifactStore.currentArtifacts);
const nodesInView = computed(() => selectionStore.artifactsInView);

const traceLinks = computed(() =>
  deltaStore.inDeltaView ? traceStore.currentTraces : traceStore.visibleTraces
);
const subtreeLinks = computed(() => subtreeStore.subtreeLinks);
const hiddenSubtreeIds = computed(() => subtreeStore.hiddenSubtreeNodes);

const tim = computed(() => typeOptionsStore.tim);

const className = computed(() => {
  if (!isInView.value) {
    return "artifact-view disabled";
  } else if (!appStore.isLoading) {
    return "artifact-view visible";
  } else {
    return "artifact-view";
  }
});

/**
 * Returns whether to fade an artifact.
 * @param id - The artifact to check.
 * @return Whether to fade.
 */
function isArtifactFaded(id: string): boolean {
  return !artifactsInView.value.includes(id);
}

/**
 * Returns whether to hide an artifact.
 * @param id - The artifact to check.
 * @return Whether to hide.
 */
function isArtifactHidden(id: string): boolean {
  return hiddenSubtreeIds.value.includes(id);
}

/**
 * Returns whether to fade a trace link.
 * @param link - The trace link to check.
 * @return Whether to fade.
 */
function isTraceLinkFaded(link: TraceLinkSchema): boolean {
  return (
    !artifactsInView.value.includes(link.targetId) ||
    !artifactsInView.value.includes(link.sourceId)
  );
}

onMounted(() => {
  artifactsInView.value = nodesInView.value;
  layoutStore.resetLayout();
});

/** Resets the layout when the route changes. */
watch(
  () => currentRoute.path,
  () => {
    if (currentRoute.path !== Routes.ARTIFACT) return;

    layoutStore.resetLayout();
  }
);

watch(
  () => nodesInView.value,
  () => {
    artifactsInView.value = nodesInView.value;
  }
);

watch(
  () => isInView.value,
  (inView) => {
    if (!inView) return;

    appStore.onLoadStart();

    setTimeout(() => {
      cyResetTree();
      appStore.onLoadEnd();
    }, 200);
  }
);

watch(
  () => isTreeMode.value,
  () => layoutStore.resetLayout()
);
</script>

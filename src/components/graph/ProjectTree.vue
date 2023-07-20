<template>
  <cytoscape-controller
    id="cytoscape-artifact"
    :cyto-core-graph="artifactTreeGraph"
    :class="className"
    data-cy="view-artifact-tree"
    @click="handleClick"
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
    </template>
    <template v-else #elements>
      <tim-node
        v-for="level in Object.values(tim.artifacts)"
        :key="level.typeId"
        :count="level.count"
        :artifact-type="level.name"
        :icon="level.icon"
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
import { watch, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import { EventObject } from "cytoscape";
import { DetailsOpenState, TraceLinkSchema } from "@/types";
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
import { artifactTreeGraph, disableDrawMode } from "@/cytoscape";
import CytoscapeController from "./CytoscapeController.vue";
import { ArtifactNode, TraceLink } from "./tree";
import { TimNode, TimLink } from "./tim";

const currentRoute = useRoute();

const isInView = computed(() => !layoutStore.isTableMode);
const isTreeMode = computed(() => layoutStore.isTreeMode);

const artifacts = computed(() => artifactStore.currentArtifacts);
const nodesInView = computed(() => selectionStore.artifactsInView);

const traceLinks = computed(() =>
  deltaStore.inDeltaView ? traceStore.currentTraces : traceStore.visibleTraces
);
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
  return !nodesInView.value.includes(id);
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
    !nodesInView.value.includes(link.targetId) ||
    !nodesInView.value.includes(link.sourceId)
  );
}

/**
 * Handles a click event on the graph.
 * When a click is registered on the background:
 * - Draw mode is disabled.
 * - Selections are cleared if a save panel is not open.
 * @param event - The click event.
 */
function handleClick(event: EventObject): void {
  if (event.target !== event.cy) return;

  disableDrawMode();

  if (
    (["document", "saveArtifact", "saveTrace"] as DetailsOpenState[]).includes(
      appStore.isDetailsPanelOpen
    )
  )
    return;

  selectionStore.clearSelections(true);
}

onMounted(() => {
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
  () => isInView.value,
  (inView) => {
    if (!inView) return;

    appStore.onLoadStart();

    setTimeout(() => {
      layoutStore.resetLayout();
      appStore.onLoadEnd();
    }, 200);
  }
);

watch(
  () => isTreeMode.value,
  () => {
    layoutStore.resetLayout();
  }
);
</script>

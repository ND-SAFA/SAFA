<template>
  <cytoscape
    id="cytoscape-artifact"
    :graph="cyStore.projectGraph"
    :class="className"
    data-cy="view-artifact-tree"
    @click="handleClick"
  >
    <template v-if="isTreeMode">
      <artifact-node
        v-for="artifact in artifacts"
        :key="artifact.id"
        :artifact="artifact"
        :artifacts-in-view="artifactsInView"
      />
      <trace-link
        v-for="traceLink in traceLinks"
        :key="traceLink.traceLinkId"
        :trace="traceLink"
        :artifacts-in-view="artifactsInView"
      />
    </template>
    <template v-else>
      <tim-node
        v-for="type in artifactTypes"
        :key="type.typeId"
        :count="type.count"
        :artifact-type="type.name"
        :icon="type.icon"
      />
      <tim-link
        v-for="matrix in traceMatrices"
        :key="matrix.sourceType + matrix.targetType"
        :count="matrix.count"
        :target-type="matrix.targetType"
        :source-type="matrix.sourceType"
        :generated="matrix.generatedCount > 0"
      />
    </template>

    <template v-if="isTreeMode" #context-menu>
      <artifact-menu />
    </template>
    <template v-else #context-menu>
      <tim-menu />
    </template>
  </cytoscape>
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
import { DetailsOpenState } from "@/types";
import {
  appStore,
  artifactStore,
  traceStore,
  deltaStore,
  selectionStore,
  layoutStore,
  timStore,
  cyStore,
} from "@/hooks";
import { Routes } from "@/router";
import { disableDrawMode } from "@/cytoscape";
import { Cytoscape } from "./base";
import { ArtifactNode, TraceLink, ArtifactMenu } from "./artifact";
import { TimNode, TimLink, TimMenu } from "./tim";

const currentRoute = useRoute();

const isInView = computed(() => !layoutStore.isTableMode);
const isTreeMode = computed(() => layoutStore.isTreeMode);

const artifacts = computed(() => artifactStore.currentArtifacts);
const artifactsInView = computed(() => selectionStore.artifactsInView);

const traceLinks = computed(() =>
  deltaStore.inDeltaView ? traceStore.currentTraces : traceStore.visibleTraces
);

const artifactTypes = computed(() => timStore.artifactTypes);
const traceMatrices = computed(() => timStore.traceMatrices);

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
 * Handles a click event on the graph.
 * When a click is registered on the background:
 * - Draw mode is disabled.
 * - Selections are cleared if a save panel is not open.
 * @param event - The click event.
 */
function handleClick(event: EventObject): void {
  if (event.target !== event.cy) return;

  if (appStore.popups.drawTrace) {
    disableDrawMode();
  }

  if (
    (
      [
        "document",
        "saveArtifact",
        "saveTrace",
        "generateArtifact",
        "generateTrace",
      ] as DetailsOpenState[]
    ).includes(appStore.popups.detailsPanel)
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

    layoutStore.resetLayout();
  }
);

watch(
  () => isTreeMode.value,
  () => {
    layoutStore.resetLayout();
  }
);
</script>

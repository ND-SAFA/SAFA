<template>
  <empty-graph-buttons />
  <graph-buttons />
  <graph-fab />

  <cytoscape
    id="cytoscape-artifact"
    :graph="graph"
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
        :key="matrix.id"
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
import { watch, computed, onMounted, ref } from "vue";
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
  traceApiStore,
  traceMatrixApiStore,
} from "@/hooks";
import { Routes } from "@/router";
import { Cytoscape } from "./base";
import { ArtifactNode, TraceLink, ArtifactMenu } from "./artifact";
import { TimNode, TimLink, TimMenu } from "./tim";
import { EmptyGraphButtons, GraphButtons, GraphFab } from "./button";

const currentRoute = useRoute();

const graph = ref(
  cyStore.buildProjectGraph({
    canCreateTrace: (source, target) =>
      traceStore.isLinkAllowed(source.data(), target.data()) === true,
    handleCreateTrace: (source, target) => {
      if (source.data()?.graph === "tree") {
        traceApiStore.handleCreate(source.data(), target.data());
      } else {
        traceMatrixApiStore.handleCreate(
          source.data().artifactType,
          target.data().artifactType
        );
      }
    },
  })
);

const isInView = computed(
  () => layoutStore.isTreeMode || layoutStore.isTimMode
);
const isTreeMode = computed(() => layoutStore.isTreeMode);

const artifacts = computed(() => artifactStore.currentArtifacts);
const artifactsInView = computed(() => artifactStore.artifactsInView);

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
    cyStore.drawMode("disable");
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

  selectionStore.clearSelections();
}

function handleReset(): void {
  selectionStore.clearSelections();
  layoutStore.setGraphLayout();
}

onMounted(() => handleReset());

/** Resets the layout when the route changes. */
watch(
  () => currentRoute.path,
  () => {
    if (currentRoute.path !== Routes.ARTIFACT) return;

    handleReset();
  }
);

watch(
  () => isInView.value,
  (inView) => {
    if (!inView) return;

    handleReset();
  }
);

watch(
  () => isTreeMode.value,
  () => handleReset()
);
</script>

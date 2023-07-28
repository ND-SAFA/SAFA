<template>
  <q-page-sticky
    v-if="display"
    position="bottom-left"
    :offset="fabPos"
    class="artifact-fab"
  >
    <q-fab
      v-model="open"
      v-touch-pan.prevent.mouse="handleMoveFab"
      direction="up"
      vertical-actions-align="left"
      :color="drawMode ? 'secondary' : 'primary'"
      active-icon="mdi-close"
      :icon="drawMode ? 'mdi-ray-start-arrow' : 'mdi-plus'"
      :disable="draggingFab"
      data-cy="button-fab-toggle"
    >
      <q-fab-action
        outline
        label="Generate Trace Links"
        icon="mdi-chart-timeline-variant-shimmer"
        class="bg-neutral"
        color="primary"
        data-cy="button-fab-generate-trace"
        @click="appStore.openDetailsPanel('generateTrace')"
      />
      <q-fab-action
        outline
        label="Generate Artifacts"
        icon="mdi-monitor-shimmer"
        class="bg-neutral"
        color="primary"
        data-cy="button-fab-generate-artifact"
        @click="appStore.openDetailsPanel('generateArtifact')"
      />
      <q-fab-action
        outline
        :label="drawMode ? 'Cancel Draw Mode' : 'Draw Links'"
        :icon="drawMode ? 'mdi-close' : 'mdi-ray-start-arrow'"
        class="bg-neutral"
        data-cy="button-fab-draw-trace"
        @click="toggleDrawMode"
      />
      <q-fab-action
        v-if="isTreeMode"
        outline
        label="Create Trace Link"
        icon="mdi-ray-start-end"
        class="bg-neutral"
        data-cy="button-fab-create-trace"
        @click="appStore.openDetailsPanel('saveTrace')"
      />
      <q-fab-action
        v-if="isTreeMode"
        outline
        label="Create Artifact"
        icon="mdi-folder-plus-outline"
        class="bg-neutral"
        data-cy="button-fab-create-artifact"
        @click="appStore.openArtifactCreatorTo({ isNewArtifact: true })"
      />
    </q-fab>
    <icon-button
      v-if="drawMode"
      icon="cancel"
      tooltip="Cancel draw mode"
      class="q-ml-sm"
      @click="disableDrawMode"
    />
  </q-page-sticky>
</template>

<script lang="ts">
/**
 * Displays action buttons for the artifact tree graph.
 */
export default {
  name: "GraphFab",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { appStore, layoutStore, projectStore, sessionStore } from "@/hooks";
import { disableDrawMode, toggleDrawMode } from "@/cytoscape";
import IconButton from "@/components/common/button/IconButton.vue";

const open = ref(false);
const fabPos = ref([18, 18]);
const draggingFab = ref(false);

const isTreeMode = computed(
  () => !appStore.isLoading && layoutStore.isTreeMode
);
const drawMode = computed(() => appStore.isCreateLinkEnabled);
const display = computed(
  () =>
    projectStore.isProjectDefined && sessionStore.isEditor(projectStore.project)
);

/**
 * Handles moving the fab tro another location.
 * @param ev - The move event.
 */
function handleMoveFab(ev: {
  isFirst?: boolean;
  isFinal?: boolean;
  delta: { x: number; y: number };
}) {
  draggingFab.value = ev.isFirst !== true && ev.isFinal !== true;

  fabPos.value = [fabPos.value[0] + ev.delta.x, fabPos.value[1] - ev.delta.y];
}
</script>

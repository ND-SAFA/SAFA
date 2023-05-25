<template>
  <q-page-sticky
    v-if="doDisplay"
    position="bottom-left"
    :offset="fabPos"
    class="artifact-fab"
  >
    <q-fab
      v-model="open"
      v-touch-pan.prevent.mouse="handleMoveFab"
      direction="up"
      vertical-actions-align="left"
      :color="isCreateLinkEnabled ? 'secondary' : 'primary'"
      active-icon="mdi-close"
      :icon="isCreateLinkEnabled ? 'mdi-ray-start-arrow' : 'mdi-plus'"
      :disable="draggingFab"
      data-cy="button-fab-toggle"
    >
      <q-fab-action
        label="Generate Trace Links"
        icon="mdi-link-variant-plus"
        class="bg-background"
        data-cy="button-fab-generate-trace"
        @click="handleGenerateTraceLink"
      />
      <q-fab-action
        v-if="isTreeMode"
        :label="isCreateLinkEnabled ? 'Cancel Trace Link' : 'Draw Trace Link'"
        :icon="isCreateLinkEnabled ? 'mdi-close' : 'mdi-ray-start-arrow'"
        class="bg-background"
        data-cy="button-fab-draw-trace"
        @click="handleDrawTraceLink"
      />
      <q-fab-action
        label="Create Trace Link"
        icon="mdi-ray-start-end"
        class="bg-background"
        data-cy="button-fab-create-trace"
        @click="handleAddTraceLink"
      />

      <q-fab-action
        label="Generate Artifacts"
        icon="mdi-folder-multiple-plus-outline"
        class="bg-background"
        data-cy="button-fab-generate-artifact"
        @click="handleGenerateArtifact"
      />
      <q-fab-action
        label="Create Artifact"
        icon="mdi-folder-plus-outline"
        class="bg-background"
        data-cy="button-fab-create-artifact"
        @click="handleAddArtifact"
      />
    </q-fab>
  </q-page-sticky>
</template>

<script lang="ts">
/**
 * Displays the artifact tree action buttons.
 */
export default {
  name: "ArtifactFab",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { appStore, layoutStore, projectStore, sessionStore } from "@/hooks";
import { disableDrawMode, enableDrawMode } from "@/cytoscape";

const open = ref(false);
const fabPos = ref([18, 18]);
const draggingFab = ref(false);

const isTreeMode = computed(
  () => !appStore.isLoading && layoutStore.isTreeMode
);
const isCreateLinkEnabled = computed(() => appStore.isCreateLinkEnabled);
const isEditor = computed(() => sessionStore.isEditor(projectStore.project));
const doDisplay = computed(
  () => projectStore.isProjectDefined && isEditor.value
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

/**
 * Opens the add artifact modal.
 */
function handleAddArtifact(): void {
  appStore.openArtifactCreatorTo({ isNewArtifact: true });
}

/**
 * Opens the add trace link modal.
 */
function handleAddTraceLink(): void {
  appStore.openDetailsPanel("saveTrace");
}

/**
 * Enables the trace link creator.
 */
function handleDrawTraceLink(): void {
  if (isCreateLinkEnabled.value) {
    disableDrawMode();
  } else {
    enableDrawMode();
  }
}

/**
 * Opens the generate trace link panel.
 */
function handleGenerateTraceLink(): void {
  appStore.openDetailsPanel("generateTrace");
}

/**
 * Opens the generate artifact panel.
 */
function handleGenerateArtifact(): void {
  appStore.openDetailsPanel("generateArtifact");
}
</script>

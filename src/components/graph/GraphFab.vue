<template>
  <q-page-sticky
    v-if="displayActions"
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
      :active-icon="getIcon('cancel')"
      :icon="drawMode ? getIcon('trace') : getIcon('graph-add')"
      :disable="draggingFab"
      data-cy="button-fab-toggle"
    >
      <q-fab-action
        v-if="displayGenerateActions"
        outline
        label="Generate Trace Links"
        :icon="getIcon('generate-traces')"
        class="bg-neutral"
        color="primary"
        data-cy="button-fab-generate-trace"
        @click="appStore.openDetailsPanel('generateTrace')"
      />
      <q-fab-action
        v-if="displayGenerateActions"
        outline
        label="Generate Artifacts"
        :icon="getIcon('generate-artifacts')"
        class="bg-neutral"
        color="primary"
        data-cy="button-fab-generate-artifact"
        @click="appStore.openDetailsPanel('generateArtifact')"
      />
      <q-fab-action
        v-if="displayGenerateActions"
        outline
        label="Summarize Artifacts"
        :icon="getIcon('generate-summaries')"
        class="bg-neutral"
        color="primary"
        data-cy="button-fab-summarize-artifact"
        @click="appStore.openDetailsPanel('summarizeArtifact')"
      />
      <q-fab-action
        outline
        :label="drawMode ? 'Cancel Draw Mode' : 'Draw Links'"
        :icon="drawMode ? getIcon('cancel') : getIcon('trace')"
        class="bg-neutral"
        data-cy="button-fab-draw-trace"
        @click="cyStore.drawMode('toggle')"
      />
      <q-fab-action
        v-if="isTreeMode"
        outline
        label="Create Trace Link"
        :icon="getIcon('create-trace')"
        class="bg-neutral"
        data-cy="button-fab-create-trace"
        @click="appStore.openDetailsPanel('saveTrace')"
      />
      <q-fab-action
        v-if="isTreeMode"
        outline
        label="Create Artifact"
        :icon="getIcon('create-artifact')"
        class="bg-neutral"
        data-cy="button-fab-create-artifact"
        @click="artifactSaveStore.openPanel({ isNewArtifact: true })"
      />
    </q-fab>
    <icon-button
      v-if="drawMode"
      icon="cancel"
      tooltip="Cancel draw mode"
      class="q-ml-sm"
      @click="cyStore.drawMode('disable')"
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
import { getIcon } from "@/util";
import {
  appStore,
  artifactSaveStore,
  cyStore,
  layoutStore,
  permissionStore,
} from "@/hooks";
import { IconButton } from "@/components/common";

const open = ref(false);
const fabPos = ref([18, 18]);
const draggingFab = ref(false);

const isTreeMode = computed(
  () => !appStore.isLoading && layoutStore.isTreeMode
);
const drawMode = computed(() => appStore.popups.drawTrace);

const displayActions = computed(() =>
  permissionStore.isAllowed("project.edit_data")
);
const displayGenerateActions = computed(() =>
  permissionStore.isAllowed("project.edit_data")
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

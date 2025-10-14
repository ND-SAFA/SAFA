<template>
  <q-page-sticky
    v-if="displayActions"
    :offset="fabPos"
    class="artifact-fab"
    position="bottom-left"
  >
    <q-fab
      v-model="open"
      v-touch-pan.prevent.mouse="handleMoveFab"
      :active-icon="getIcon('cancel')"
      :color="drawMode ? 'secondary' : 'gradient'"
      :disable="draggingFab"
      :icon="drawMode ? getIcon('trace') : getIcon('graph-add')"
      class="bg-neutral"
      data-cy="button-fab-toggle"
      direction="up"
      vertical-actions-align="left"
    >
      <q-fab-action
        v-if="displayGenerateActions"
        :icon="getIcon('generate-traces')"
        class="bg-neutral"
        color="gradient"
        data-cy="button-fab-generate-trace"
        label="Generate Trace Links"
        @click="appStore.openDetailsPanel('generateTrace')"
      />
      <q-fab-action
        v-if="displayGenerateActions"
        :icon="getIcon('generate-artifacts')"
        class="bg-neutral"
        color="gradient"
        data-cy="button-fab-generate-artifact"
        label="Generate Artifacts"
        @click="appStore.openDetailsPanel('generateArtifact')"
      />
      <q-fab-action
        v-if="displayGenerateActions && ENABLED_FEATURES.GENERATE_SUMMARIES"
        :icon="getIcon('generate-summaries')"
        class="bg-neutral"
        color="gradient"
        data-cy="button-fab-summarize-artifact"
        label="Summarize Artifacts"
        @click="appStore.openDetailsPanel('summarizeArtifact')"
      />
      <q-fab-action
        v-if="isTreeMode"
        :icon="drawMode ? getIcon('cancel') : getIcon('trace')"
        :label="drawMode ? 'Cancel Draw Mode' : 'Draw Trace Link'"
        class="bg-neutral"
        data-cy="button-fab-draw-trace"
        @click="cyStore.drawMode('toggle')"
      />
      <q-fab-action
        v-if="isTreeMode"
        :icon="getIcon('create-trace')"
        class="bg-neutral"
        data-cy="button-fab-create-trace"
        label="Create Trace Link"
        @click="appStore.openDetailsPanel('saveTrace')"
      />
      <q-fab-action
        v-if="isTreeMode"
        :icon="getIcon('create-artifact')"
        class="bg-neutral"
        data-cy="button-fab-create-artifact"
        label="Create Artifact"
        @click="artifactSaveStore.openPanel({ isNewArtifact: true })"
      />
    </q-fab>
    <icon-button
      v-if="drawMode"
      class="q-ml-sm"
      icon="cancel"
      tooltip="Cancel draw mode"
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

<script lang="ts" setup>
import { computed, ref } from "vue";
import { ENABLED_FEATURES, getIcon } from "@/util";
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
  permissionStore.isAllowed("project.generate")
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

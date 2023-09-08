<template>
  <node-display
    v-if="displayActions"
    variant="menu"
    color="primary"
    @mousedown.stop
    @mouseup.stop
  >
    <flex-box>
      <icon-button
        tooltip="Create artifact"
        icon="create-artifact"
        data-cy="button-add-artifact"
        @click="
          artifactSaveStore.openPanel({ isNewArtifact: true });
          handleCloseMenu();
        "
      />
      <icon-button
        tooltip="Create trace link"
        icon="create-trace"
        data-cy="button-add-trace"
        @click="
          traceSaveStore.openPanel();
          handleCloseMenu();
        "
      />
      <icon-button
        :tooltip="drawMode ? 'Cancel Draw Mode' : 'Draw Trace Link'"
        :icon="drawMode ? 'cancel' : 'trace'"
        @click="
          toggleDrawMode();
          handleCloseMenu();
        "
      />
      <separator vertical class="q-mx-xs" />
      <icon-button
        v-if="displayGenerateActions"
        tooltip="Generate artifacts"
        icon="generate-artifacts"
        color="primary"
        data-cy="button-generate-artifact"
        @click="
          appStore.openDetailsPanel('generateArtifact');
          handleCloseMenu();
        "
      />
      <icon-button
        v-if="displayGenerateActions"
        tooltip="Generate trace links"
        icon="generate-traces"
        color="primary"
        data-cy="button-generate-trace"
        @click="
          appStore.openDetailsPanel('generateTrace');
          handleCloseMenu();
        "
      />
    </flex-box>
  </node-display>
</template>

<script lang="ts">
/**
 * Renders a context menu for the artifact tree.
 */
export default {
  name: "ArtifactMenu",
};
</script>

<script setup lang="ts">
import { computed, inject } from "vue";
import {
  appStore,
  artifactSaveStore,
  permissionStore,
  traceSaveStore,
} from "@/hooks";
import { toggleDrawMode } from "@/cytoscape";
import { FlexBox, IconButton, Separator } from "@/components/common";
import { NodeDisplay } from "../display";

const handleCloseMenu = inject<() => void>("menu-close");

const drawMode = computed(() => appStore.popups.drawTrace);

const displayActions = computed(() =>
  permissionStore.isAllowed("project.edit_data")
);
const displayGenerateActions = computed(() =>
  permissionStore.isAllowed("project.edit_data")
);
</script>

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
        :tooltip="
          drawMode ? 'Cancel draw mode' : 'Draw artifact type direction'
        "
        :icon="drawMode ? 'cancel' : 'trace'"
        @click="
          toggleDrawMode();
          handleCloseMenu();
        "
      />
      <separator v-if="displayGenerateActions" vertical class="q-mx-xs" />
      <icon-button
        v-if="displayGenerateActions"
        tooltip="Generate artifacts"
        icon="generate-artifacts"
        color="primary"
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
 * Renders a context menu for the tim tree.
 */
export default {
  name: "TimMenu",
};
</script>

<script setup lang="ts">
import { computed, inject } from "vue";
import { appStore, permissionStore } from "@/hooks";
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

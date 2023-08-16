<template>
  <node-display
    v-if="display"
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
      <separator vertical class="q-mx-xs" />
      <icon-button
        tooltip="Generate artifacts"
        icon="generate-artifacts"
        color="primary"
        @click="
          appStore.openDetailsPanel('generateArtifact');
          handleCloseMenu();
        "
      />
      <icon-button
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

const display = computed(() => permissionStore.projectAllows("editor"));

const drawMode = computed(() => appStore.isCreateLinkEnabled);
</script>

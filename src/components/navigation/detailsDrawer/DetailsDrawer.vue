<template>
  <v-navigation-drawer
    location="right"
    disable-resize-watcher
    :model-value="drawerOpen"
    height="100%"
    :width="width"
    class="primary-bg"
    :scrim="false"
  >
    <v-container class="full-height">
      <flex-box justify="space-between" align="center">
        <typography color="primary" el="h2" variant="subtitle" :value="title" />
        <icon-button
          icon-id="mdi-close"
          tooltip="Close panel"
          data-cy="button-close-details"
          @click="handleClose"
        />
      </flex-box>
      <v-divider />
      <delta-panel />
      <document-panel />
      <artifact-panel />
      <artifact-body-panel />
      <save-artifact-panel />
      <trace-link-panel />
      <save-trace-link-panel />
      <generate-trace-link-panel />
      <artifact-level-panel />
      <trace-matrix-panel />
    </v-container>
  </v-navigation-drawer>
</template>

<script lang="ts">
/**
 * Renders content in a right side panel.
 */
export default {
  name: "DetailsDrawer",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { appStore, selectionStore } from "@/hooks";
import { IconButton, Typography, FlexBox } from "@/components/common";
import { DeltaPanel } from "@/components/delta";
import { DocumentPanel } from "@/components/document";
import {
  ArtifactPanel,
  ArtifactBodyPanel,
  SaveArtifactPanel,
} from "@/components/artifact/panels";
import {
  TraceLinkPanel,
  SaveTraceLinkPanel,
  GenerateTraceLinkPanel,
} from "@/components/traceLink/panels";
import { ArtifactLevelPanel, TraceMatrixPanel } from "@/components/tim";

const openState = computed(() => appStore.isDetailsPanelOpen);
const drawerOpen = computed(() => typeof openState.value === "string");

const title = computed(() => {
  switch (openState.value) {
    case "delta":
      return "Version Delta";
    case "document":
      return "Save View";
    case "displayArtifact":
      return "Artifact";
    case "displayArtifactBody":
      return "Artifact Body";
    case "saveArtifact":
      return "Save Artifact";
    case "displayTrace":
      return "Trace Link";
    case "saveTrace":
      return "Create Trace Link";
    case "generateTrace":
      return "Generate Trace Links";
    case "displayArtifactLevel":
      return "Artifact Type";
    case "displayTraceMatrix":
      return "Trace Matrix";
    default:
      return "";
  }
});

const width = computed(() => {
  if (
    openState.value === "displayArtifactBody" ||
    openState.value === "displayArtifact" ||
    openState.value === "saveArtifact"
  ) {
    return "600";
  } else if (openState.value === "generateTrace") {
    return "800";
  } else {
    return "400";
  }
});

/**
 * Toggles whether the details panel is open.
 */
function handleClose(): void {
  selectionStore.clearSelections();
}
</script>

<template>
  <q-drawer
    bordered
    side="right"
    :model-value="drawerOpen"
    :breakpoint="0"
    :width="width"
    :class="className"
  >
    <div class="q-pa-sm q-mb-md bg-background">
      <flex-box justify="between" align="center">
        <typography color="primary" variant="subtitle" :value="title" />
        <icon-button
          icon="cancel"
          tooltip="Close panel"
          data-cy="button-close-details"
          @click="handleClose"
        />
      </flex-box>
      <separator />
      <delta-panel />
      <document-panel />
      <artifact-panel />
      <artifact-body-panel />
      <save-artifact-panel />
      <trace-link-panel />
      <save-trace-link-panel />
      <generate-trace-link-panel />
      <artifact-level-panel />
      <save-artifact-level-panel />
      <trace-matrix-panel />
      <artifact-generation-panel />
    </div>
  </q-drawer>
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
import { appStore, selectionStore, useScreen } from "@/hooks";
import {
  IconButton,
  Typography,
  FlexBox,
  Separator,
} from "@/components/common";
import { DeltaPanel } from "@/components/delta";
import { DocumentPanel } from "@/components/document";
import {
  ArtifactPanel,
  ArtifactBodyPanel,
  SaveArtifactPanel,
  ArtifactGenerationPanel,
} from "@/components/artifact/panels";
import {
  TraceLinkPanel,
  SaveTraceLinkPanel,
  GenerateTraceLinkPanel,
} from "@/components/traceLink/panels";
import {
  ArtifactLevelPanel,
  TraceMatrixPanel,
  SaveArtifactLevelPanel,
} from "@/components/tim";

const { smallWindow } = useScreen();

const openState = computed(() => appStore.isDetailsPanelOpen);
const drawerOpen = computed(() => typeof openState.value === "string");

const className = computed(
  () => `bg-background nav-panel nav-panel-${openState.value}`
);

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
    case "generateArtifact":
      return "Generate Artifacts";
    case "displayTrace":
      return "Trace Link";
    case "saveTrace":
      return "Create Trace Link";
    case "generateTrace":
      return "Generate Trace Links";
    case "displayArtifactLevel":
      return "Artifact Type";
    case "saveArtifactLevel":
      return "Save Artifact Type";
    case "displayTraceMatrix":
      return "Trace Matrix";
    default:
      return "";
  }
});

const width = computed(() => {
  if (smallWindow.value) {
    return 500;
  } else if (
    openState.value === "displayArtifactLevel" ||
    openState.value === "displayTraceMatrix" ||
    openState.value === "displayTrace" ||
    openState.value === "displayArtifact" ||
    openState.value === "saveArtifact"
  ) {
    return 600;
  } else if (
    openState.value === "displayArtifactBody" ||
    openState.value === "generateTrace"
  ) {
    return 800;
  } else {
    return 500;
  }
});

/**
 * Toggles whether the details panel is open.
 */
function handleClose(): void {
  selectionStore.clearSelections();
}
</script>

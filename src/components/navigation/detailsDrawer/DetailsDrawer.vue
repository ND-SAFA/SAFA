<template>
  <q-drawer
    bordered
    side="right"
    :model-value="drawerOpen"
    :breakpoint="500"
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
      <project-overview-panel />
      <artifact-panel />
      <artifact-body-panel />
      <save-artifact-panel />
      <trace-link-panel />
      <save-trace-link-panel />
      <edit-trace-link-panel />
      <generate-trace-link-panel />
      <artifact-level-panel />
      <save-artifact-level-panel />
      <trace-matrix-panel />
      <artifact-generation-panel />
      <artifact-summarization-panel />
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
import { DeltaPanel } from "@/components/delta/panel";
import { DocumentPanel } from "@/components/document";
import {
  ArtifactPanel,
  ArtifactBodyPanel,
  SaveArtifactPanel,
  ArtifactGenerationPanel,
  ArtifactSummarizationPanel,
} from "@/components/artifact/panel";
import {
  TraceLinkPanel,
  SaveTraceLinkPanel,
  GenerateTraceLinkPanel,
  EditTraceLinkPanel,
} from "@/components/traceLink/panels";
import {
  ArtifactLevelPanel,
  SaveArtifactLevelPanel,
} from "@/components/artifactType";
import { TraceMatrixPanel } from "@/components/traceMatrix";
import { ProjectOverviewPanel } from "@/components/project/panel";

const { smallWindow } = useScreen();

const openState = computed(() => appStore.popups.detailsPanel);
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
    case "summarizeArtifact":
      return "Summarize Artifacts";
    case "displayTrace":
      return "Trace Link";
    case "saveTrace":
      return "Create Trace Link";
    case "editTrace":
      return "Edit Trace Link";
    case "generateTrace":
      return "Generate Trace Links";
    case "displayArtifactLevel":
      return "Artifact Type";
    case "saveArtifactLevel":
      return "Save Artifact Type";
    case "displayTraceMatrix":
      return "Trace Matrix";
    case "displayProject":
      return "Project Overview";
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
    openState.value === "generateTrace" ||
    openState.value === "displayProject"
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

<template>
  <q-drawer
    :breakpoint="500"
    :class="className"
    :model-value="drawerOpen"
    :width="width"
    bordered
    side="right"
  >
    <div class="q-pa-sm q-mb-md bg-neutral">
      <delta-panel />
      <view-panel />
      <project-overview-panel />
      <artifact-panel />
      <artifact-body-panel />
      <save-artifact-panel />
      <trace-link-panel />
      <save-trace-link-panel />
      <edit-trace-link-panel />
      <artifact-level-panel />
      <save-artifact-level-panel />
      <trace-matrix-panel />
      <generate-trace-link-panel />
      <artifact-generation-panel />
      <health-panel />
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

<script lang="ts" setup>
import { computed } from "vue";
import { appStore, useScreen } from "@/hooks";
import { DeltaPanel } from "@/components/delta/panel";
import { ViewPanel } from "@/components/view";
import {
  ArtifactPanel,
  ArtifactBodyPanel,
  HealthPanel,
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
  () => `bg-neutral nav-panel nav-panel-${openState.value}`
);

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
</script>

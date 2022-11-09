<template>
  <v-navigation-drawer
    app
    right
    clipped
    hide-overlay
    disable-resize-watcher
    :value="drawerOpen"
    height="100%"
    :width="width"
  >
    <v-container>
      <flex-box justify="space-between" align="center">
        <typography color="primary" el="h2" variant="subtitle" :value="title" />
        <generic-icon-button
          icon-id="mdi-close"
          tooltip="Close panel"
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
    </v-container>
  </v-navigation-drawer>
</template>

<script lang="ts">
import Vue from "vue";
import { DetailsOpenState } from "@/types";
import { appStore, selectionStore } from "@/hooks";
import { GenericIconButton, Typography, FlexBox } from "@/components/common";
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
} from "@/components/traceLink/panels";

/**
 * Renders content in a right side panel.
 */
export default Vue.extend({
  name: "DetailsDrawer",
  components: {
    SaveTraceLinkPanel,
    TraceLinkPanel,
    SaveArtifactPanel,
    ArtifactBodyPanel,
    ArtifactPanel,
    DocumentPanel,
    DeltaPanel,
    Typography,
    FlexBox,
    GenericIconButton,
  },
  computed: {
    /**
     * @return The state of the details panel.
     */
    openState(): DetailsOpenState {
      return appStore.isDetailsPanelOpen;
    },
    /**
     * @return Whether the details panel is open.
     */
    drawerOpen(): boolean {
      return typeof this.openState === "string";
    },
    /**
     * @return The title of the panel.
     */
    title(): string {
      switch (appStore.isDetailsPanelOpen) {
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
        default:
          return "";
      }
    },
    /**
     * @return The width of the panel.
     */
    width(): string {
      if (appStore.isDetailsPanelOpen === "displayArtifactBody") {
        return "600";
      } else {
        return "400";
      }
    },
  },
  methods: {
    /**
     * Toggles whether the details panel is open.
     */
    handleClose(): void {
      selectionStore.clearSelections();
    },
  },
});
</script>

<style scoped lang="scss"></style>

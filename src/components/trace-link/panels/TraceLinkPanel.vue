<template>
  <v-container v-if="isOpen" data-cy="panel-trace-display">
    <v-card outlined class="pa-2">
      <generic-artifact-body-display
        :artifact="targetArtifact"
        display-title
        display-divider
      />
    </v-card>
    <flex-box justify="center" y="2">
      <v-icon large style="transform: rotate(270deg)">
        mdi-ray-start-arrow
      </v-icon>
    </flex-box>
    <v-card outlined class="pa-2">
      <generic-artifact-body-display
        :artifact="sourceArtifact"
        display-title
        display-divider
      />
    </v-card>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { ArtifactModel, TraceLinkModel } from "@/types";
import { appStore, artifactStore, selectionStore } from "@/hooks";
import { GenericArtifactBodyDisplay, FlexBox } from "@/components/common";

/**
 * Displays trace link information.
 */
export default Vue.extend({
  name: "TraceLinkPanel",
  components: { FlexBox, GenericArtifactBodyDisplay },
  computed: {
    /**
     * @return Whether this panel is open.
     */
    isOpen(): boolean {
      return appStore.isDetailsPanelOpen === "displayTrace";
    },
    /**
     * @return The selected trace link.
     */
    traceLink(): TraceLinkModel | undefined {
      return selectionStore.selectedTraceLink;
    },
    /**
     * @return The artifact this link comes from.
     */
    sourceArtifact(): ArtifactModel | undefined {
      return artifactStore.getArtifactById(this.traceLink?.sourceId || "");
    },
    /**
     * @return The artifact this link goes towards.
     */
    targetArtifact(): ArtifactModel | undefined {
      return artifactStore.getArtifactById(this.traceLink?.targetId || "");
    },
  },
  methods: {
    /**
     * Closes this panel.
     */
    handleClose(): void {
      appStore.closeSidePanels();
    },
  },
});
</script>

<style scoped lang="scss"></style>

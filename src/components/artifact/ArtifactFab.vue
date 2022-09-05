<template>
  <v-speed-dial
    fixed
    bottom
    right
    v-model="fab"
    transition="scroll-y-transition"
  >
    <template v-slot:activator>
      <v-btn
        v-model="fab"
        :color="isCreateLinkEnabled ? 'secondary darken-1' : 'primary'"
        dark
        fab
        data-cy="button-fab-toggle"
      >
        <v-icon v-if="fab"> mdi-close </v-icon>
        <v-icon
          v-else-if="isCreateLinkEnabled"
          style="transform: rotate(-45deg)"
        >
          mdi-ray-start-arrow
        </v-icon>
        <v-icon v-else>mdi-plus</v-icon>
      </v-btn>
    </template>
    <generic-icon-button
      v-if="isVisible"
      fab
      small
      :icon-style="isCreateLinkEnabled ? '' : 'transform: rotate(-45deg)'"
      :icon-id="isCreateLinkEnabled ? 'mdi-close' : 'mdi-ray-start-arrow'"
      :tooltip="isCreateLinkEnabled ? 'Cancel Trace Link' : 'Draw Trace Link'"
      data-cy="button-fab-draw-trace"
      @click="handleDrawTraceLink"
    />
    <generic-icon-button
      fab
      small
      icon-id="mdi-ray-start-end"
      tooltip="Add Trace Link"
      data-cy="button-fab-create-trace"
      @click="handleAddTraceLink"
    />
    <generic-icon-button
      fab
      small
      icon-id="mdi-folder-plus-outline"
      tooltip="Add Artifact"
      data-cy="button-fab-create-artifact"
      @click="handleAddArtifact"
    />
  </v-speed-dial>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore, documentStore, projectStore } from "@/hooks";
import { disableDrawMode, enableDrawMode } from "@/cytoscape";
import { GenericIconButton } from "@/components";

/**
 * Displays the artifact tree action buttons.
 */
export default Vue.extend({
  name: "ArtifactFab",
  components: {
    GenericIconButton,
  },
  data() {
    return { fab: false };
  },
  computed: {
    /**
     * @return Whether to render the artifact tree.
     */
    isVisible(): boolean {
      return !appStore.isLoading && !documentStore.isTableDocument;
    },
    /**
     * @return Whether trace link draw mode is currently enabled.
     */
    isCreateLinkEnabled(): boolean {
      return appStore.isCreateLinkEnabled;
    },
  },
  methods: {
    /**
     * Opens the add artifact modal.
     */
    handleAddArtifact(): void {
      projectStore.ifProjectDefined(() => {
        appStore.openArtifactCreatorTo({ isNewArtifact: true });
      });
    },
    /**
     * Opens the add trace link modal.
     */
    handleAddTraceLink(): void {
      projectStore.ifProjectDefined(() => {
        appStore.toggleTraceLinkCreator();
      });
    },
    /**
     * Enables the trace link creator.
     */
    handleDrawTraceLink(): void {
      projectStore.ifProjectDefined(() => {
        if (this.isCreateLinkEnabled) {
          disableDrawMode();
        } else {
          enableDrawMode();
        }
      });
    },
  },
});
</script>

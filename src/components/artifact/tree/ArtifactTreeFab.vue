<template>
  <v-speed-dial
    v-if="isVisible"
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
      fab
      small
      :icon-style="isCreateLinkEnabled ? '' : 'transform: rotate(-45deg)'"
      :icon-id="isCreateLinkEnabled ? 'mdi-close' : 'mdi-ray-start-arrow'"
      :tooltip="isCreateLinkEnabled ? 'Cancel Trace Link' : 'Draw Trace Link'"
      @click="handleDrawTraceLink"
    />
    <generic-icon-button
      fab
      small
      icon-id="mdi-ray-start-end"
      tooltip="Add Trace Link"
      @click="handleAddTraceLink"
    />
    <generic-icon-button
      fab
      small
      icon-id="mdi-folder-plus-outline"
      tooltip="Add Artifact"
      @click="handleAddArtifact"
    />
  </v-speed-dial>
</template>

<script lang="ts">
import Vue from "vue";
import { appModule, documentModule, projectModule } from "@/store";
import { GenericIconButton } from "@/components";
import { disableDrawMode, enableDrawMode } from "@/cytoscape";

/**
 * Displays the artifact tree action buttons.
 */
export default Vue.extend({
  name: "ArtifactTreeFab",
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
      return !appModule.getIsLoading && !documentModule.isTableDocument;
    },
    /**
     * @return Whether trace link draw mode is currently enabled.
     */
    isCreateLinkEnabled(): boolean {
      return appModule.getIsCreateLinkEnabled;
    },
  },
  methods: {
    /**
     * Opens the add artifact modal.
     */
    handleAddArtifact(): void {
      projectModule.ifProjectDefined(() => {
        appModule.openArtifactCreatorTo({ isNewArtifact: true });
      });
    },
    /**
     * Opens the add trace link modal.
     */
    handleAddTraceLink(): void {
      projectModule.ifProjectDefined(() => {
        appModule.toggleTraceLinkCreator();
      });
    },
    /**
     * Enables the trace link creator.
     */
    handleDrawTraceLink(): void {
      projectModule.ifProjectDefined(() => {
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

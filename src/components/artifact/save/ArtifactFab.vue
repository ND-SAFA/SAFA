<template>
  <v-speed-dial
    v-if="isEditor"
    v-model="fab"
    fixed
    bottom
    right
    transition="scroll-y-transition"
  >
    <template #activator>
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
    <icon-button
      fab
      small
      icon-id="mdi-link-variant-plus"
      tooltip="Generate Trace Links"
      data-cy="button-fab-generate-trace"
      @click="handleGenerateTraceLink"
    />
    <icon-button
      v-if="isTreeMode"
      fab
      small
      :icon-style="isCreateLinkEnabled ? '' : 'transform: rotate(-45deg)'"
      :icon-id="isCreateLinkEnabled ? 'mdi-close' : 'mdi-ray-start-arrow'"
      :tooltip="isCreateLinkEnabled ? 'Cancel Trace Link' : 'Draw Trace Link'"
      data-cy="button-fab-draw-trace"
      @click="handleDrawTraceLink"
    />
    <icon-button
      fab
      small
      icon-id="mdi-ray-start-end"
      tooltip="Add Trace Link"
      data-cy="button-fab-create-trace"
      @click="handleAddTraceLink"
    />
    <icon-button
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
import { defineComponent } from "vue";
import { appStore, layoutStore, projectStore, sessionStore } from "@/hooks";
import { disableDrawMode, enableDrawMode } from "@/cytoscape";
import { IconButton } from "@/components/common";

/**
 * Displays the artifact tree action buttons.
 */
export default defineComponent({
  name: "ArtifactFab",
  components: {
    IconButton,
  },
  data() {
    return { fab: false };
  },
  computed: {
    /**
     * @return Whether to render the artifact tree.
     */
    isTreeMode(): boolean {
      return !appStore.isLoading && layoutStore.isTreeMode;
    },
    /**
     * @return Whether trace link draw mode is currently enabled.
     */
    isCreateLinkEnabled(): boolean {
      return appStore.isCreateLinkEnabled;
    },
    /**
     * @return Whether the current user is an editor of the current project.
     */
    isEditor(): boolean {
      return sessionStore.isEditor(projectStore.project);
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
        appStore.openDetailsPanel("saveTrace");
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
    /**
     * Opens the generate trace link modal.
     */
    handleGenerateTraceLink(): void {
      projectStore.ifProjectDefined(() => {
        appStore.openDetailsPanel("generateTrace");
      });
    },
  },
});
</script>

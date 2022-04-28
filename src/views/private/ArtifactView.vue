<template>
  <private-page full-window>
    <template v-slot:page>
      <artifact-table />
      <artifact-tree />
      <artifact-creator-modal
        :title="creatorTitle"
        :is-open="isArtifactCreatorOpen"
        :artifact="selectedArtifact"
        @close="closeArtifactCreator"
      />
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
          >
            <v-icon v-if="fab"> mdi-close </v-icon>
            <v-icon v-else-if="isCreateLinkEnabled">
              mdi-ray-start-arrow
            </v-icon>
            <v-icon v-else>mdi-plus</v-icon>
          </v-btn>
        </template>
        <generic-icon-button
          fab
          small
          :icon-id="isCreateLinkEnabled ? 'mdi-close' : 'mdi-ray-start-arrow'"
          :tooltip="
            isCreateLinkEnabled ? 'Cancel Trace Link' : 'Add Trace Link'
          "
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
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import {
  appModule,
  artifactSelectionModule,
  logModule,
  projectModule,
} from "@/store";
import {
  ArtifactTree,
  ArtifactTable,
  PrivatePage,
  ArtifactCreatorModal,
  GenericIconButton,
} from "@/components";
import { disableDrawMode, enableDrawMode } from "@/cytoscape";

/**
 * Displays the artifact tree and table.
 */
export default Vue.extend({
  name: "ArtifactView",
  components: {
    ArtifactTable,
    PrivatePage,
    ArtifactTree,
    ArtifactCreatorModal,
    GenericIconButton,
  },
  data() {
    return { fab: false };
  },
  computed: {
    /**
     * Returns whether the artifact creator is open.
     */
    isArtifactCreatorOpen() {
      return appModule.getIsArtifactCreatorOpen;
    },
    /**
     * @return The selected artifact.
     */
    selectedArtifact() {
      return artifactSelectionModule.getSelectedArtifact;
    },
    /**
     * @return The selected artifact.
     */
    creatorTitle() {
      return artifactSelectionModule.getSelectedArtifact
        ? "Edit Artifact"
        : "Create Artifact";
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
     * Closes the artifact creator.
     */
    closeArtifactCreator(): void {
      appModule.closeCreator();
    },
    /**
     * Opens the add artifact window.
     */
    handleAddArtifact(): void {
      if (projectModule.isProjectDefined) {
        artifactSelectionModule.clearSelections();
        appModule.openArtifactCreatorTo();
      } else {
        logModule.onWarning("Please select a project to create artifacts.");
      }
    },
    /**
     * Enables the trace link creator.
     */
    handleAddTraceLink(): void {
      if (projectModule.isProjectDefined) {
        if (this.isCreateLinkEnabled) {
          disableDrawMode();
        } else {
          enableDrawMode();
        }
      } else {
        logModule.onWarning("Please select a project to create trace links.");
      }
    },
  },
});
</script>

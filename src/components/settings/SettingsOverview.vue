<template>
  <v-container style="max-width: 50em">
    <flex-box justify="space-between">
      <panel-card class="full-width mr-2">
        <typography el="h2" variant="subtitle" value="Project Data" />
        <v-divider class="mb-2" />
        <typography el="p" :value="subtitle" />
        <typography el="h2" variant="subtitle" value="Description" />
        <v-divider class="mb-2" />
        <typography ep="p" :value="description" />
      </panel-card>

      <div>
        <v-card outlined>
          <v-container>
            <v-btn text @click="handleDownload">
              <v-icon class="mr-1">mdi-download</v-icon>
              Download Files
            </v-btn>
            <br />
            <v-btn text @click="handleEdit">
              <v-icon class="mr-1">mdi-pencil</v-icon>
              Edit Project
            </v-btn>
            <v-divider />
            <v-btn text color="error" @click="handleDelete">
              <v-icon class="mr-1">mdi-delete</v-icon>
              Delete Project
            </v-btn>
          </v-container>
        </v-card>
      </div>

      <project-identifier-modal
        :is-open="isEditOpen"
        :is-loading="isLoading"
        @close="isEditOpen = false"
        @save="handleSave"
      />
      <confirm-project-delete
        :is-open="isDeleteOpen"
        @confirm="handleConfirmDeleteProject"
        @cancel="isDeleteOpen = false"
      />
    </flex-box>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { identifierSaveStore, projectStore } from "@/hooks";
import {
  handleSaveProject,
  handleDownloadProjectCSV,
  handleDeleteProject,
} from "@/api";
import { Typography, FlexBox, PanelCard } from "@/components/common";
import {
  ProjectIdentifierModal,
  ConfirmProjectDelete,
} from "@/components/project/base";

/**
 * Represents the section describing the project name and descriptions
 * within the settings.
 */
export default Vue.extend({
  name: "SettingsOverview",
  components: {
    PanelCard,
    FlexBox,
    Typography,
    ProjectIdentifierModal,
    ConfirmProjectDelete,
  },
  data() {
    return {
      isLoading: false,
      isEditOpen: false,
      isDeleteOpen: false,
      projectToEdit: projectStore.project,
    };
  },
  computed: {
    /**
     * @return The current project.
     */
    project() {
      return projectStore.project;
    },
    /**
     * @return The subtitle for this project.
     */
    subtitle(): string {
      const { artifacts, traces } = this.project;
      return `${artifacts.length} Artifacts | ${traces.length} Trace Links`;
    },
    /**
     * @return The description for this project.
     */
    description(): string {
      return this.project.description || "No Description.";
    },
  },
  methods: {
    /**
     * Opens the edit modal.
     */
    handleEdit(): void {
      identifierSaveStore.baseIdentifier = this.project;
      this.isEditOpen = true;
    },
    /**
     * Opens the edit modal.
     */
    handleDelete(): void {
      identifierSaveStore.baseIdentifier = this.project;
      this.isDeleteOpen = true;
    },
    /**
     * Attempts to save the project.
     */
    handleSave(): void {
      this.isLoading = true;

      handleSaveProject({
        onSuccess: (project) => projectStore.updateProject(project),
        onComplete: () => {
          this.isLoading = false;
          this.isEditOpen = false;
        },
      });
    },
    /**
     * Downloads project files
     */
    handleDownload(): void {
      handleDownloadProjectCSV();
    },
    /**
     * Attempts to delete a project, and closes the delete modal.
     */
    handleConfirmDeleteProject() {
      this.isLoading = true;

      handleDeleteProject({
        onSuccess: () => {
          this.isDeleteOpen = false;
          this.$emit("unselected");
        },
        onComplete: () => (this.isLoading = false),
      });
    },
  },
});
</script>

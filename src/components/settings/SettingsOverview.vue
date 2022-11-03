<template>
  <div>
    <flex-box justify="space-between">
      <typography el="h1" variant="title" :value="project.name" />
      <flex-box>
        <v-btn text @click="handleDownload">
          <v-icon class="mr-1">mdi-download</v-icon>
          Download Files
        </v-btn>
        <v-btn text @click="handleEdit">
          <v-icon class="mr-1">mdi-pencil</v-icon>
          Edit Project
        </v-btn>
      </flex-box>
    </flex-box>

    <v-divider class="mb-2" />

    <typography el="p" :value="subtitle" />
    <typography ep="p" :value="project.description" />

    <project-identifier-modal
      :is-open="isEditOpen"
      :is-loading="isEditLoading"
      @close="isEditOpen = false"
      @save="handleSave"
    />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { identifierSaveStore, projectStore } from "@/hooks";
import { handleSaveProject, handleDownloadProjectCSV } from "@/api";
import { Typography, FlexBox } from "@/components/common";
import { ProjectIdentifierModal } from "@/components/project/shared";

/**
 * Represents the section describing the project name and descriptions
 * within the settings.
 */
export default Vue.extend({
  name: "SettingsOverview",
  components: {
    FlexBox,
    Typography,
    ProjectIdentifierModal,
  },
  data() {
    return {
      isEditLoading: false,
      isEditOpen: false,
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
     * Attempts to save the project.
     */
    handleSave(): void {
      this.isEditLoading = true;

      handleSaveProject({
        onSuccess: (project) => projectStore.updateProject(project),
        onComplete: () => {
          this.isEditLoading = false;
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
  },
});
</script>

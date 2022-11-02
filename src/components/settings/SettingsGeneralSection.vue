<template>
  <v-container>
    <flex-box justify="space-between">
      <typography el="h1" variant="title" :value="project.name" />
      <flex-box>
        <generic-icon-button
          tooltip="Download Project Files"
          icon-id="mdi-download"
          @click="handleDownload"
        />
        <generic-icon-button
          tooltip="Edit title"
          icon-id="mdi-pencil"
          @click="handleEdit"
        />
      </flex-box>
    </flex-box>

    <v-divider />

    <typography el="p" :value="subtitle" />
    <typography ep="p" :value="project.description" />

    <project-identifier-modal
      :is-open="isEditOpen"
      :is-loading="isEditLoading"
      @close="isEditOpen = false"
      @save="handleSave"
    />
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ProjectModel } from "@/types";
import { identifierSaveStore, projectStore } from "@/hooks";
import { handleSaveProject, handleDownloadProjectCSV } from "@/api";
import { GenericIconButton, Typography, FlexBox } from "@/components/common";
import { ProjectIdentifierModal } from "@/components/project/shared";

/**
 * Represents the section describing the project name and descriptions
 * within the settings.
 */
export default Vue.extend({
  name: "SettingsGeneralSection",
  components: {
    FlexBox,
    Typography,
    GenericIconButton,
    ProjectIdentifierModal,
  },
  props: {
    project: {
      type: Object as PropType<ProjectModel>,
      required: true,
    },
  },
  data() {
    return {
      isEditLoading: false,
      isEditOpen: false,
      projectToEdit: this.project,
    };
  },
  computed: {
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

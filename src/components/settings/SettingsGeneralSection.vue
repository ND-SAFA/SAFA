<template>
  <v-container>
    <flex-box justify="space-between">
      <typography el="h1" variant="title" :value="project.name" />
      <generic-icon-button
        tooltip="Edit title"
        icon-id="mdi-pencil"
        @click="handleEdit"
      />
    </flex-box>
    <v-divider />
    <typography :value="project.description" />

    <project-identifier-modal
      title="Edit Project"
      :is-open="isEditOpen"
      v-bind:project.sync="projectToEdit"
      :is-loading="isEditLoading"
      @close="isEditOpen = false"
      @save="handleSave"
    />
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ProjectModel, IdentifierModel } from "@/types";
import { handleSaveProject } from "@/api";
import { projectStore } from "@/hooks";
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
  methods: {
    /**
     * Opens the edit modal.
     */
    handleEdit(): void {
      this.projectToEdit = this.project;
      this.isEditOpen = true;
    },
    /**
     * Attempts to save the project.
     */
    handleSave(project: IdentifierModel): void {
      this.isEditLoading = true;

      handleSaveProject(
        {
          projectId: this.project.projectId,
          name: project.name,
          description: project.description,
        },
        {
          onSuccess: () => {
            projectStore.updateProject(project);
            this.isEditLoading = false;
            this.isEditOpen = false;
          },
          onError: () => {
            this.isEditLoading = false;
            this.isEditOpen = false;
          },
        }
      );
    },
  },
});
</script>

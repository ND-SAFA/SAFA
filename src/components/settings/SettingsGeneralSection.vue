<template>
  <v-container>
    <div class="d-flex justify-space-between">
      <typography el="h1" variant="title" :value="project.name" />
      <generic-icon-button
        tooltip="Edit title"
        icon-id="mdi-pencil"
        @click="handleEdit"
      />
    </div>
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
import { Project, ProjectIdentifier } from "@/types";
import { handleSaveProject } from "@/api";
import { projectModule } from "@/store";
import { GenericIconButton, Typography } from "@/components/common";
import { ProjectIdentifierModal } from "@/components/project/shared";

/**
 * Represents the section describing the project name and descriptions
 * within the settings.
 */
export default Vue.extend({
  name: "SettingsGeneralSection",
  components: { Typography, GenericIconButton, ProjectIdentifierModal },
  props: {
    project: {
      type: Object as PropType<Project>,
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
    handleSave(project: ProjectIdentifier): void {
      this.isEditLoading = true;

      handleSaveProject(
        {
          projectId: this.project.projectId,
          name: project.name,
          description: project.description,
        },
        {
          onSuccess: () => {
            projectModule.SET_PROJECT_IDENTIFIER(project);
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

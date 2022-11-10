<template>
  <flex-box b="2">
    <v-btn text @click="handleDownload">
      <v-icon class="mr-1">mdi-download</v-icon>
      Download
    </v-btn>
    <br />
    <v-btn text @click="handleEdit">
      <v-icon class="mr-1">mdi-pencil</v-icon>
      Edit
    </v-btn>
    <v-divider vertical />
    <v-btn text color="error" @click="handleDelete">
      <v-icon class="mr-1">mdi-delete</v-icon>
      Delete
    </v-btn>
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
</template>

<script lang="ts">
import Vue from "vue";
import { identifierSaveStore, projectStore } from "@/hooks";
import {
  handleSaveProject,
  handleDownloadProjectCSV,
  handleDeleteProject,
} from "@/api";
import { FlexBox } from "@/components/common";
import ProjectIdentifierModal from "./ProjectIdentifierModal.vue";
import ConfirmProjectDelete from "./ConfirmProjectDelete.vue";

/**
 * Displays buttons for interacting with projects.
 */
export default Vue.extend({
  name: "ProjectButtons",
  components: {
    FlexBox,
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

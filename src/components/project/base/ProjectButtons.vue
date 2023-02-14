<template>
  <flex-box v-if="doDisplay" wrap b="2">
    <text-button
      text
      icon-id="mdi-download"
      data-cy="button-settings-download"
      @click="handleDownload"
    >
      Download
    </text-button>
    <text-button
      text
      variant="edit"
      data-cy="button-settings-edit"
      @click="handleEdit"
    >
      Edit
    </text-button>
    <v-divider vertical />
    <text-button
      text
      variant="delete"
      data-cy="button-settings-delete"
      @click="handleDelete"
    >
      Delete
    </text-button>
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
import { defineComponent } from "vue";
import { identifierSaveStore, projectStore, sessionStore } from "@/hooks";
import {
  handleSaveProject,
  handleDownloadProjectCSV,
  handleDeleteProject,
} from "@/api";
import { FlexBox, TextButton } from "@/components/common";
import ProjectIdentifierModal from "./ProjectIdentifierModal.vue";
import ConfirmProjectDelete from "./ConfirmProjectDelete.vue";

/**
 * Displays buttons for interacting with projects.
 */
export default defineComponent({
  name: "ProjectButtons",
  components: {
    TextButton,
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
     * @return Whether to display these buttons.
     */
    doDisplay(): boolean {
      return sessionStore.isEditor(projectStore.project);
    },
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

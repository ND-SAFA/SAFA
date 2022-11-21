<template>
  <generic-selector
    :headers="headers"
    :items="projects"
    :is-open="isOpen"
    :minimal="minimal"
    item-key="projectId"
    no-data-text="No projects created."
    :is-loading="isLoading"
    :has-delete-for-indexes="deletableProjects"
    :has-delete="false"
    data-cy="table-project"
    @item:edit="handleEditProject"
    @item:select="handleSelectProject"
    @item:delete="handleDeleteProject"
    @item:add="handleAddItem"
    @refresh="fetchProjects"
  >
    <template v-slot:editItemDialogue>
      <project-identifier-modal
        :is-open="isSaveOpen"
        @save="handleConfirmSaveProject"
        @close="handleCloseSaveProject"
      />
    </template>
    <template v-slot:deleteItemDialogue>
      <confirm-project-delete
        :is-open="isDeleteOpen"
        @confirm="handleConfirmDeleteProject"
        @cancel="handleCancelDeleteProject"
      />
    </template>
  </generic-selector>
</template>

<script lang="ts">
import Vue from "vue";
import { DataItem, IdentifierModel } from "@/types";
import { identifierSaveStore, projectStore, sessionStore } from "@/hooks";
import {
  handleDeleteProject,
  handleGetProjects,
  handleSaveProject,
} from "@/api";
import { GenericSelector } from "@/components/common";
import { ConfirmProjectDelete, ProjectIdentifierModal } from "../base";

/**
 * Displays list of project available to current user and allows them to
 * select, edit, delete, or create projects. Project list is refreshed whenever
 * mounted or isOpen is changed to true.
 *
 * @emits-1 `selected` (IdentifierModal) - On project selected.
 * @emits-1 `unselected` - On project unselected.
 */
export default Vue.extend({
  name: "ProjectSelector",
  components: {
    GenericSelector,
    ProjectIdentifierModal,
    ConfirmProjectDelete,
  },
  props: {
    /**
     * Whether this component is currently in view. If within
     * a stepper then this is true when this component is on the current step.
     */
    isOpen: {
      type: Boolean,
      required: true,
    },
    minimal: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      selected: undefined as IdentifierModel | undefined,
      headers: this.minimal
        ? [{ text: "Name", value: "name", sortable: true, isSelectable: true }]
        : [
            { text: "Name", value: "name", sortable: true, isSelectable: true },
            {
              text: "Description",
              sortable: false,
              value: "description",
            },
            {
              text: "Owner",
              sortable: false,
              value: "owner",
            },
            { text: "Actions", value: "actions", sortable: false },
          ],
      isSaveOpen: false,
      isDeleteOpen: false,
      isLoading: false,
    };
  },
  computed: {
    /**
     * @return All projects for the current user.
     */
    projects(): IdentifierModel[] {
      return projectStore.allProjects;
    },
    /**
     * @return All deletable project indexes for the current user.
     */
    deletableProjects(): number[] {
      return projectStore.deletableProjects;
    },
  },
  watch: {
    /**
     * When opened, fetches projects and selects the first if there is only one.
     */
    isOpen(open: boolean): void {
      if (!open) return;

      this.fetchProjects();

      if (this.projects.length !== 1) return;

      this.$emit("selected", this.projects[0], false);
    },
    $route(): void {
      this.fetchProjects();
    },
  },
  methods: {
    /**
     * Emits changes to the selected item.
     * @param item - The selected project.
     * @param goToNextStep - If true with a valid project, the next step will be navigated to.
     */
    handleSelectProject(item: DataItem<IdentifierModel>, goToNextStep = false) {
      if (item.value) {
        this.$emit("selected", item.item, goToNextStep);
      } else {
        this.$emit("unselected");
      }
    },
    /**
     * Opens the add project modal.
     */
    handleAddItem() {
      identifierSaveStore.baseIdentifier = undefined;
      this.isSaveOpen = true;
    },
    /**
     * Closes the add project modal.
     */
    handleCloseSaveProject() {
      this.isSaveOpen = false;
    },
    /**
     * Opens the edit project modal.
     * @param item - The project to edit.
     */
    handleEditProject(item: IdentifierModel) {
      identifierSaveStore.baseIdentifier = item;
      this.isSaveOpen = true;
    },
    /**
     * Opens the delete project modal.
     * @param item - The project to delete.
     */
    handleDeleteProject(item: IdentifierModel) {
      identifierSaveStore.baseIdentifier = item;
      this.isDeleteOpen = true;
    },
    /**
     * Closes the delete project modal.
     */
    handleCancelDeleteProject() {
      this.isDeleteOpen = false;
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
    /**
     * Attempts to save a project.
     */
    handleConfirmSaveProject() {
      this.isLoading = true;

      handleSaveProject({
        onSuccess: (project) => {
          this.selected = project;
          this.isSaveOpen = false;
          this.$emit("selected", project, true);
        },
        onComplete: () => (this.isLoading = false),
      });
    },
    /**
     * Fetches all projects.
     */
    fetchProjects(): void {
      if (!sessionStore.doesSessionExist) return;

      this.isLoading = true;

      handleGetProjects({
        onComplete: () => (this.isLoading = false),
      });
    },
  },
});
</script>

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
    @item:edit="handleEditProject"
    @item:select="handleSelectProject"
    @item:delete="handleDeleteProject"
    @item:add="handleAddItem"
    @refresh="fetchProjects"
  >
    <template v-slot:editItemDialogue>
      <project-identifier-modal
        title="Edit Project"
        :is-open="editProjectDialogue"
        :project="projectToEdit"
        @save="handleConfirmEditProject"
        @close="handleCloseProjectEdit"
      />
    </template>
    <template v-slot:addItemDialogue>
      <project-identifier-modal
        do-show-upload
        title="Create New Project"
        :is-open="addProjectDialogue"
        @save="handleConfirmAddProject"
        @close="handleCloseAddProject"
      />
    </template>
    <template v-slot:deleteItemDialogue>
      <confirm-project-delete
        :is-open="deleteProjectDialogue"
        :project="projectToDelete"
        @confirm="handleConfirmDeleteProject"
        @cancel="handleCancelDeleteProject"
      />
    </template>
  </generic-selector>
</template>

<script lang="ts">
import Vue from "vue";
import { DataItem, IdentifierModel, ProjectRole } from "@/types";
import { logModule, sessionModule } from "@/store";
import { getProjects, handleDeleteProject, handleSaveProject } from "@/api";
import { GenericSelector } from "@/components/common";
import { ProjectIdentifierModal } from "@/components/project/shared";
import ConfirmProjectDelete from "./ConfirmProjectDelete.vue";

/**
 * Displays list of project available to current user and allows them to
 * select, edit, delete, or create projects. Project list is refreshed whenever
 * mounted or isOpen is changed to true.
 *
 * @emits-1 `selected` (ProjectIdentifier) - On project selected.
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
     * a stepper then this is true when the this component is within the current step.
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
      projects: [] as IdentifierModel[],
      deletableProjects: [] as number[],
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
      editProjectDialogue: false,
      deleteProjectDialogue: false,
      addProjectDialogue: false,
      isLoading: false,
      projectToEdit: { name: "", description: "" } as IdentifierModel,
      projectToDelete: undefined as IdentifierModel | undefined,
    };
  },
  /**
   * When mounted, load all projects.
   */
  mounted() {
    this.fetchProjects();
  },
  watch: {
    $route() {
      this.fetchProjects();
    },
    /**
     * When opened, fetches projects and selects the first if there is only one.
     */
    isOpen(open: boolean): void {
      if (!open) return;

      this.fetchProjects();

      if (this.projects.length !== 1) return;

      this.$emit("selected", this.projects[0], false);
    },
  },
  methods: {
    /**
     * @returns The indexes that the current user has delete permissions for.
     */
    getDeletableProjects(): number[] {
      const userEmail = sessionModule.userEmail;

      return this.projects
        .map((project, projectIndex) => {
          const adminMember = project.members.find(
            (m) => m.email === userEmail && m.role === ProjectRole.OWNER
          );
          return adminMember ? projectIndex : -1;
        })
        .filter((idx) => idx !== -1);
    },
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
      this.addProjectDialogue = true;
    },
    /**
     * Closes the add project modal.
     */
    handleCloseAddProject() {
      this.addProjectDialogue = false;
    },
    /**
     * Attempts to create a project, and closes the add modal.
     * @param project - The project to create.
     */
    handleConfirmAddProject(project: IdentifierModel) {
      this.saveOrUpdateProjectHandler(project);
      this.addProjectDialogue = false;
    },
    /**
     * Opens the edit project modal.
     * @param item - The project to edit.
     */
    handleEditProject(item: IdentifierModel) {
      this.projectToEdit = item;
      this.editProjectDialogue = true;
    },
    /**
     * Closes the edit project modal.
     */
    handleCloseProjectEdit() {
      this.editProjectDialogue = false;
    },
    /**
     * Attempts to update a project, and closes the edit modal.
     * @param project - The project to update.
     */
    handleConfirmEditProject(project: IdentifierModel) {
      this.saveOrUpdateProjectHandler(project);
      this.editProjectDialogue = false;
    },
    /**
     * Opens the delete project modal.
     * @param item - The project to delete.
     */
    handleDeleteProject(item: IdentifierModel) {
      this.deleteProjectDialogue = true;
      this.projectToDelete = item;
    },
    /**
     * Closes the delete project modal.
     */
    handleCancelDeleteProject() {
      this.deleteProjectDialogue = false;
    },
    /**
     * Attempts to delete a project, and closes the delete modal.
     * @param project - The project to delete.
     */
    handleConfirmDeleteProject(project: IdentifierModel) {
      this.deleteProjectHandler(project);
      this.deleteProjectDialogue = false;
    },
    /**
     * Fetches all projects.
     */
    fetchProjects(): void {
      this.isLoading = true;
      getProjects()
        .then((projects) => {
          this.projects = projects;
          this.deletableProjects = this.getDeletableProjects();
        })
        .catch((e) => {
          logModule.onDevError(e);
        })
        .finally(() => (this.isLoading = false));
    },
    /**
     * Attempts to delete a project.
     * @param project - The project to delete.
     */
    deleteProjectHandler(project: IdentifierModel) {
      this.isLoading = true;

      handleDeleteProject(project, {
        onSuccess: () => {
          this.isLoading = false;
          this.projects = this.projects.filter(
            (p) => p.projectId !== project.projectId
          );
          this.$emit("unselected");
        },
        onError: () => (this.isLoading = false),
      });
    },
    /**
     * Attempts to save a project.
     * @param project - The project to save.
     */
    saveOrUpdateProjectHandler(project: IdentifierModel) {
      this.isLoading = true;

      handleSaveProject(project, {
        onSuccess: (project) => {
          const projectRemoved = this.projects.filter(
            (p) => project.projectId !== p.projectId
          );

          this.isLoading = false;
          this.projects = [project, ...projectRemoved];
          this.selected = project;
          this.$emit("selected", project, true);
        },
        onError: () => (this.isLoading = false),
      });
    },
  },
});
</script>

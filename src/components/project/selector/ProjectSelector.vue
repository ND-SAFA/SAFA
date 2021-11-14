<template>
  <generic-selector
    :headers="headers"
    :items="projects"
    :is-open="isOpen"
    item-key="projectId"
    no-data-text="No projects created."
    :is-loading="isLoading"
    @edit-item="onEditProject"
    @select-item="onSelectProject"
    @delete-item="onDeleteProject"
    @add-item="onAddItem"
    @refresh="fetchProjects"
  >
    <template v-slot:editItemDialogue>
      <project-identifier-modal
        title="Edit Project"
        :is-open="editProjectDialogue"
        :project="projectToEdit"
        @onSave="onUpdateProject"
        @onClose="onCloseProjectEdit"
      />
    </template>
    <template v-slot:addItemDialogue>
      <project-identifier-modal
        title="Create New Project"
        :is-open="addProjectDialogue"
        @onSave="onSaveNewProject"
        @onClose="onCloseAddProject"
      />
    </template>
    <template v-slot:deleteItemDialogue>
      <confirm-project-delete
        :is-open="deleteProjectDialogue"
        :project="projectToDelete"
        @onConfirmDelete="onConfirmDeleteProject"
        @onCancelDelete="onCancelDeleteProject"
      />
    </template>
  </generic-selector>
</template>

<script lang="ts">
import Vue from "vue";
import { DataItem, ProjectCreationResponse, ProjectIdentifier } from "@/types";
import { deleteProject, getProjects, saveOrUpdateProject } from "@/api";
import { appModule } from "@/store";
import { GenericSelector } from "@/components/common";
import ProjectIdentifierModal from "./ProjectIdentifierModal.vue";
import ConfirmProjectDelete from "./ConfirmProjectDelete.vue";
import { projectSelectorHeaders } from "./headers";

/**
 * Displays list of project available to current user and allows them to
 * select, edit, delete, or create projects. Project list is refreshed whenever
 * mounted or isOpen is changed to true.
 *
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
  },
  data() {
    return {
      selected: undefined as ProjectIdentifier | undefined,
      projects: [] as ProjectIdentifier[],
      headers: projectSelectorHeaders,
      editProjectDialogue: false,
      deleteProjectDialogue: false,
      addProjectDialogue: false,
      isLoading: false,
      projectToEdit: undefined as ProjectIdentifier | undefined,
      projectToDelete: undefined as ProjectIdentifier | undefined,
    };
  },
  mounted() {
    this.fetchProjects();
  },
  watch: {
    isOpen(isOpen: boolean): void {
      if (isOpen) {
        this.fetchProjects();
      }
    },
  },
  methods: {
    onUpdateProject(project: ProjectIdentifier) {
      this.isLoading = true;
      this.saveOrUpdateProjectHandler(project, "updated");
      this.editProjectDialogue = false;
      this.selected = project;
    },
    onSaveNewProject(newProject: ProjectIdentifier) {
      this.isLoading = true;
      this.saveOrUpdateProjectHandler(newProject, "created").then(
        (projectCreated: ProjectCreationResponse) => {
          this.$emit("onProjectSelected", projectCreated.project);
        }
      );
      this.addProjectDialogue = false;
      this.selected = newProject;
    },
    onCloseProjectEdit() {
      this.editProjectDialogue = false;
    },
    onSelectProject(item: DataItem<ProjectIdentifier>) {
      if (item.value) {
        this.$emit("onProjectSelected", item.item);
      } else {
        this.$emit("onProjectUnselected");
      }
    },
    onAddItem() {
      this.addProjectDialogue = true;
    },
    onCloseAddProject() {
      this.addProjectDialogue = false;
    },
    onEditProject(item: ProjectIdentifier) {
      this.projectToEdit = item;
      this.editProjectDialogue = true;
    },
    onDeleteProject(item: ProjectIdentifier) {
      this.deleteProjectDialogue = true;
      this.projectToDelete = item;
    },
    onCancelDeleteProject() {
      this.deleteProjectDialogue = false;
    },
    onConfirmDeleteProject(project: ProjectIdentifier) {
      this.isLoading = true;
      this.deleteProjectHandler(project);
      this.deleteProjectDialogue = false;
    },
    fetchProjects(): void {
      this.isLoading = true;
      getProjects()
        .then((projects) => {
          this.projects = projects;
        })
        .finally(() => (this.isLoading = false));
    },
    deleteProjectHandler(project: ProjectIdentifier) {
      deleteProject(project.projectId)
        .then(() => {
          appModule.onSuccess(`${project.name} successfully deleted.`);
          this.projects = this.projects.filter(
            (p) => p.projectId !== project.projectId
          );
        })
        .finally(() => (this.isLoading = false));
    },
    saveOrUpdateProjectHandler(
      project: ProjectIdentifier,
      operation: "updated" | "created"
    ): Promise<ProjectCreationResponse> {
      return new Promise<ProjectCreationResponse>((resolve, reject) => {
        saveOrUpdateProject({
          projectId: project.projectId,
          description: project.description,
          name: project.name,
          artifacts: [],
          traces: [],
        })
          .then((res: ProjectCreationResponse) => {
            appModule.onSuccess(
              `${res.project.name} was successfully ${operation}.`
            );
            this.isLoading = false;
            const projectRemoved = this.projects.filter(
              (p) => res.project.projectId !== p.projectId
            );

            this.projects = [res.project as ProjectIdentifier].concat(
              projectRemoved
            );
            resolve(res);
          })
          .catch(reject)
          .finally(() => {
            this.isLoading = false;
          });
      });
    },
  },
});
</script>

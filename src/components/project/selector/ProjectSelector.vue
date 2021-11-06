<template>
  <GenericSelector
    :headers="headers"
    :items="projects"
    :isOpen="isOpen"
    itemKey="projectId"
    noDataText="No projects created."
    :isLoading="isLoading"
    @onEditItem="editItem"
    @onSelectItem="selectItem"
    @onDeleteItem="deleteItem"
    @onAddItem="addItem"
    @onRefresh="refresh"
  >
    <template v-slot:editItemDialogue>
      <ProjectCreatorModal
        title="Edit Project"
        :isOpen="editProjectDialogue"
        :project="projectToEdit"
        @onSave="onUpdateProject"
        @onClose="onCloseProject"
      />
    </template>
    <template v-slot:addItemDialogue>
      <ProjectCreatorModal
        title="Create New Project"
        :isOpen="addProjectDialogue"
        @onSave="onSaveAddProject"
        @onClose="onCloseAddProject"
      />
    </template>
    <template v-slot:deleteItemDialogue>
      <ConfirmProjectDelete
        :isOpen="deleteProjectDialogue"
        :project="projectToDelete"
        @onConfirmDelete="onConfirmProjectDelete"
        @onCancelDelete="onCancelDelete"
      />
    </template>
  </GenericSelector>
</template>

<script lang="ts">
import Vue from "vue";
import { deleteProject, getProjects, saveOrUpdateProject } from "@/api";
import { DataItem, ProjectCreationResponse } from "@/types";
import { ProjectIdentifier } from "@/types";
import GenericSelector from "@/components/common/generic/GenericSelector.vue";
import ProjectCreatorModal from "@/components/project/selector/ProjectIdentifierModal.vue";
import ConfirmProjectDelete from "@/components/project/selector/ConfirmProjectDelete.vue";
import { projectSelectorHeaders } from "@/components/project/selector/headers";
import { appModule } from "@/store";

export default Vue.extend({
  components: {
    GenericSelector,
    ProjectCreatorModal,
    ConfirmProjectDelete,
  },
  props: {
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
    this.refresh();
  },
  watch: {
    isOpen(isOpen: boolean): void {
      if (isOpen) {
        this.refresh();
      }
    },
  },
  methods: {
    refresh() {
      this.isLoading = true;
      this.handleGetProjects();
    },
    onUpdateProject(project: ProjectIdentifier) {
      this.isLoading = true;
      this.saveOrUpdateProjectHandler(project, "updated");
      this.editProjectDialogue = false;
      this.selected = project;
    },
    onSaveAddProject(newProject: ProjectIdentifier) {
      this.isLoading = true;
      this.saveOrUpdateProjectHandler(newProject, "created").then(
        (projectCreated: ProjectCreationResponse) => {
          this.$emit("onProjectSelected", projectCreated.project);
        }
      );
      this.addProjectDialogue = false;
      this.selected = newProject;
    },
    onCloseProject() {
      this.editProjectDialogue = false;
    },
    selectItem(item: DataItem<ProjectIdentifier>) {
      if (item.value) {
        this.$emit("onProjectSelected", item.item);
      } else {
        this.$emit("onProjectUnselected");
      }
    },
    addItem() {
      this.addProjectDialogue = true;
    },

    onCloseAddProject() {
      this.addProjectDialogue = false;
    },
    editItem(item: ProjectIdentifier) {
      this.projectToEdit = item;
      this.editProjectDialogue = true;
    },
    deleteItem(item: ProjectIdentifier) {
      this.deleteProjectDialogue = true;
      this.projectToDelete = item;
    },
    onCancelDelete() {
      this.deleteProjectDialogue = false;
    },

    onConfirmProjectDelete(project: ProjectIdentifier) {
      this.isLoading = true;
      this.deleteProjectHandler(project);
      this.deleteProjectDialogue = false;
    },
    handleGetProjects() {
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

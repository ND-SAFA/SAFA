<template>
  <generic-selector
    :headers="headers"
    :items="projects"
    :is-open="isOpen"
    item-key="projectId"
    no-data-text="No projects created."
    :is-loading="isLoading"
    :has-delete-for-indexes="hasDeleteForIndexes"
    @item:edit="onEditProject"
    @item:select="onSelectProject"
    @item:delete="onDeleteProject"
    @item:add="onAddItem"
    @refresh="fetchProjects"
  >
    <template v-slot:editItemDialogue>
      <project-identifier-modal
        title="Edit Project"
        :is-open="editProjectDialogue"
        :project="projectToEdit"
        @save="onUpdateProject"
        @close="onCloseProjectEdit"
      />
    </template>
    <template v-slot:addItemDialogue>
      <project-identifier-modal
        title="Create New Project"
        :is-open="addProjectDialogue"
        @save="onSaveNewProject"
        @close="onCloseAddProject"
      />
    </template>
    <template v-slot:deleteItemDialogue>
      <confirm-project-delete
        :is-open="deleteProjectDialogue"
        :project="projectToDelete"
        @confirm="onConfirmDeleteProject"
        @cancel="onCancelDeleteProject"
      />
    </template>
  </generic-selector>
</template>

<script lang="ts">
import Vue from "vue";
import {
  DataItem,
  Project,
  ProjectCreationResponse,
  ProjectIdentifier,
  ProjectRole,
} from "@/types";
import {
  clearProject,
  deleteProject,
  getProjects,
  saveOrUpdateProject,
} from "@/api";
import { logModule, projectModule, sessionModule } from "@/store";
import { GenericSelector } from "@/components/common";
import { ProjectIdentifierModal } from "@/components/project/shared";
import ConfirmProjectDelete from "./ConfirmProjectDelete.vue";
import { projectSelectorHeaders } from "./headers";

/**
 * Displays list of project available to current user and allows them to
 * select, edit, delete, or create projects. Project list is refreshed whenever
 * mounted or isOpen is changed to true.
 *
 * @emits-1 `selected` (ProjectIdentifier) - On project selected.
 * @emits-1 `unselected` - On project unselected.
 */
export default Vue.extend({
  name: "project-selector",
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
      projectToEdit: { name: "", description: "" } as ProjectIdentifier,
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
        if (this.projects.length === 1) {
          this.$emit("selected", this.projects[0], true);
        }
      }
    },
  },
  computed: {
    hasDeleteForIndexes(): number[] {
      const userEmail = sessionModule.authenticationToken?.sub || "";

      return this.projects
        .map((project, projectIndex) => {
          const projectMembershipQuery = project.members.filter(
            (m) => m.email === userEmail
          );
          if (
            projectMembershipQuery.length === 1 &&
            projectMembershipQuery[0].role === ProjectRole.OWNER
          ) {
            return projectIndex;
          }

          return -1;
        })
        .filter((idx) => idx !== -1);
    },
  },
  methods: {
    onUpdateProject(project: ProjectIdentifier) {
      this.isLoading = true;
      this.saveOrUpdateProjectHandler(project);
      this.editProjectDialogue = false;
      this.selected = project;
    },
    onSaveNewProject(newProject: ProjectIdentifier) {
      this.isLoading = true;
      this.saveOrUpdateProjectHandler(newProject).then((project: Project) => {
        this.$emit("selected", project);
      });
      this.addProjectDialogue = false;
      this.selected = newProject;
    },
    onCloseProjectEdit() {
      this.editProjectDialogue = false;
    },
    onSelectProject(item: DataItem<ProjectIdentifier>, goToNextStep = false) {
      if (item.value) {
        this.$emit("selected", item.item, goToNextStep);
      } else {
        this.$emit("unselected");
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
        .then(async () => {
          logModule.onSuccess(`${project.name} successfully deleted.`);

          this.projects = this.projects.filter(
            (p) => p.projectId !== project.projectId
          );

          if (project.name === projectModule.getProject.name) {
            // Clear the current project if it has been deleted.
            await clearProject();
          }
        })
        .finally(() => (this.isLoading = false));
    },
    saveOrUpdateProjectHandler(project: ProjectIdentifier): Promise<Project> {
      return saveOrUpdateProject({
        projectId: project.projectId,
        description: project.description,
        name: project.name,
        members: [],
        artifacts: [],
        traces: [],
      })
        .then((res: ProjectCreationResponse) => {
          const project = res.project;
          projectModule.SET_PROJECT_IDENTIFIER(project);
          const projectRemoved = this.projects.filter(
            (p) => project.projectId !== p.projectId
          );

          this.projects = [project as ProjectIdentifier].concat(projectRemoved);
          this.$emit("selected", project, true);
          return project;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
  },
});
</script>

import { defineStore } from "pinia";
import {
  IdentifierSchema,
  ProjectSchema,
  GenerationModelSchema,
  VersionSchema,
  TimStructure,
} from "@/types";
import { createProject, createTIM } from "@/util";
import { pinia } from "@/plugins";
import sessionStore from "../core/useSession";
import selectionStore from "../graph/useSelection";
import logStore from "../core/useLog";
import membersStore from "./useMembers";
import warningStore from "./useWarnings";
import documentStore from "./useDocuments";
import subtreeStore from "./useSubtree";
import typeOptionsStore from "./useTypeOptions";
import attributesStore from "./useAttributes";

/**
 * Manages the selected project.
 */
export const useProject = defineStore("project", {
  state: () => ({
    /**
     * All projects available to the current user.
     */
    allProjects: [] as IdentifierSchema[],
    /**
     * The currently loaded project.
     */
    project: createProject(),
    /**
     * The TIM structure for the current project.
     */
    tim: { artifacts: [], traces: [] } as TimStructure,
  }),
  getters: {
    /**
     * @return The current project id.
     */
    projectId(): string {
      return this.project.projectId;
    },
    /**
     * @return The current version.
     */
    version(): VersionSchema | undefined {
      return this.project.projectVersion;
    },
    /**
     * @return The current version id.
     */
    versionId(): string {
      return this.version?.versionId || "";
    },
    /**
     * @returns Whether the project is defined.
     */
    isProjectDefined(): boolean {
      return this.projectId !== "";
    },
    /**
     * @returns Whether the version is defined.
     */
    isVersionDefined(): boolean {
      return this.versionId !== "";
    },
    /**
     * @return Returns the version ID, and logs an error if there isn't one.
     */
    versionIdWithLog(): string {
      if (!this.versionId) {
        logStore.onWarning("Please select a project version.");
      }

      return this.versionId;
    },
    /**
     * @return The current project's models.
     */
    models(): GenerationModelSchema[] {
      return this.project.models;
    },
    /**
     * @return A list of indexes for deletable projects.
     */
    deletableProjects(): number[] {
      return this.allProjects
        .map((project, projectIndex) =>
          sessionStore.isAdmin(project) ? projectIndex : -1
        )
        .filter((idx) => idx !== -1);
    },
    /**
     * @return All projects that arent currently loaded.
     */
    unloadedProjects(): IdentifierSchema[] {
      return this.allProjects.filter(
        ({ projectId }) => projectId !== this.projectId
      );
    },
  },
  actions: {
    /**
     * Updates the current project.
     *
     * @param project - The new project fields.
     */
    updateProject(project: Partial<ProjectSchema>): void {
      this.project = {
        ...this.project,
        ...project,
      };
    },
    /**
     * Initializes the current project.
     */
    initializeProject(project: ProjectSchema): void {
      this.project = project;

      selectionStore.clearSelections();
      membersStore.initializeProject(project);
      typeOptionsStore.initializeProject(project);
      documentStore.initializeProject(project);
      subtreeStore.initializeProject(project);
      attributesStore.initializeProject(project);
      warningStore.artifactWarnings = project.warnings;
      this.initializeTim(project);
    },
    /**
     * Initializes the current project's TIM structure.
     */
    initializeTim(project: ProjectSchema): void {
      this.tim = createTIM(project);
    },
    /**
     * Runs the callback only if the project is defined. Otherwise logs a warning.
     *
     * @param cb - The callback to run.
     */
    ifProjectDefined(cb: () => void): void {
      if (this.isProjectDefined) {
        cb();
      } else {
        logStore.onWarning("Please select a project.");
      }
    },
    /**
     * Adds or replaces a project in the project list.
     *
     * @param project - The project to add.
     */
    addProject(project: IdentifierSchema): void {
      this.allProjects = [
        project,
        ...this.allProjects.filter(
          ({ projectId }) => projectId !== project.projectId
        ),
      ];
    },
  },
});

export default useProject(pinia);

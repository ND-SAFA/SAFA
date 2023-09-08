import { defineStore } from "pinia";
import {
  IdentifierSchema,
  ProjectSchema,
  GenerationModelSchema,
  VersionSchema,
} from "@/types";
import { buildProject, buildProjectIdentifier, removeMatches } from "@/util";
import { pinia } from "@/plugins";
import selectionStore from "../graph/useSelection";
import logStore from "../core/useLog";
import membersStore from "./useMembers";
import warningStore from "./useWarnings";
import documentStore from "./useDocuments";
import subtreeStore from "./useSubtree";
import attributesStore from "./useAttributes";
import timStore from "./useTIM";

/**
 * Manages the selected project.
 */
export const useProject = defineStore("project", {
  state: () => ({
    /**
     * The currently loaded project.
     */
    project: buildProject(),
    /**
     * All projects the user has access to.
     */
    allProjects: [] as IdentifierSchema[],
  }),
  getters: {
    /**
     * @return All projects that have not been loaded.
     */
    unloadedProjects(): IdentifierSchema[] {
      return this.allProjects.filter(
        ({ projectId }) => projectId !== this.projectId
      );
    },
    /**
     * @return The full project identifier.
     */
    projectIdentifier(): IdentifierSchema {
      return buildProjectIdentifier(this.project);
    },
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
  },
  actions: {
    /**
     * Adds a project to the list of all projects.
     * @param project - The project to add.
     */
    addProject(project: IdentifierSchema): void {
      this.allProjects = [
        project,
        ...removeMatches(this.allProjects, "projectId", [project.projectId]),
      ];
    },
    /**
     * Removes a project to the list of all projects.
     * @param project - The project to remove.
     */
    removeProject(project: IdentifierSchema): void {
      this.allProjects = removeMatches(this.allProjects, "projectId", [
        project.projectId,
      ]);
    },
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
      timStore.initializeProject(project);
      documentStore.initializeProject(project);
      subtreeStore.initializeProject(project);
      attributesStore.initializeProject(project);
      warningStore.artifactWarnings = project.warnings;
    },
  },
});

export default useProject(pinia);

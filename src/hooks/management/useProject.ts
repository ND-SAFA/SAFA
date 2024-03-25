import { defineStore } from "pinia";
import {
  IdentifierSchema,
  MinimalProjectSchema,
  ProjectSchema,
  VersionSchema,
} from "@/types";
import { buildProject, buildProjectIdentifier, removeMatches } from "@/util";
import {
  attributesStore,
  documentStore,
  layoutStore,
  logStore,
  membersStore,
  selectionStore,
  subtreeStore,
  timStore,
} from "@/hooks";
import { pinia } from "@/plugins";

/**
 * Manages the selected project.
 */
export const useProject = defineStore("project", {
  state: () => ({
    /**
     * The currently loaded project.
     */
    project: buildProject() as MinimalProjectSchema,
    /**
     * All projects the user has access to.
     */
    allProjects: [] as IdentifierSchema[],
    /**
     * All versions for the currently loaded project.
     */
    allVersions: [] as VersionSchema[],
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
     * @return An overview of the current project.
     */
    overview(): string {
      return this.project.specification || this.project.description;
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
     * @param onCurrentRemoved - A callback to run if the current project is removed.
     */
    removeProject(
      project: IdentifierSchema,
      onCurrentRemoved?: () => void
    ): void {
      this.allProjects = removeMatches(this.allProjects, "projectId", [
        project.projectId,
      ]);

      if (project.projectId === this.projectId) {
        onCurrentRemoved?.();
      }
    },
    /**
     * Updates the current project.
     *
     * @param project - The new project fields.
     */
    updateProject(project: Partial<MinimalProjectSchema>): void {
      this.project = {
        ...this.project,
        ...project,
      };
    },
    /**
     * Removes a version to the list of all versions.
     * @param version - The version to remove.
     * @param onCurrentRemoved - A callback to run if the current version is removed.
     */
    removeVersion(
      version: VersionSchema,
      onCurrentRemoved?: (newVersion: VersionSchema) => void
    ): void {
      this.allVersions = removeMatches(this.allVersions, "versionId", [
        version.versionId,
      ]);

      if (version.versionId === this.versionId) {
        this.project.projectVersion = this.allVersions[0];
        onCurrentRemoved?.(this.project.projectVersion);
      }
    },
    /**
     * Initializes the current project.
     */
    initializeProject(project: ProjectSchema): void {
      this.project = project;

      layoutStore.mode = "tim";
      selectionStore.clearSelections();
      timStore.initializeProject(project);
      subtreeStore.initializeProject(project);
      documentStore.initializeProject(project); // Must be after subtree store reset.
      attributesStore.initializeProject(project);
      membersStore.initialize(project.members, "PROJECT");
    },
  },
});

export default useProject(pinia);

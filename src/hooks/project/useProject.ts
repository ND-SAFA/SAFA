import { defineStore } from "pinia";
import {
  MembershipModel,
  ProjectModel,
  TrainedModel,
  VersionModel,
} from "@/types";
import { createProject, removeMatches } from "@/util";
import { pinia } from "@/plugins";
import selectionStore from "@/hooks/graph/useSelection";
import logStore from "../core/useLog";
import warningStore from "./useWarnings";
import documentStore from "./useDocuments";
import subtreeStore from "./useSubtree";
import typeOptionsStore from "./useTypeOptions";

/**
 * Manages the selected project.
 */
export const useProject = defineStore("project", {
  state: () => ({
    /**
     * The currently loaded project.
     */
    project: createProject(),
    /**
     * The current project's models.
     */
    models: [] as TrainedModel[],
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
    version(): VersionModel | undefined {
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
  },
  actions: {
    /**
     * Updates the current project.
     *
     * @param project - The new project fields.
     */
    updateProject(project: Partial<ProjectModel>): void {
      this.project = {
        ...this.project,
        ...project,
      };
    },
    /**
     * Updates the current project members.
     *
     * @param updatedMembers - The updated members.
     */
    updateMembers(updatedMembers: MembershipModel[]): void {
      const ids = updatedMembers.map((member) => member.projectMembershipId);

      this.updateProject({
        members: [
          ...removeMatches(this.project.members, "projectMembershipId", ids),
          ...updatedMembers,
        ],
      });
    },
    /**
     * Deletes from the current project members.
     *
     * @param deletedMembers - The member ids to delete.
     */
    deleteMembers(deletedMembers: string[]): void {
      this.updateProject({
        members: removeMatches(
          this.project.members,
          "projectMembershipId",
          deletedMembers
        ),
      });
    },
    /**
     * Initializes the current project.
     */
    initializeProject(project: ProjectModel): void {
      this.project = project;

      selectionStore.clearSelections();
      typeOptionsStore.initializeProject(project);
      documentStore.initializeProject(project);
      subtreeStore.initializeProject(project);
      warningStore.artifactWarnings = project.warnings;
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
  },
});

export default useProject(pinia);

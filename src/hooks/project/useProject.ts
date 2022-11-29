import { defineStore } from "pinia";
import {
  IdentifierModel,
  MembershipModel,
  ProjectModel,
  GenerationModel,
  VersionModel,
  InstallationModel,
  AttributeModel,
} from "@/types";
import { createProject, removeMatches } from "@/util";
import { pinia } from "@/plugins";
import sessionStore from "../core/useSession";
import selectionStore from "../graph/useSelection";
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
     * All projects available to the current user.
     */
    allProjects: [] as IdentifierModel[],
    /**
     * The currently loaded project.
     */
    project: createProject(),
    /**
     * The 3rd party installations linked to the current project.
     */
    installations: [] as InstallationModel[],
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
    /**
     * @return The current project's models.
     */
    models(): GenerationModel[] {
      return this.project.models;
    },
    /**
     * @return The current project's models.
     */
    attributes(): AttributeModel[] {
      return this.project.attributes?.items || [];
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
    unloadedProjects(): IdentifierModel[] {
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
      // TODO: remove testing code.
      project.attributes = {
        items: [
          {
            key: "str",
            label: "Custom String",
            type: "text",
            min: 4,
            max: 4,
          },
          {
            key: "int",
            label: "Custom Int",
            type: "int",
            min: 0,
            max: 5,
          },
          {
            key: "sel",
            label: "Custom Select",
            type: "select",
            options: ["A", "B", "C"],
          },
          {
            key: "multi",
            label: "Custom Multiselect",
            type: "multiselect",
            options: ["A", "B", "C"],
            min: 1,
            max: 2,
          },
          {
            key: "date",
            label: "Custom Date",
            type: "date",
          },
          {
            key: "float",
            label: "Custom Float",
            type: "float",
          },
          {
            key: "bool",
            label: "Custom Boolean",
            type: "boolean",
          },
          {
            key: "rel",
            label: "Custom Relation",
            type: "relation",
          },
          {
            key: "par",
            label: "Custom Paragraph",
            type: "paragraph",
          },
        ],
        defaultLayout: [
          { x: 0, y: 0, width: 1, height: 1, key: "str" },
          { x: 1, y: 0, width: 1, height: 1, key: "bool" },

          { x: 0, y: 1, width: 1, height: 1, key: "date" },

          { x: 0, y: 2, width: 1, height: 1, key: "int" },
          { x: 1, y: 2, width: 1, height: 1, key: "float" },

          { x: 0, y: 3, width: 1, height: 1, key: "sel" },
          { x: 1, y: 3, width: 1, height: 1, key: "rel" },

          { x: 0, y: 4, width: 2, height: 1, key: "multi" },

          { x: 0, y: 5, width: 2, height: 1, key: "par" },
        ],
        layouts: [],
      };

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
    /**
     * Adds or replaces a project in the project list.
     *
     * @param project - The project to add.
     */
    addProject(project: IdentifierModel): void {
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

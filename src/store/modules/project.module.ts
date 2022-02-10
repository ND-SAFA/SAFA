import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";

import type {
  Project,
  ProjectDocument,
  ProjectIdentifier,
  ProjectMembership,
} from "@/types";
import { createProject } from "@/util";
import { documentModule } from "@/store";

@Module({ namespaced: true, name: "project" })
/**
 * This module tracks the currently loaded project.
 */
export default class ProjectModule extends VuexModule {
  /**
   * The currently loaded project.
   */
  private project = createProject();

  @Action
  /**
   * Initializes the current project
   */
  initializeProject(project: Project): void {
    this.SAVE_PROJECT(project);
    documentModule.initializeProject(project);
  }

  @Action
  /**
   * Updates the project documents.
   */
  updateDocuments(documents: ProjectDocument[]): void {
    this.SET_DOCUMENTS(documents);
    documentModule.initializeProject(this.project);
  }

  @Mutation
  /**
   * Sets a new project.
   *
   * @param project - The new project to track.
   */
  SET_PROJECT_IDENTIFIER(project: ProjectIdentifier): void {
    this.project = {
      ...this.project,
      name: project.name,
      description: project.description,
    };
  }

  @Mutation
  /**
   * Sets a new project.
   *
   * @param project - The new project to track.
   */
  SAVE_PROJECT(project: Project): void {
    this.project = project;
  }

  @Mutation
  /**
   * Sets the members of current project.
   */
  SET_MEMBERS(members: ProjectMembership[]): void {
    this.project.members = members;
  }

  @Mutation
  /**
   * Sets the current documents in the project.
   */
  SET_DOCUMENTS(documents: ProjectDocument[]): void {
    this.project.documents = documents;
  }

  /**
   * @return The current project.
   */
  get getProject(): Project {
    return this.project;
  }

  /**
   * @return The current project id.
   */
  get projectId(): string {
    return this.project.projectId;
  }

  /**
   * @return The current version id.
   */
  get versionId(): string | undefined {
    return this.project.projectVersion?.versionId;
  }

  /**
   * Returns whether project is defined
   *
   * @returns Boolean representing whether project is defined.
   */
  get isProjectDefined(): boolean {
    return this.project.projectId !== "";
  }
}

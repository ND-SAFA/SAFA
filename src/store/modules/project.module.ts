import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";

import type {
  ArtifactType,
  Project,
  ProjectDocument,
  ProjectIdentifier,
  ProjectMembership,
} from "@/types";
import { createProject } from "@/util";
import {
  artifactModule,
  documentModule,
  logModule,
  subtreeModule,
  traceModule,
  typeOptionsModule,
} from "@/store";
import { Artifact, TraceLink } from "@/types";
import { reloadDocumentArtifacts } from "@/api";

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
  async initializeProject(project: Project): Promise<void> {
    this.SAVE_PROJECT(project);
    documentModule.initializeProject(project);
    typeOptionsModule.initializeTypeIcons(project.artifactTypes);

    await setTimeout(async () => {
      // Not sure why this needs any wait, but it doesnt work without it.
      await subtreeModule.initializeProject(project);
    }, 100);
  }

  @Action
  /**
   * Updates the project documents.
   */
  async updateDocuments(documents: ProjectDocument[]): Promise<void> {
    this.SET_DOCUMENTS(documents);
    await documentModule.updateDocuments(documents);
  }

  @Action
  /**
   * Updates the current artifacts in the project, preserving any that already existed.
   *
   * @param artifacts - The artifacts to set.
   */
  async addOrUpdateArtifacts(newArtifacts: Artifact[]): Promise<void> {
    const newIds = newArtifacts.map(({ id }) => id);
    const updatedArtifacts = [
      ...this.project.artifacts.filter(({ id }) => !newIds.includes(id)),
      ...newArtifacts,
    ];

    this.SET_ARTIFACTS(updatedArtifacts);
    await reloadDocumentArtifacts();
    await artifactModule.addOrUpdateArtifacts(updatedArtifacts);
    await subtreeModule.updateSubtreeMap();
  }

  @Action
  /**
   * Deletes the artifact with the given name.
   */
  async deleteArtifacts(artifacts: Artifact[]): Promise<void> {
    if (artifacts.length === 0) return;

    const deletedNames = artifacts.map(({ name }) => name);

    this.SET_ARTIFACTS(
      this.project.artifacts.filter(({ name }) => !deletedNames.includes(name))
    );
    await artifactModule.deleteArtifacts(artifacts);
    await subtreeModule.updateSubtreeMap();
  }

  @Action
  /**
   * Updates the current trace links in the project, preserving any that already existed.
   *
   * @param traceLinks - The trace links to set.
   */
  async addOrUpdateTraceLinks(newTraces: TraceLink[]): Promise<void> {
    const newIds = newTraces.map(({ traceLinkId }) => traceLinkId);
    const updatedTraces = [
      ...this.project.traces.filter(
        ({ traceLinkId }) => !newIds.includes(traceLinkId)
      ),
      ...newTraces,
    ];

    this.SET_TRACES(updatedTraces);
    await traceModule.addOrUpdateTraceLinks(updatedTraces);
    await subtreeModule.updateSubtreeMap();
  }

  @Action
  /**
   * Deletes the given trace link.
   *
   * @param traceLink - The trace link to remove.
   */
  async deleteTraceLink(traceLink: TraceLink): Promise<void> {
    this.SET_TRACES(
      this.project.traces.filter(
        ({ traceLinkId }) => traceLinkId !== traceLink.traceLinkId
      )
    );
    await traceModule.deleteTraceLink(traceLink);
    await subtreeModule.updateSubtreeMap();
  }

  @Action
  /**
   * Adds a new artifact type.
   *
   * @param artifactType - The artifact type to add.
   */
  addOrUpdateArtifactType(artifactType: ArtifactType): void {
    const unaffectedTypes = this.project.artifactTypes.filter(
      (a) => a.typeId !== artifactType.typeId
    );
    const allArtifactTypes = [...unaffectedTypes, artifactType];

    this.SET_ARTIFACT_TYPES(allArtifactTypes);
    typeOptionsModule.SET_TYPES(allArtifactTypes);
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
   * Sets the current artifacts in the project.
   */
  SET_ARTIFACTS(artifacts: Artifact[]): void {
    this.project.artifacts = artifacts;
  }

  @Mutation
  /**
   * Sets the current trace links in the project.
   */
  SET_TRACES(traces: TraceLink[]): void {
    this.project.traces = traces;
  }

  @Mutation
  /**
   * Sets the current documents in the project.
   */
  SET_DOCUMENTS(documents: ProjectDocument[]): void {
    this.project.documents = documents;
  }

  @Mutation
  /**
   * Sets the current artifact type in the project.
   */
  SET_ARTIFACT_TYPES(artifactTypes: ArtifactType[]): void {
    this.project.artifactTypes = artifactTypes;
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
   * Returns the version ID, and logs an error if there isnt one.
   * @return The current version id.
   */
  get versionIdWithLog(): string | undefined {
    if (!this.versionId) {
      logModule.onWarning("Please select a project version.");
    }

    return this.versionId;
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

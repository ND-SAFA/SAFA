import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";
import type {
  Artifact,
  ArtifactQueryFunction,
  Project,
  ProjectIdentifier,
  TraceLink,
} from "@/types";
import { LinkValidator } from "@/types";
import { artifactSelectionModule, subtreeModule } from "@/store";
import { createProject, getSingleQueryResult, getTraceId } from "@/util";

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
   * Updates the current trace links in the project, preserving any that already existed.
   *
   * @param traceLinks - The trace links to set.
   */
  async addOrUpdateTraceLinks(traceLinks: TraceLink[]): Promise<void> {
    this.ADD_OR_UPDATE_TRACE_LINKS(traceLinks);
    await subtreeModule.updateSubtreeMap();
  }

  @Action
  /**
   * Updates the current artifacts in the project, preserving any that already existed.
   *
   * @param artifacts - The artifacts to set.
   */
  async addOrUpdateArtifacts(artifacts: Artifact[]): Promise<void> {
    this.ADD_OR_UPDATE_ARTIFACTS(artifacts);
    const selectedArtifact = artifactSelectionModule.getSelectedArtifact;

    if (selectedArtifact !== undefined) {
      const query = artifacts.filter((a) => a.name === selectedArtifact.name);
      if (query.length > 0) {
        await artifactSelectionModule.selectArtifact(query[0].id);
      }
    }

    await subtreeModule.updateSubtreeMap();
  }

  @Action
  /**
   * Removes the given trace link.
   *
   * @param traceLink - The trace link to remove.
   */
  async removeTraceLink(traceLink: TraceLink): Promise<void> {
    this.REMOVE_TRACE_LINK(traceLink);
    await subtreeModule.updateSubtreeMap();
  }

  @Action
  /**
   * Deletes artifact and updates subtree map.
   */
  async deleteArtifactByName(artifactName: string): Promise<void> {
    this.DELETE_ARTIFACT_BY_NAME(artifactName);
    await subtreeModule.updateSubtreeMap();
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
   * Updates the current trace links in the project, preserving any that already existed.
   *
   * @param traceLinks - The trace links to set.
   */
  ADD_OR_UPDATE_TRACE_LINKS(traceLinks: TraceLink[]): void {
    const traceLinkIds = traceLinks.map((t) => t.traceLinkId);
    const unaffected = this.project.traces.filter(
      (link) => !traceLinkIds.includes(link.traceLinkId)
    );
    this.project.traces = [...unaffected, ...traceLinks];
  }

  @Mutation
  /**
   * Removes the given trace link.
   *
   * @param traceLink - The trace link to remove.
   */
  REMOVE_TRACE_LINK(traceLink: TraceLink): void {
    this.project.traces = this.project.traces.filter(
      (link) => link.traceLinkId !== traceLink.traceLinkId
    );
  }

  @Mutation
  /**
   * Deletes given artifact.
   *
   * @param artifactName - The artifact to remove.
   */
  DELETE_ARTIFACT_BY_NAME(artifactName: string): void {
    this.project.artifacts = this.project.artifacts.filter(
      (a) => a.name !== artifactName
    );
  }

  @Mutation
  /**
   * Updates the current artifacts in the project, preserving any that already existed.
   *
   * @param artifacts - The artifacts to set.
   */
  ADD_OR_UPDATE_ARTIFACTS(artifacts: Artifact[]): void {
    const newArtifactIds = artifacts.map((a) => a.id);
    const unaffected = this.project.artifacts.filter(
      (a) => !newArtifactIds.includes(a.id)
    );
    this.project.artifacts = [...unaffected, ...artifacts];
  }

  /**
   * @return The current project.
   */
  get getProject(): Project {
    return this.project;
  }

  /**
   * Returns whether project is defined
   *
   * @returns Boolean representing whether project is defined.
   */
  get isProjectDefined(): boolean {
    return this.project.projectId !== "";
  }

  /**
   * @return The current project artifacts.
   */
  get artifacts(): Artifact[] {
    return this.project.artifacts;
  }

  /**
   * @return A function for finding an artifact by name.
   * @throws If exactly 1 artifact is found to match.
   */
  get getArtifactByName(): ArtifactQueryFunction {
    return (artifactName) => {
      const query = this.artifacts.filter((a) => a.name === artifactName);

      return getSingleQueryResult(query, `Find by name: ${artifactName}`);
    };
  }

  /**
   * @return A function for finding an artifact by id.
   * @throws If exactly 1 artifact is found to match.
   */
  get getArtifactById(): ArtifactQueryFunction {
    return (targetArtifactId) => {
      const query = this.artifacts.filter((a) => a.id === targetArtifactId);

      return getSingleQueryResult(query, `Find by id: ${targetArtifactId}`);
    };
  }

  /**
   * @return A collection of artifacts, keyed by their id.
   */
  get getArtifactsById(): Record<string, Artifact> {
    return this.artifacts
      .map((artifact) => ({ [artifact.id]: artifact }))
      .reduce((acc, cur) => ({ ...acc, ...cur }), {});
  }

  /**
   * @return All trace links in the current project.
   */
  get traceLinks(): TraceLink[] {
    return this.project.traces;
  }

  /**
   * @return Returns a function to query a single trace link by the
   * source and target artifact ids.
   */
  get getTraceLinkByArtifacts(): (
    sourceId: string,
    targetId: string
  ) => TraceLink {
    return (sourceId, targetId) => {
      const traceQuery = this.traceLinks.filter(
        (t) => t.sourceId === sourceId && t.targetId === targetId
      );

      if (traceQuery.length === 0) {
        throw Error(
          `Could not find trace link with id: ${getTraceId(sourceId, targetId)}`
        );
      }

      return traceQuery[0];
    };
  }

  /**
   * @return A function that determines whether a link with the given source and target IDs exists.
   */
  get doesLinkExist(): LinkValidator {
    return (sourceId, targetId) => {
      const traceLinkQuery = this.traceLinks.filter(
        (t) =>
          (t.sourceId === sourceId && t.targetId === targetId) ||
          (t.targetId === sourceId && t.sourceId === targetId)
      );
      return traceLinkQuery.length > 0;
    };
  }
}

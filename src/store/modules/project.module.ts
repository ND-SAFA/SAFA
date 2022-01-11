import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";
import type {
  Artifact,
  ArtifactDirection,
  ArtifactQueryFunction,
  Project,
  ProjectIdentifier,
  TraceLink,
  ArtifactTypeDirections,
} from "@/types";
import { LinkValidator } from "@/types";
import { logModule, artifactSelectionModule, subtreeModule } from "@/store";
import { createProject } from "@/util";

@Module({ namespaced: true, name: "project" })
/**
 * This module tracks the currently loaded project.
 */
export default class ProjectModule extends VuexModule {
  /**
   * The currently loaded project.
   */
  private project = createProject();

  /**
   * A mapping of the allowed directions of traces between artifacts.
   */
  private artifactTypeDirections: ArtifactTypeDirections = {};

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

  @Action({ rawError: true })
  /**
   * Updates what directions of trace links between artifacts are allowed.
   */
  updateAllowedTraceDirections(): void {
    const allowedDirections: ArtifactTypeDirections = {};

    // Ensure that all artifact types appear in mapping.
    this.artifacts.forEach((artifact) => {
      allowedDirections[artifact.type] = [];
    });

    this.traceLinks.forEach(({ sourceId, targetId }) => {
      try {
        const sourceType = this.getArtifactById(sourceId).type;
        const targetType = this.getArtifactById(targetId).type;

        if (!allowedDirections[sourceType].includes(targetType)) {
          allowedDirections[sourceType].push(targetType);
        }
      } catch (e) {
        logModule.onDevMessage(
          `Unable to calculate allowed trace directions: ${e}`
        );
      }
    });

    this.SET_TRACE_DIRECTIONS(allowedDirections);
  }

  @Action
  /**
   * Changes what directions of trace links between artifacts are allowed.
   */
  editAllowedTraceDirections({ type, allowedTypes }: ArtifactDirection): void {
    this.SET_TRACE_DIRECTIONS({
      ...this.artifactTypeDirections,
      [type]: allowedTypes,
    });
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
    this.project.traces = unaffected.concat(traceLinks);
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
    this.project.artifacts = unaffected.concat(artifacts);
  }

  @Mutation
  /**
   * Sets a new collection of allowed directions between artifact types.
   *
   * @param artifactTypeDirections - Directions between artifact types to allow.
   */
  SET_TRACE_DIRECTIONS(artifactTypeDirections: ArtifactTypeDirections): void {
    this.artifactTypeDirections = artifactTypeDirections;
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
   * Returns the artifact in list if single item exists.
   *
   * @return The found artifact.
   *
   * @throws Error if query contains multiple or no results.
   */
  get getSingleQueryResult(): (
    query: Artifact[],
    queryName: string
  ) => Artifact {
    /**
     * @param query - List of artifacts representing some query for an artifact.
     * @param queryName - The name of the operation to log if operation fails.
     */
    return (query, queryName) => {
      let error = "";
      switch (query.length) {
        case 1:
          return query[0];
        case 0:
          error = `Query resulted in empty results: ${queryName}`;
          logModule.onWarning(error);
          throw Error(error);
        default:
          error = `Found more than one result in query: ${queryName}`;
          logModule.onWarning(error);
          throw Error(error);
      }
    };
  }

  /**
   * @return A function for finding an artifact by name.
   */
  get getArtifactByName(): ArtifactQueryFunction {
    return (artifactName) => {
      const query = this.project.artifacts.filter(
        (a) => a.name === artifactName
      );
      return this.getSingleQueryResult(query, `Find by name: ${artifactName}`);
    };
  }

  /**
   * @return A function for finding an artifact by id.
   */
  get getArtifactById(): ArtifactQueryFunction {
    return (targetArtifactId) => {
      const query = this.project.artifacts.filter(
        (a) => a.id === targetArtifactId
      );
      return this.getSingleQueryResult(
        query,
        `Find by id: ${targetArtifactId}`
      );
    };
  }

  /**
   * @return A collection of artifacts, keyed by their id.
   */
  get getArtifactsById(): Record<string, Artifact> {
    return this.project.artifacts
      .map((artifact) => ({ [artifact.id]: artifact }))
      .reduce((acc, cur) => ({ ...acc, ...cur }), {});
  }

  /**
   * @return All artifact types in the current project.
   */
  get getArtifactTypes(): string[] {
    return Array.from(new Set(this.project.artifacts.map((a) => a.type)));
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
      const traceQuery = this.project.traces.filter(
        (t) => t.sourceId === sourceId && t.targetId === targetId
      );

      if (traceQuery.length === 0) {
        const traceId = `${sourceId}-${targetId}`;
        const error = `Could not find trace link with id: ${traceId}`;
        logModule.onDevError(error);
        throw Error(error);
      }

      return traceQuery[0];
    };
  }

  /**
   * @return A function that determines whether a link with the given source and target IDs exists.
   */
  get doesLinkExist(): LinkValidator {
    return (sourceId, targetId) => {
      const traceLinks = this.project.traces;
      const traceLinkQuery = traceLinks.filter(
        (t) =>
          (t.sourceId === sourceId && t.targetId === targetId) ||
          (t.targetId === sourceId && t.sourceId === targetId)
      );
      return traceLinkQuery.length > 0;
    };
  }

  /**
   * Return the allowed directions of traces between artifacts.
   */
  get allowedArtifactTypeDirections(): ArtifactTypeDirections {
    return this.artifactTypeDirections;
  }

  /**
   * @return A function for determining if the trace link is allowed
   * based on the type of the nodes.
   */
  get isLinkAllowedByType(): (
    sourceType: string,
    targetType: string
  ) => boolean {
    return (sourceType, targetType) => {
      return this.allowedArtifactTypeDirections[sourceType]?.includes(
        targetType
      );
    };
  }
}

import { Module, VuexModule, Mutation, Action } from "vuex-module-decorators";
import { connectAndSubscribeToVersion } from "@/api";
import type {
  ProjectCreationResponse,
  Project,
  Artifact,
  TraceLink,
  ChannelSubscriptionId,
  ArtifactQueryFunction,
  ProjectVersion,
} from "@/types";
import { LinkValidator } from "@/types";
import {
  appModule,
  artifactSelectionModule,
  deltaModule,
  errorModule,
  viewportModule,
} from "@/store";

@Module({ namespaced: true, name: "project" })
/**
 * This module tracks the currently loaded project.
 */
export default class ProjectModule extends VuexModule {
  /**
   * The currently loaded project.
   */
  private project: Project = {
    projectId: "",
    description: "",
    name: "Untitled",
    artifacts: [],
    traces: [],
    projectVersion: undefined,
  };

  @Action({ rawError: true })
  /**
   * 1. Sets the current project to the created project.
   * 2. Sets any warnings generated when loading the project.
   * 3. Resets the viewport to frame the new project graph.
   * 4. Disables delta view, if it was enabled.
   *
   * @param res - The response from creating the project.
   */
  async setProjectCreationResponse(
    res: ProjectCreationResponse
  ): Promise<void> {
    await this.setProject(res.project);
    errorModule.setArtifactWarnings(res.warnings);
    await viewportModule.setArtifactTreeLayout();
    deltaModule.setIsDeltaViewEnabled(false);
  }

  @Action
  /**
   * 1. Sets a new project.
   * 2. Subscribes to the new project's version.
   * 3. Clears any deltas to previous projects.
   *
   * @param newProject - The new project to set.
   */
  async setProject(newProject: Project): Promise<void> {
    const projectId = newProject.projectId;
    const versionId = newProject.projectVersion?.versionId;

    this.SAVE_PROJECT(newProject);

    await this.subscribeToVersion({ projectId, versionId });

    deltaModule.clearDelta();
  }

  @Action
  /**
   * Subscribes to a new project version.
   *
   * @param subscriptionId - The project and version ID to subscribe to.
   */
  async subscribeToVersion(
    subscriptionId: ChannelSubscriptionId
  ): Promise<void> {
    const { projectId, versionId } = subscriptionId;

    if (projectId !== undefined && versionId !== undefined) {
      await connectAndSubscribeToVersion(projectId, versionId);
    }
  }

  @Action
  /**
   * Updates the current trace links in the project, preserving any that already existed.
   *
   * @param traceLinks - The trace links to set.
   */
  addOrUpdateTraceLinks(traceLinks: TraceLink[]): void {
    this.ADD_OR_UPDATE_TRACE_LINKS(traceLinks);
  }

  @Action
  /**
   * Updates the current artifacts in the project, preserving any that already existed.
   *
   * @param artifacts - The artifacts to set.
   */
  addOrUpdateArtifacts(artifacts: Artifact[]): void {
    this.ADD_OR_UPDATE_ARTIFACTS(artifacts);
    const selectedArtifact = artifactSelectionModule.getSelectedArtifact;

    if (selectedArtifact !== undefined) {
      const query = artifacts.filter((a) => a.name === selectedArtifact.name);
      if (query.length > 0) {
        artifactSelectionModule.selectArtifact(query[0]);
      }
    }
  }

  @Action
  /**
   * Removes the given trace link.
   *
   * @param traceLink - The trace link to remove.
   */
  removeTraceLink(traceLink: TraceLink): void {
    this.REMOVE_TRACE_LINK(traceLink);
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
    const newArtifactIds = artifacts.map((a) => a.name);
    const unaffected = this.project.artifacts.filter(
      (a) => !newArtifactIds.includes(a.name)
    );
    this.project.artifacts = unaffected.concat(artifacts);
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
  get getArtifacts(): Artifact[] {
    return this.project.artifacts;
  }

  /**
   * @return A function for finding an artifact by name.
   */
  get getArtifactByName(): ArtifactQueryFunction {
    return (artifactName) => {
      const query = this.project.artifacts.filter(
        (a) => a.name === artifactName
      );
      if (query.length === 0) {
        const error = `Could not find artifact with name: ${artifactName}`;
        appModule.onWarning(error);
        throw Error(error);
      } else if (query.length > 1) {
        const error = `Found more than one artifact with name: ${artifactName}`;
        appModule.onWarning(error);
        throw Error(error);
      } else {
        return query[0];
      }
    };
  }

  get helloWorld(): string {
    return "hell world";
  }

  /**
   * @return A collection of artifacts, keyed by their name.
   */
  get getArtifactHashmap(): Record<string, Artifact> {
    return this.project.artifacts
      .map((artifact) => ({ [artifact.name]: artifact }))
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
  get getTraceLinks(): TraceLink[] {
    return this.project.traces;
  }

  /**
   * @return Returns a function to query a single trace link by the
   * source and target artifact names.
   */
  get getTraceLinkByArtifacts(): (s: string, t: string) => TraceLink {
    return (sourceName: string, targetName: string) => {
      const traceQuery = this.project.traces.filter(
        (t) => t.source === sourceName && t.target === targetName
      );
      if (traceQuery.length === 0) {
        const traceId = `${sourceName}-${targetName}`;
        const error = `Could not find trace link with id: ${traceId}`;
        appModule.onDevError(error);
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
      const traceLinks: TraceLink[] = this.project.traces;
      const traceLinkQuery = traceLinks.filter(
        (t) =>
          (t.source === sourceId && t.target === targetId) ||
          (t.target === sourceId && t.source === targetId)
      );
      return traceLinkQuery.length > 0;
    };
  }
}

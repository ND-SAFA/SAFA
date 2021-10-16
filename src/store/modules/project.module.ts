import type { Project } from "@/types/domain/project";
import type { Artifact } from "@/types/domain/artifact";
import type { TraceLink } from "@/types/domain/links";
import { connectAndSubscriptToVersion } from "@/api/revision-api";
import type { ProjectCreationResponse } from "@/types/api";
import { appModule, deltaModule, errorModule, viewportModule } from "@/store";
import { Module, VuexModule, Mutation, Action } from "vuex-module-decorators";

export interface ChannelSubscriptionId {
  projectId?: string;
  versionId?: string;
}

export type ArtifactQueryFunction = (q: string) => Artifact | undefined;

@Module({ namespaced: true, name: "project" })
export default class ProjectModule extends VuexModule {
  project: Project = {
    projectId: "",
    description: "",
    name: "Untitled",
    artifacts: [],
    traces: [],
    projectVersion: undefined,
  };

  @Action
  async setProjectCreationResponse(
    res: ProjectCreationResponse
  ): Promise<void> {
    await this.setProject(res.project);
    errorModule.setArtifactWarnings(res.warnings);
    await viewportModule.setGraphLayout();
  }
  @Action
  async setProject(newProject: Project): Promise<void> {
    this.SAVE_PROJECT(newProject);
    const projectId = newProject.projectId;
    const versionId = newProject.projectVersion?.versionId;
    await this.subscribeToVersion({ projectId, versionId });
    deltaModule.clearDelta();
  }

  @Action
  async subscribeToVersion(
    subscriptionId: ChannelSubscriptionId
  ): Promise<void> {
    const { projectId, versionId } = subscriptionId;
    if (projectId !== undefined && versionId !== undefined) {
      connectAndSubscriptToVersion(projectId, versionId);
    }
  }

  @Action
  addOrUpdateTraceLinks(traceLinks: TraceLink[]): void {
    this.ADD_OR_UPDATE_TRACE_LINKS(traceLinks);
  }

  @Action
  addOrUpdateArtifacts(artifacts: Artifact[]): void {
    this.ADD_OR_UPDATE_ARTIFACTS(artifacts);
  }

  @Action
  removeTraceLink(traceLink: TraceLink): void {
    this.REMOVE_TRACE_LINK(traceLink);
  }

  @Mutation
  SAVE_PROJECT(project: Project): void {
    this.project = project;
  }

  @Mutation
  ADD_OR_UPDATE_TRACE_LINKS(traceLinks: TraceLink[]): void {
    const traceLinkIds = traceLinks.map((t) => t.traceLinkId);
    const unaffected = this.project.traces.filter(
      (link) => !traceLinkIds.includes(link.traceLinkId)
    );
    this.project.traces = unaffected.concat(traceLinks);
  }

  @Mutation
  REMOVE_TRACE_LINK(traceLink: TraceLink): void {
    this.project.traces = this.project.traces.filter(
      (link) => link.traceLinkId !== traceLink.traceLinkId
    );
  }

  @Mutation
  ADD_OR_UPDATE_ARTIFACTS(artifacts: Artifact[]): void {
    const newArtifactIds = artifacts.map((a) => a.name);
    const unaffected = this.project.artifacts.filter(
      (a) => !newArtifactIds.includes(a.name)
    );
    this.project.artifacts = unaffected.concat(artifacts);
  }

  get getProject(): Project {
    return this.project;
  }

  get getArtifacts(): Artifact[] {
    return this.project.artifacts;
  }

  get getArtifactByName(): ArtifactQueryFunction {
    return (artifactName: string) => {
      const query = this.project.artifacts.filter(
        (a) => a.name === artifactName
      );
      if (query.length === 0) {
        appModule.onError(`Could not find artifact with name: ${artifactName}`);
      } else if (query.length > 1) {
        appModule.onWarning(
          `Found more than one artifact with name: ${artifactName}`
        );
      } else {
        return query[0];
      }
    };
  }
  get getArtifactHashmap(): Record<string, Artifact> {
    const artifactMap: Record<string, Artifact> = {};
    this.project.artifacts.forEach((artifact) => {
      artifactMap[artifact.name] = artifact;
    });
    return artifactMap;
  }

  get getArtifactTypes(): string[] {
    return Array.from(new Set(this.project.artifacts.map((a) => a.type)));
  }
  get getTraceLinks(): TraceLink[] {
    return this.project.traces;
  }

  get doesLinkExist(): (s: string, t: string) => boolean {
    return (sourceId: string, targetId: string) => {
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

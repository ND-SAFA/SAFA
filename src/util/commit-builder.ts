import { Artifact, Commit, ProjectVersion, TraceLink } from "@/types";
import { projectModule } from "@/store";
import authHttpClient from "@/api/endpoints/auth-http-client";
import { Endpoint, fillEndpoint } from "@/api/endpoints/endpoints";

/**
 * Responsible for creating a commit and saving it to the database.
 */
export class CommitBuilder {
  /**
   * The commit being built
   */
  commit: Commit;

  constructor(version: ProjectVersion) {
    this.commit = {
      commitVersion: version,
      artifacts: {
        added: [],
        removed: [],
        modified: [],
      },
      traces: {
        added: [],
        removed: [],
        modified: [],
      },
    };
  }
  static withCurrentVersion(): CommitBuilder {
    const version = projectModule.getProject.projectVersion;
    if (version === undefined) {
      throw Error("No project version is selected.");
    }
    return new CommitBuilder(version);
  }
  withNewArtifact(artifact: Artifact): CommitBuilder {
    this.commit.artifacts.added.push(artifact);
    return this;
  }
  withRemovedArtifact(artifact: Artifact): CommitBuilder {
    this.commit.artifacts.removed.push(artifact);
    return this;
  }
  withNewTraceLink(traceLink: TraceLink): CommitBuilder {
    this.commit.traces.added.push(traceLink);
    return this;
  }
  withModifiedTraceLink(traceLink: TraceLink): CommitBuilder {
    this.commit.traces.modified.push(traceLink);
    return this;
  }
  save(): Promise<void> {
    const versionId = this.commit.commitVersion.versionId;
    return authHttpClient<void>(fillEndpoint(Endpoint.commit, { versionId }), {
      method: "POST",
      body: JSON.stringify(this.commit),
    });
  }
}

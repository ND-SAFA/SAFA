import { Artifact, Commit, ProjectVersion, TraceLink } from "@/types";
import { commitModule, projectModule } from "@/store";

/**
 * Responsible for creating a commit and saving it to the database.
 */
export class CommitBuilder {
  /**
   * The commit being built
   */
  commit: Commit;

  constructor(version: ProjectVersion) {
    this.commit = commitModule.emptyCommit(version);
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
  withModifiedArtifact(artifact: Artifact): CommitBuilder {
    this.commit.artifacts.modified.push(artifact);
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
    return commitModule.saveCommit(this.commit);
  }
}

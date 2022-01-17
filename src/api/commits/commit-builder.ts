import { Artifact, Commit, ProjectVersion, TraceLink } from "@/types";
import { projectModule } from "@/store";
import { createCommit } from "@/util";
import { saveCommit } from "./commit-handler";

/**
 * Responsible for creating a commit and saving it to the database.
 */
export class CommitBuilder {
  /**
   * The commit being built
   */
  commit: Commit;

  constructor(version: ProjectVersion) {
    this.commit = createCommit(version);
  }

  static withCurrentVersion(): CommitBuilder {
    const { projectVersion } = projectModule.getProject;
    if (projectVersion === undefined) {
      throw Error("No project version is selected.");
    }
    return new CommitBuilder(projectVersion);
  }
  withNewArtifact(artifact: Artifact): this {
    this.commit.artifacts.added.push(artifact);
    return this;
  }
  withModifiedArtifact(artifact: Artifact): this {
    this.commit.artifacts.modified.push(artifact);
    return this;
  }
  withRemovedArtifact(artifact: Artifact): this {
    this.commit.artifacts.removed.push(artifact);
    return this;
  }
  withNewTraceLink(traceLink: TraceLink): this {
    this.commit.traces.added.push(traceLink);
    return this;
  }
  withModifiedTraceLink(traceLink: TraceLink): this {
    this.commit.traces.modified.push(traceLink);
    return this;
  }
  save(): Promise<void> {
    return saveCommit(this.commit);
  }
}

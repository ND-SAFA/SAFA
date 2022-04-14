import { Artifact, Commit, ProjectVersion, TraceLink } from "@/types";
import { createCommit } from "@/util";
import { projectModule } from "@/store";
import { saveCommit } from "@/api";

/**
 * Responsible for creating a commit and saving it to the database.
 */
export class CommitBuilder {
  /**
   * The commit being built
   */
  commit: Commit;

  /**
   * Creates a commit builder.
   * @param version - The project version to commit to.
   */
  constructor(version: ProjectVersion) {
    this.commit = createCommit(version);
  }

  /**
   * Adds a new artifact to this commit.
   *
   * @param artifact - The artifact to create.
   */
  withNewArtifact(artifact: Artifact): this {
    this.commit.artifacts.added.push(artifact);
    return this;
  }

  /**
   * Adds a modified artifact to this commit.
   *
   * @param artifact - The artifact to modify.
   */
  withModifiedArtifact(artifact: Artifact): this {
    this.commit.artifacts.modified.push(artifact);
    return this;
  }

  /**
   * Adds a removed artifact to this commit.
   *
   * @param artifact - The artifact to remove.
   */
  withRemovedArtifact(artifact: Artifact): this {
    this.commit.artifacts.removed.push(artifact);
    return this;
  }

  /**
   * Adds a new trace link to this commit.
   *
   * @param traceLink - The link to add.
   */
  withNewTraceLink(traceLink: TraceLink): this {
    this.commit.traces.added.push(traceLink);
    return this;
  }

  /**
   * Adds a modified trace link to this commit.
   *
   * @param traceLink - The link to modify.
   */
  withModifiedTraceLink(traceLink: TraceLink): this {
    this.commit.traces.modified.push(traceLink);
    return this;
  }

  /**
   * Saves this commit.
   */
  save(): Promise<Commit> {
    return saveCommit(this.commit);
  }

  /**
   * Creates a new commit based on the current project version.
   */
  static withCurrentVersion(): CommitBuilder {
    const { projectVersion } = projectModule.getProject;
    if (projectVersion === undefined) {
      throw Error("No project version is selected.");
    }
    return new CommitBuilder(projectVersion);
  }
}

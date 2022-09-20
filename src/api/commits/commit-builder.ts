import { ArtifactModel, Commit, VersionModel, TraceLinkModel } from "@/types";
import { createCommit } from "@/util";
import { projectStore } from "@/hooks";
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
  constructor(version: VersionModel) {
    this.commit = createCommit(version);
  }

  /**
   * Hides errors from the commit.
   */
  hideErrors(): this {
    this.commit.failOnError = false;
    return this;
  }

  /**
   * Adds a new artifact to this commit.
   *
   * @param artifact - The artifact to create.
   */
  withNewArtifact(artifact: ArtifactModel): this {
    this.commit.artifacts.added.push(artifact);
    return this;
  }

  /**
   * Adds a modified artifact to this commit.
   *
   * @param artifact - The artifact to modify.
   */
  withModifiedArtifact(artifact: ArtifactModel): this {
    this.commit.artifacts.modified.push(artifact);
    return this;
  }

  /**
   * Adds a removed artifact to this commit.
   *
   * @param artifact - The artifact to remove.
   */
  withRemovedArtifact(artifact: ArtifactModel): this {
    this.commit.artifacts.removed.push(artifact);
    return this;
  }

  /**
   * Adds a new trace link to this commit.
   *
   * @param traceLink - The link to add.
   */
  withNewTraceLink(traceLink: TraceLinkModel): this {
    this.commit.traces.added.push(traceLink);
    return this;
  }

  /**
   * Adds multiple new trace links to this commit.
   *
   * @param traceLinks - The links to add.
   */
  withNewTraceLinks(traceLinks: TraceLinkModel[]): this {
    this.commit.traces.added.push(...traceLinks);
    return this;
  }

  /**
   * Adds a modified trace link to this commit.
   *
   * @param traceLink - The link to modify.
   */
  withModifiedTraceLink(traceLink: TraceLinkModel): this {
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
    const version = projectStore.version;

    if (version === undefined) {
      throw Error("No project version is selected.");
    }

    return new CommitBuilder(version);
  }
}

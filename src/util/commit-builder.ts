import {
  ArtifactSchema,
  CommitSchema,
  VersionSchema,
  TraceLinkSchema,
} from "@/types";
import { createCommit } from "@/util";

/**
 * Responsible for creating a commit of changes.
 */
export class CommitBuilder {
  /**
   * The commit being built
   */
  commit: CommitSchema;

  /**
   * Creates a commit builder.
   * @param version - The project version to commit to.
   */
  constructor(version: VersionSchema) {
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
  withNewArtifact(artifact: ArtifactSchema): this {
    this.commit.artifacts.added.push(artifact);
    return this;
  }

  /**
   * Adds a modified artifact to this commit.
   *
   * @param artifact - The artifact to modify.
   */
  withModifiedArtifact(artifact: ArtifactSchema): this {
    this.commit.artifacts.modified.push(artifact);
    return this;
  }

  /**
   * Adds a removed artifact to this commit.
   *
   * @param artifact - The artifact to remove.
   */
  withRemovedArtifact(artifact: ArtifactSchema): this {
    this.commit.artifacts.removed.push(artifact);
    return this;
  }

  /**
   * Adds a new trace link to this commit.
   *
   * @param traceLink - The link to add.
   */
  withNewTraceLink(traceLink: TraceLinkSchema): this {
    this.commit.traces.added.push(traceLink);
    return this;
  }

  /**
   * Adds multiple new trace links to this commit.
   *
   * @param traceLinks - The links to add.
   */
  withNewTraceLinks(traceLinks: TraceLinkSchema[]): this {
    this.commit.traces.added.push(...traceLinks);
    return this;
  }

  /**
   * Adds a modified trace link to this commit.
   *
   * @param traceLinks - The links to modify.
   */
  withModifiedTraceLink(...traceLinks: TraceLinkSchema[]): this {
    this.commit.traces.modified.push(...traceLinks);
    return this;
  }
}

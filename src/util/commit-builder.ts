import {
  ArtifactSchema,
  CommitSchema,
  VersionSchema,
  TraceLinkSchema,
} from "@/types";
import { buildCommit } from "@/util";

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
    this.commit = buildCommit(version);
  }

  /**
   * Hides errors from the commit.
   */
  hideErrors(): this {
    this.commit.failOnError = false;
    return this;
  }

  /**
   * Adds new artifacts to this commit.
   *
   * @param artifacts - The artifacts to create.
   */
  withNewArtifact(...artifacts: ArtifactSchema[]): this {
    this.commit.artifacts.added.push(...artifacts);
    return this;
  }

  /**
   * Adds modified artifacts to this commit.
   *
   * @param artifacts - The artifacts to modify.
   */
  withModifiedArtifact(...artifacts: ArtifactSchema[]): this {
    this.commit.artifacts.modified.push(...artifacts);
    return this;
  }

  /**
   * Adds removed artifacts to this commit.
   *
   * @param artifacts - The artifacts to remove.
   */
  withRemovedArtifact(...artifacts: ArtifactSchema[]): this {
    this.commit.artifacts.removed.push(...artifacts);
    return this;
  }

  /**
   * Adds new trace links to this commit.
   *
   * @param traceLinks - The links to add.
   */
  withNewTraceLink(...traceLinks: TraceLinkSchema[]): this {
    this.commit.traces.added.push(...traceLinks);
    return this;
  }

  /**
   * Adds modified trace links to this commit.
   *
   * @param traceLinks - The links to modify.
   */
  withModifiedTraceLink(...traceLinks: TraceLinkSchema[]): this {
    this.commit.traces.modified.push(...traceLinks);
    return this;
  }
}

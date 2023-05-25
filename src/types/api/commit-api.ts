import { ArtifactSchema, VersionSchema, TraceLinkSchema } from "@/types";

/**
 * Represents a single commit containing one or more changes to
 * either artifacts or trace links
 */
export interface CommitSchema {
  /**
   * The version this commit is being made on.
   */
  commitVersion: VersionSchema;
  /**
   * The changes occurring to the project artifacts.
   */
  artifacts: EntityCommitSchema<ArtifactSchema>;
  /**
   * The changes occurring to project traces.
   */
  traces: EntityCommitSchema<TraceLinkSchema>;
  /**
   * If false, errors will be silent.
   */
  failOnError?: boolean;
}

/**
 * Encapsulates the changes for a generic type of project entity.
 */
export interface EntityCommitSchema<T> {
  /**
   * The entities that were added.
   */
  added: T[];
  /**
   * The entities that were removed
   */
  removed: T[];
  /**
   * The entities that were modified.
   */
  modified: T[];
}

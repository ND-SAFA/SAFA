import { Artifact, ProjectVersion, TraceLink } from "@/types";

/**
 * Represents a single commit containing one or more changes to
 * either artifacts or trace links
 */
export interface Commit {
  /**
   * The version this commit is being made on.
   */
  commitVersion: ProjectVersion;
  /**
   * The changes occurring to the project artifacts.
   */
  artifacts: EntityCommit<Artifact>;
  /**
   * The changes occurring to project traces.
   */
  traces: EntityCommit<TraceLink>;
}

/**
 * Encapsulates the changes for a generic type of project entity.
 */
export interface EntityCommit<T> {
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

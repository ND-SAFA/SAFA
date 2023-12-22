/**
 * Represents a GitHub import request.
 */
export interface GitHubImportSchema {
  /**
   * The organization to import to.
   */
  orgId?: string;
  /**
   * The team to import to.
   */
  teamId?: string;
  /**
   * The branch to import.
   */
  branch?: string;
  /**
   * File patterns to include.
   * Matches based on java's default globbing.
   * See https://docs.oracle.com/en/java/javase/16/docs/api/java.base/java/nio/file/FileSystem.html#getPathMatcher(java.lang.String)
   */
  include?: string[];
  /**
   * File patterns to exclude.
   * Matches based on java's default globbing.
   * See https://docs.oracle.com/en/java/javase/16/docs/api/java.base/java/nio/file/FileSystem.html#getPathMatcher(java.lang.String)
   */
  exclude?: string[];
  /**
   * The artifact type id to import as.
   */
  artifactType?: string;
  /**
   * Whether to generate artifact summaries and a project overview.
   */
  summarize?: boolean;
}

/**
 * Represents a GitHub installation (authorized organization).
 */
export interface GitHubOrganizationSchema {
  /**
   * The installation's unique id.
   */
  id: string;
  /**
   * The installation's name.
   */
  name: string;
}

/**
 * Defines a GitHub repository.
 */
export interface GitHubProjectSchema {
  /**
   * The project's id.
   */
  id: string;
  /**
   * The project's name.
   */
  name: string;
  /**
   * The project's description.
   */
  description: string;
  /**
   * The project's url.
   */
  url?: string;
  /**
   * The project's size.
   */
  size: number;
  /**
   * A timestamp for the project was created.
   */
  creationDate: string;
  /**
   * The owner of this project.
   */
  owner: string;
  /**
   * The list of active branches in this repository.
   */
  branches: string[];
  /**
   * The default branch for this repository.
   */
  defaultBranch: string;
}

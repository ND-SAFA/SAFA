/**
 * Container for the project entity to update
 * along with the initiator.
 */
export interface ProjectMessage {
  type: ProjectMessageType;
  user: string;
}

/**
 * Enumerates the type of notification messages that signal
 * that a project meta entity should be updated.
 */
export enum ProjectMessageType {
  MEMBERS = "MEMBERS",
  DOCUMENTS = "DOCUMENTS",
  META = "META",
}

/**
 * Container for the versioned entity to update
 * along with the initiator.
 */
export interface VersionMessage {
  type: VersionMessageType;
  user: string;
}

/**
 * Enumerates the types of notifications messages that trigger
 * updates of the versioned entities
 */
export enum VersionMessageType {
  VERSION = "VERSION",
  ARTIFACTS = "ARTIFACTS",
  TRACES = "TRACES",
  WARNINGS = "WARNINGS",
}

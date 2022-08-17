/**
 * Container for the project entity to update
 * along with the initiator.
 */
export interface ProjectMessageModel {
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
export interface VersionMessageModel {
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

/**
 * Notifies client of a series of changes to the project.
 *
 */
export interface EntityChangeMessage {
  /**
   * The user initiating the change.
   */
  user: string;
  /**
   * List of changes occurring to project.
   * Each change depicts what entity was affected, how it was affected
   * (UPDATED / DELETED), and the affected entity ids).
   */
  changes: Change[];
  /**
   * Includes whether the default document layout should be updated.
   * This is true if any artifacts or trace links where changed.
   */
  updateLayout: boolean;
}

/**
 * Represents list of changed entities.
 */
export interface Change {
  entity: Entity;
  action: Action;
  entityIds: string[];
}

/**
 * Entity being changed.
 */
export enum Entity {
  PROJECT = "PROJECT",
  MEMBERS = "MEMBERS",
  VERSION = "VERSION",
  TYPES = "TYPES",
  DOCUMENT = "DOCUMENT",
  ARTIFACTS = "ARTIFACTS",
  TRACES = "TRACES",
  WARNINGS = "WARNINGS",
  JOBS = "JOBS",
}

/**
 * The action performed on an change to an entity.
 * Used in notifications to signal asyncronous updates.
 */
export enum Action {
  UPDATE = "UPDATE",
  DELETE = "DELETE",
}

import { Artifact, TraceLink } from "@/types";

/**
 * Enumerates the type of notification messages that signal
 * that a project meta entity should be updated.
 */
export enum ProjectMessage {
  MEMBERS = "MEMBERS",
  DOCUMENTS = "DOCUMENTS",
  META = "META",
}

/**
 * Enumerates the types of notifications messages that trigger
 * updates of the versioned entities
 */
export enum VersionMessage {
  VERSION = "VERSION",
  ARTIFACTS = "ARTIFACTS",
  TRACES = "TRACES",
}
/**
 * Defines an update to traces and artifacts within a project version.
 */
export interface ProjectVersionUpdate {
  /**
   * Whether the data modified is included in the Update.
   */
  type: "VERSION" | "MEMBERS" | "DOCUMENTS" | "ARTIFACTS";
  /**
   * The traces updated.
   */
  traces: TraceLink[];
  /**
   * The artifacts updated.
   */
  artifacts: Artifact[];
}

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

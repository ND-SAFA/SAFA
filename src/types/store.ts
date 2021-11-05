import {
  AddedArtifact,
  ModifiedArtifact,
  RemovedArtifact,
  Artifact,
} from "@/types";

/**
 * Enumerates app store message types.
 */
export enum MessageType {
  INFO = "info",
  SUCCESS = "success",
  ERROR = "error",
  WARNING = "warning",
}

/**
 * Defines a snackbar message.
 */
export interface SnackbarMessage {
  /**
   * A list of errors.
   */
  errors: string[];
  /**
   * The message text.
   */
  message: string;
  /**
   * The message type.
   */
  type: MessageType;
}

/**
 * Enumerates types of panels.
 */
export enum PanelType {
  left,
  right,
  artifactCreator,
  errorDisplay,
}

/**
 * Defines the state of a panel.
 */
export interface PanelState {
  /**
   * The type of panel.
   */
  type: PanelType;
  /**
   * Whether the panel is open.
   */
  isOpen: boolean;
}

/**
 * Defines the delta artifacts state.
 */
export interface DeltaArtifacts {
  /**
   * A collection of all added artifacts.
   */
  added: Record<string, AddedArtifact>;
  /**
   * A collection of all removed artifacts.
   */
  removed: Record<string, RemovedArtifact>;
  /**
   * A collection of all modified artifacts.
   */
  modified: Record<string, ModifiedArtifact>;
}

/**
 * Defines the delta payload state.
 */
export interface DeltaPayload extends DeltaArtifacts {
  /**
   * A list of all missing artifacts.
   */
  missingArtifacts: Artifact[];
}

/**
 * Defines a channel subscription.
 */
export interface ChannelSubscriptionId {
  /**
   * The project's id.
   */
  projectId?: string;
  /**
   * The version's id.
   */
  versionId?: string;
}

/**
 * Returns an artifact matching the given query, if one exists.
 */
export type ArtifactQueryFunction = (q: string) => Artifact | undefined;

/**
 * Returns whether a link exists from the given source to the given target ID.
 */
export type LinkValidator = (sourceId: string, targetId: string) => boolean;

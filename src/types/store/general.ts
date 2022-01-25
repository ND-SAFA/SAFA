/**
 * Enumerates the allowed trace link directions between artifact types.
 */
export type ArtifactTypeDirections = Record<string, string[]>;

/**
 * Enumerates the icons for each artifact type.
 */
export type ArtifactTypeIcons = Record<string, string>;

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
 * Returns whether a link exists from the given source to the given target ID.
 */
export type LinkValidator = (sourceId: string, targetId: string) => boolean;

/**
 * Defines a title and message for a confirmation dialog.
 */
export interface ConfirmDialogueMessage {
  type: ConfirmationType;
  title: string;
  body: string;
  statusCallback: (status: boolean) => void;
}

export enum ConfirmationType {
  INFO = "info",
  CLEAR = "clear",
}

/**
 * General type for representing an empty callback
 */
export type EmptyLambda = () => void;

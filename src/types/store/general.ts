import {
  ArtifactModel,
  ArtifactData,
  DocumentType,
  FTANodeType,
  SafetyCaseType,
  TraceLinkModel,
} from "@/types";

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
  artifactBody,
  traceLinkCreator,
}

export type PanelOpenState =
  | boolean
  | SafetyCaseType
  | FTANodeType
  | DocumentType;

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
  isOpen: PanelOpenState;
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
 * Returns true if a link can be created, otherwise an error.
 */
export type CreateLinkValidator = (
  source: ArtifactModel | ArtifactData,
  target: ArtifactModel | ArtifactData
) => boolean | string;

/**
 * Returns the trace link between the given artifact ids.
 */
export type LinkFinder = (sourceId: string, targetId: string) => TraceLinkModel;

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

/**
 * Enumerates keys used in local storage.
 */
export enum LocalStorageKeys {
  JIRA_REFRESH_TOKEN = "jrt",
  JIRA_CLOUD_ID = "jci",
  GIT_HUB_REFRESH_TOKEN = "grt",
  GIT_HUB_INSTALLATION_ID = "gid",
}

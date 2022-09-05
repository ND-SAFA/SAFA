import { DocumentType, FTANodeType, SafetyCaseType } from "@/types";

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
  traceLinkDraw,
  traceLinkGenerator,
}

/**
 * Represents the open state of the artifact creator.
 */
export type PanelOpenState =
  | boolean
  | SafetyCaseType
  | FTANodeType
  | DocumentType;

/**
 * Represents the states of all openable panels.
 */
export interface PanelStateMap {
  [PanelType.left]: boolean;
  [PanelType.right]: boolean;
  [PanelType.artifactCreator]: PanelOpenState;
  [PanelType.errorDisplay]: boolean;
  [PanelType.artifactBody]: boolean;
  [PanelType.traceLinkCreator]: boolean;
  [PanelType.traceLinkDraw]: boolean;
  [PanelType.traceLinkGenerator]: boolean;
}

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
  SESSION_TOKEN = "t",
  JIRA_REFRESH_TOKEN = "jrt",
  JIRA_CLOUD_ID = "jci",
  GIT_HUB_REFRESH_TOKEN = "grt",
  GIT_HUB_INSTALLATION_ID = "gid",
}

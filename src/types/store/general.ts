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
  appPanel = "appPanel",
  detailsPanel = "detailsPanel",
  artifactCreator = "artifactCreator",
  errorDisplay = "errorDisplay",
  traceLinkDraw = "traceLinkDraw",
}

/**
 * Represents the open state of the artifact creator.
 */
export type CreatorOpenState =
  | boolean
  | SafetyCaseType
  | FTANodeType
  | DocumentType;

/**
 * Represents the type of details panel states.
 */
export type DetailsOpenState =
  | boolean
  | "delta"
  | "document"
  | "displayArtifact"
  | "displayArtifactBody"
  | "saveArtifact"
  | "displayTrace"
  | "saveTrace";

/**
 * Represents the states of all openable panels.
 */
export interface PanelStateMap {
  [PanelType.appPanel]: boolean;
  [PanelType.detailsPanel]: DetailsOpenState;
  [PanelType.artifactCreator]: CreatorOpenState;
  [PanelType.errorDisplay]: boolean;
  [PanelType.traceLinkDraw]: boolean;
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

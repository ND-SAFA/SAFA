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
  errorDisplay = "errorDisplay",
  detailsPanel = "detailsPanel",
  artifactCreator = "artifactCreator",
  traceCreator = "traceCreator",
  traceLinkDraw = "traceLinkDraw",
}

/**
 * Represents the open state of the artifact creator.
 */
export type ArtifactCreatorOpenState =
  | boolean
  | SafetyCaseType
  | FTANodeType
  | DocumentType;

/**
 * Represents the open state of the trace link creator.
 */
export type TraceCreatorOpenState =
  | boolean
  | { type: "source"; artifactId: string }
  | { type: "target"; artifactId: string };

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
  | "saveTrace"
  | "generateTrace"
  | "displayArtifactLevel"
  | "displayTraceMatrix";

/**
 * Represents the states of all openable panels.
 */
export interface PanelStateMap {
  [PanelType.appPanel]: boolean;
  [PanelType.detailsPanel]: DetailsOpenState;
  [PanelType.artifactCreator]: ArtifactCreatorOpenState;
  [PanelType.traceCreator]: TraceCreatorOpenState;
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

export enum LocalStorageKeys {
  darkMode = "dark",
}

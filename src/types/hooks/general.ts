import { DocumentType, FTANodeType, SafetyCaseType } from "@/types";

/**
 * Enumerates types of panels.
 */
export enum PanelType {
  appPanel = "appPanel",
  errorDisplay = "errorDisplay",
  detailsPanel = "detailsPanel",
  projectSaver = "projectSaver",
  projectDeleter = "projectDeleter",
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
  | { type: "target"; artifactId: string }
  | { type: "both"; sourceId: string; targetId: string };

/**
 * Represents the type of details panel states.
 */
export type DetailsOpenState =
  | boolean
  | "delta"
  | "document"
  | "displayArtifact"
  | "displayArtifactBody"
  | "generateArtifact"
  | "saveArtifact"
  | "displayTrace"
  | "saveTrace"
  | "generateTrace"
  | "displayArtifactLevel"
  | "saveArtifactLevel"
  | "displayTraceMatrix";

/**
 * Represents the states of all openable panels.
 */
export interface PanelStateMap {
  [PanelType.appPanel]: boolean;
  [PanelType.detailsPanel]: DetailsOpenState;
  [PanelType.projectSaver]: boolean;
  [PanelType.projectDeleter]: boolean;
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

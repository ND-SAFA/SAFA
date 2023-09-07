import { DocumentType, FTANodeType, SafetyCaseType } from "@/types";

export type PopupType =
  | "errorModal"
  | "navPanel"
  | "detailsPanel"
  | "saveOrg"
  | "saveTeam"
  | "saveProject"
  | "editProject"
  | "deleteProject"
  | "saveArtifact"
  | "saveTrace"
  | "drawTrace";

/**
 * Represents the states of all popups.
 */
export interface PopupStateMap
  extends Record<
    PopupType,
    | boolean
    | DetailsOpenState
    | ArtifactCreatorOpenState
    | TraceCreatorOpenState
  > {
  errorModal: boolean;
  navPanel: boolean;
  detailsPanel: DetailsOpenState;
  saveOrg: boolean;
  saveTeam: boolean;
  saveProject: boolean;
  editProject: boolean;
  deleteProject: boolean;
  saveArtifact: ArtifactCreatorOpenState;
  saveTrace: TraceCreatorOpenState;
  drawTrace: boolean;
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

import { ArtifactSchema } from "@/types";

export type PopupType =
  | "errorModal"
  | "navPanel"
  | "detailsPanel"
  | "saveOrg"
  | "saveTeam"
  | "saveProject"
  | "editProject"
  | "moveProject"
  | "deleteProject"
  | "saveArtifact"
  | "saveTrace"
  | "drawTrace";

/**
 * Represents the states of all popups.
 */
export interface PopupStateMap
  extends Record<PopupType, boolean | DetailsOpenState> {
  errorModal: boolean;
  navPanel: boolean;
  detailsPanel: DetailsOpenState;
  saveOrg: boolean;
  saveTeam: boolean;
  saveProject: boolean;
  editProject: boolean;
  moveProject: boolean;
  deleteProject: boolean;
  saveArtifact: boolean;
  saveTrace: boolean;
  drawTrace: boolean;
}

/**
 * Represents the open state of the trace link creator.
 */
export type TraceCreatorOpenState =
  | boolean
  | { type: "source"; artifactId: string }
  | { type: "target"; artifactId: string }
  | { type: "both"; sourceIds: string[]; targetIds: string[] };

/**
 * Represents the open state of the artifact creator.
 */
export interface ArtifactCreatorOpenState {
  /**
   * Whether this is a new artifact, or one being edited.
   */
  isNewArtifact?: boolean;
  /**
   * Additional fields to include in the artifact being saved.
   */
  artifact?: Partial<ArtifactSchema>;
  /**
   * A parent artifact to optionally link to.
   */
  parentId?: string;
}

/**
 * Represents the type of details panel states.
 */
export type DetailsOpenState =
  | boolean
  | "delta"
  | "document"
  | "displayProject"
  | "displayArtifact"
  | "displayArtifactBody"
  | "generateArtifact"
  | "summarizeArtifact"
  | "saveArtifact"
  | "displayTrace"
  | "saveTrace"
  | "editTrace"
  | "generateTrace"
  | "displayArtifactLevel"
  | "saveArtifactLevel"
  | "displayTraceMatrix"
  | "health";

/**
 * Defines a title and message for a confirmation dialog.
 */
export interface ConfirmDialogueMessage {
  type: "info" | "clear";
  title: string;
  body: string;
  statusCallback: (status: boolean) => void;
}

/**
 * General type for representing an empty callback
 */
export type EmptyLambda = () => void;

export enum LocalStorageKeys {
  darkMode = "dark",
}

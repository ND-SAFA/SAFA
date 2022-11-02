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
export type CreatorOpenState =
  | boolean
  | SafetyCaseType
  | FTANodeType
  | DocumentType;

/**
 * Represents the open state of the trace link generator.
 */
export type GeneratorOpenState = boolean | "generate" | "train";

/**
 * Represents the states of all openable panels.
 */
export interface PanelStateMap {
  [PanelType.left]: boolean;
  [PanelType.right]: boolean;
  [PanelType.artifactCreator]: CreatorOpenState;
  [PanelType.errorDisplay]: boolean;
  [PanelType.artifactBody]: boolean;
  [PanelType.traceLinkCreator]: boolean;
  [PanelType.traceLinkDraw]: boolean;
  [PanelType.traceLinkGenerator]: GeneratorOpenState;
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

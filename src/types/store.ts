import {
  AddedArtifact,
  ModifiedArtifact,
  RemovedArtifact,
} from "@/types/domain/delta";
import { Artifact } from "@/types/domain/artifact";

/**
 *APP STATE
 */
export enum MessageType {
  INFO,
  SUCCESS,
  ERROR,
  WARNING,
}
export interface SnackbarMessage {
  message: string;
  type: MessageType;
}

export enum PanelType {
  left,
  right,
  artifactCreator,
}

export interface PanelState {
  type: PanelType;
  isOpen: boolean;
}

/**
 * DELTA STATE
 */
export interface DeltaPayload {
  added: Record<string, AddedArtifact>;
  removed: Record<string, RemovedArtifact>;
  modified: Record<string, ModifiedArtifact>;
  missingArtifacts: Artifact[];
}

export interface DeltaArtifacts {
  added: Record<string, AddedArtifact>;
  removed: Record<string, RemovedArtifact>;
  modified: Record<string, ModifiedArtifact>;
}

import { LayoutPositionsSchema } from "@/types";
import { IdentifierSchema } from "@/types/domain/project";

/**
 * Enumerates the type of project subset views supported by SAFA.
 */
export type ViewType =
  | "ARTIFACT_TREE"
  | "FTA"
  | "SAFETY_CASE"
  | "FMEA"
  | "FMECA";

/**
 * Defines a specific view of a subset of project data.
 */
export interface ViewSchema {
  /**
   * The id of this view.
   */
  documentId: string;
  /**
   * The project associated with this view.
   */
  project: IdentifierSchema;
  /**
   * The name of the view.
   */
  name: string;
  /**
   * The description of the view.
   */
  description: string;
  /**
   * The type of view.
   */
  type: ViewType;
  /**
   * The ids of artifacts displayed within this view.
   */
  artifactIds: string[];
  /**
   * Map of artifact ids to their artifact positions.
   */
  layout: LayoutPositionsSchema;
}

import { ArtifactSchema, MatrixSchema, TraceProps } from "@/types";

/**
 * Enumerates the different methods of filtering artifacts by number of traces.
 */
export type TraceCountTypes = "all" | "onlyTraced" | "notTraced";

/**
 * The props for displaying a trace link.
 */
export interface TraceLinkDisplayProps extends TraceProps {
  /**
   * Whether to display only the source or target artifact.
   */
  showOnly?: "source" | "target";
}

/**
 * The props for displaying trace link approval buttons.
 */
export interface TraceLinkApprovalProps extends TraceProps {
  /**
   * Whether this trace link can be deleted.
   */
  deletable?: boolean;
}

/**
 * The props for displaying a trace matrix creator.
 */
export interface TraceMatrixCreatorProps {
  /**
   * The trace matrices to edit.
   */
  modelValue: MatrixSchema[];
}

/**
 * The props for displaying a trace matrix chip.
 */
export interface TraceMatrixChipProps {
  /**
   * The source artifact.
   */
  source: ArtifactSchema;
  /**
   * The target artifact.
   */
  target: ArtifactSchema;
}

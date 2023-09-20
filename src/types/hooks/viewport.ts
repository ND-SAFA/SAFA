import { CyPromise, CyLayout } from "@/types";

/**
 * Represents a payload for a cytoscape layout operation.
 */
export interface CyLayoutPayload {
  /**
   * The cytoscape instance.
   */
  cyPromise: CyPromise;
  /**
   * The layout options.
   */
  layout: CyLayout;
  /**
   * Whether to generate the layout.
   */
  generate?: boolean;
}

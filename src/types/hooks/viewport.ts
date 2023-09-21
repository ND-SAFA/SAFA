import { LayoutOptions } from "cytoscape";
import { CyPromise } from "@/types";

/**
 * Represents a payload for a cytoscape layout operation.
 */
export interface CyLayoutPayload {
  /**
   * The cytoscape instance.
   */
  cyPromise: CyPromise;
  /**
   The layout options.
   */
  options: LayoutOptions;
  /**
   * Whether to generate the layout.
   */
  generate?: boolean;
}

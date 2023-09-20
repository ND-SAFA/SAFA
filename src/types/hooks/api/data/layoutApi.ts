import { IOHandlerCallback } from "@/types";

/**
 * A hook for calling graph layout API endpoints.
 */
export interface LayoutApiHook {
  /**
   * Handles regenerating and storing the layout for the current project version and document.
   *
   * @param callbacks - Callbacks to handle the result of the operation.
   */
  handleRegenerate(callbacks?: IOHandlerCallback): Promise<void>;
}

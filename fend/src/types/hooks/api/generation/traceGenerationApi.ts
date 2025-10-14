import { ComputedRef } from "vue";
import { IOHandlerCallback, MatrixSchema } from "@/types";

/**
 * A hook for calling trace generation API endpoints.
 */
export interface TraceGenerationApiHook {
  /**
   * Whether the trace generation request is loading.
   */
  loading: ComputedRef<boolean>;
  /**
   * Updates the storage of generated links.
   *
   * @param callbacks - The callbacks to use for the action.
   */
  handleReload(callbacks?: IOHandlerCallback): Promise<void>;
  /**
   * Generates links between sets of artifact types and adds them to the project.
   *
   * @param matrices - An array of source and target artifact types to generate traces between.
   * @param callbacks - The callbacks to use for the action.
   */
  handleGenerate(
    matrices: MatrixSchema[],
    callbacks: IOHandlerCallback
  ): Promise<void>;
}

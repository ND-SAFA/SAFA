import { ComputedRef } from "vue";
import {
  GenerationModelSchema,
  IOHandlerCallback,
  MatrixSchema,
  ModelType,
} from "@/types";

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
   * @param method - The base model to generate with.
   * @param matrices - An array of source and target artifact types to generate traces between.
   * @param callbacks - The callbacks to use for the action.
   */
  handleGenerate(
    method: ModelType | undefined,
    matrices: MatrixSchema[],
    callbacks: IOHandlerCallback
  ): Promise<void>;
  /**
   * Trains models on created trace links.
   *
   * @param model - The model to train.
   * @param matrices - An array of source and target artifact types to train on traces between.
   * @param callbacks - The callbacks to use for the action.
   */
  handleTrain(
    model: GenerationModelSchema,
    matrices: MatrixSchema[],
    callbacks: IOHandlerCallback
  ): Promise<void>;
}

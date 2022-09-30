import { ModelType } from "@/types";

export interface TrainedModel {
  /**
   * The model's id.
   */
  id: string;
  /**
   * The model's name.
   */
  name: string;
  /**
   * The base model that is being extended.
   */
  baseModel: ModelType;
  /**
   * NOT YET IMPLEMENTED.
   * The trace directions that this model has been trained on.
   */
  defaultTraceDirections?: { source: string; target: string }[];
}

/**
 * Lists the methods by which a model can be shared.
 */
export enum ModelShareType {
  CLONE = "COPY_BY_VALUE",
  REUSE = "COPY_BY_REFERENCE",
}

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

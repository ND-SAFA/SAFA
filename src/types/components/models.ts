import { GenerationModelSchema, TrainingStepSchema } from "@/types";

/**
 * Enumerates the different tabs for the model editor.
 */
export enum TracePredictionTabTypes {
  models = "models",
  generation = "generation",
  approval = "approval",
}

/**
 * Defines a generated summary and callback to save it.
 */
export interface ArtifactSummaryConfirmation {
  /**
   * The generated summary to save.
   */
  summary: string;
  /**
   * A callback to save the summary.
   */
  confirm: () => void;
  /**
   * A callback to clear the summary & confirmation.
   */
  clear: () => void;
}

/**
 * The props for displaying a generation model.
 */
export interface GenerationModelProps {
  /**
   * The model to display.
   */
  model: GenerationModelSchema;
  /**
   * Whether this model is generated.
   */
  generated?: boolean;
}

/**
 * The props for displaying a model training step.
 */
export interface ModelTrainingStepProps {
  /**
   * The step to display.
   */
  step: TrainingStepSchema;
}

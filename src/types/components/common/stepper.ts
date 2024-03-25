import { LoadingProps, MinimalProps } from "@/types";

/**
 * Defines a step used by the stepper component.
 */
export interface StepperStep {
  /**
   * The step title.
   */
  title: string;
  /**
   * Whether the step is done.
   */
  done: boolean;
  /**
   * An optional step caption.
   */
  caption?: string;
}

/**
 * Defines props for the stepper component.
 */
export interface StepperProps extends MinimalProps, LoadingProps {
  /**
   * The current 1-based step number.
   */
  modelValue: number;
  /**
   * The steps to render.
   * A slot will be created for each step, named by their 1-based index.
   */
  steps: StepperStep[];
  /**
   * If true, the label text will be made as dense as possible.
   * Useful when displaying long lists of steps
   */
  denseLabels?: boolean;
  /**
   * If true, the actions will be hidden.
   */
  hideActions?: boolean;
  /**
   * If true, the ability to click a previous step to go back will be hidden.
   */
  hideStepBack?: boolean;
  /**
   * The color to display the completed steps using.
   */
  color?: "gradient" | "primary";
}

/**
 * Defines props for the stepper step that displays a list of items.
 */
export interface StepperListStepProps extends LoadingProps {
  /**
   * The step title.
   */
  title: string;
  /**
   * The number of items in this step.
   */
  itemCount: number;
  /**
   * The message to display when empty.
   */
  emptyMessage?: string;
}

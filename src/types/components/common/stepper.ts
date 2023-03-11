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

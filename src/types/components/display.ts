/**
 * Defines the possible modal sizes.
 */
export type ModalSize = "xxs" | "xs" | "s" | "m" | "l";

/**
 * Defines the name of a step and whether the step is currently valid.
 */
export type StepState = [string, boolean];

/**
 * Defines a toggleable item of data.
 */
export interface DataItem<T> {
  /**
   * Whether this item is enabled.
   */
  value: boolean;
  /**
   * The item of data.
   */
  item: T;
}

/**
 * Displays a generic list item.
 */
export interface ListItem {
  /**
   * The title to display.
   */
  title: string;
  /**
   * The subtitle to display.
   */
  subtitle?: string;
}

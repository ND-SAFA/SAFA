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

/**
 * The variants of text that can be displayed.
 */
export type TextType =
  | "large"
  | "title"
  | "subtitle"
  | "body"
  | "small"
  | "caption"
  | "expandable"
  | "code";

/**
 * The types of text elements.
 */
export type ElementType = "span" | "p" | "div" | "h1" | "h2" | "h3";

/**
 * The methods of text alignment.
 */
export type TextAlignType = "left" | "center" | "right";

/**
 * The methods of alignment.
 */
export type AlignType = "start" | "center" | "end";

/**
 * The methods of justifying.
 */
export type JustifyType = AlignType | "space-between" | "space-around";

/**
 * The possible increments for spacing.
 */
export type SizeType =
  | ""
  | "1"
  | "2"
  | "3"
  | "4"
  | "5"
  | "6"
  | "7"
  | "8"
  | "9"
  | "10";

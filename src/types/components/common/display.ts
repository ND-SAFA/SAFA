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
export type JustifyType = AlignType | "between" | "around";

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
  | "10"
  | "11"
  | "12";

/**
 * Package: 'vue3-drr-grid-layout'
 * Defines component props.
 */
export interface GridItemData {
  x: number;
  y: number;
  w: number;
  h: number;
  i: string;
}

/**
 * Represents an option for a select menu.
 */
export interface SelectOption {
  /**
   * The iud of the option to use as a stored.
   */
  id: string;
  /**
   * The name of the option to display.
   */
  name: string;
}

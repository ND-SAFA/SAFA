import { ClassNameProps, ColorProps, MarginProps, SizeProps } from "@/types";

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
  | "markdown"
  | "code";

/**
 * The types of text elements.
 */
export type ElementType = "span" | "p" | "div" | "h1" | "h2" | "h3" | "a";

/**
 * The methods of text alignment.
 */
export type TextAlignType = "left" | "center" | "right";

/**
 * Defines props for displaying text.
 */
export interface TypographyProps
  extends ColorProps,
    SizeProps,
    MarginProps,
    ClassNameProps {
  /**
   * The text value to display.
   */
  value?: string | number;
  /**
   * Whether to truncate text with an ellipsis.
   */
  ellipsis?: boolean;

  /**
   * Whether to inherit color from the parent element.
   */
  inheritColor?: boolean;
  /**
   * Whether to color this text as an error.
   */
  error?: boolean;
  /**
   * Renders the text with a faded color.
   */
  secondary?: boolean;

  /**
   * Bolds the text.
   */
  bold?: boolean;
  /**
   * Sets the text to wrap.
   */
  wrap?: boolean;
  /**
   * On expandable text, whether the text can be copied.
   */
  copyable?: boolean;

  /**
   * The variant of text to render.
   * @default `body`
   */
  variant?: TextType;
  /**
   * The element to render the text on.
   * @default `span`
   */
  el?: ElementType;
  /**
   * How to align the text.
   * @default `left`
   */
  align?: TextAlignType;

  /**
   * For expandable variants, whether the content defaults to expanded.
   */
  defaultExpanded?: boolean;
  /**
   * The length at which to automatically collapse a default expanded component.
   * If set to 0, the component will never collapse by default.
   */
  collapseLength?: number;
  /**
   * If displaying code, the extension to use.
   * Supported md code types for prism can be found here:
   * - https://github.com/jincheng9/markdown_supported_languages?ref=itsfoss.com
   * - https://prismjs.com/#supported-languages
   */
  codeExt?: string;
}

/**
 * Defines props for a component that renders a separator.
 */
export interface SeparatorProps
  extends MarginProps,
    ClassNameProps,
    ColorProps {
  /**
   * Whether to render the separator vertically.
   */
  vertical?: boolean;
  /**
   * Whether to pad the separator.
   */
  inset?: boolean;
  /**
   * Whether to style to separator for the navigation bar.
   */
  nav?: boolean;
}

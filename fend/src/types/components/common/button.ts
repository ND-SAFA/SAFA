import {
  ClassNameProps,
  ColorProps,
  DisabledProps,
  IconProps,
  LoadingProps,
  MarginProps,
  OutlinedProps,
  SizeProps,
  TestableProps,
} from "@/types";
import { Routes } from "@/router";

/**
 * The props for the back button.
 */
export interface BackButtonProps {
  /**
   * The label to render on the button.
   * @default "Back To Project" | "Go Back"
   */
  label?: string;
  /**
   * The route to navigate to.
   * @default Go back in router history.
   */
  route?: Routes;
  /**
   * If true, the back button will always return to the project page.
   */
  toProject?: boolean;
}

/**
 * The props for the icon button component.
 */
export interface IconButtonProps
  extends IconProps,
    DisabledProps,
    ColorProps,
    SizeProps,
    TestableProps {
  /**
   * The tooltip message to display on this button.
   */
  tooltip: string;
  /**
   * The ms to wait before displaying the tooltip.
   * @default 200
   */
  tooltipDelay?: number;
  /**
   * The icon id to render on this button.
   */
  iconId?: string;
  /**
   * Whether to render this button as a fab.
   */
  fab?: boolean;
  /**
   * Rotates the icon on this button (in degrees).
   */
  rotate?: number;
}

/**
 * The props for the text button component.
 */
export interface TextButtonProps
  extends IconProps,
    DisabledProps,
    ColorProps,
    LoadingProps,
    MarginProps,
    ClassNameProps,
    SizeProps,
    OutlinedProps,
    TestableProps {
  /**
   * Renders a flat text button.
   */
  text?: boolean;
  /**
   * Renders the button as a full width block.
   */
  block?: boolean;
  /**
   * The loading percentage to render on a loading button.
   */
  percentage?: number;
  /**
   * The button text to display, if not using the default slot.
   */
  label?: string;
  /**
   * If true, the button label will be hidden.
   */
  hideLabel?: boolean;
  /**
   * The icon rotation degrees.
   */
  iconRotate?: number;
}

/**
 * The props for the artifact type button group component.
 */
export interface TypeButtonProps {
  /**
   * Whether the buttons are visible by default.
   * @default false
   */
  defaultVisible?: boolean;
  /**
   * Which type buttons are not active.
   * Defaults to all buttons being active.
   */
  hiddenTypes: string[];
}

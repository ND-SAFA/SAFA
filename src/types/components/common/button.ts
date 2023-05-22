import {
  ClassNameProps,
  ColorProps,
  DisabledProps,
  IconProps,
  LoadingProps,
  MarginProps,
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
    TestableProps {
  /**
   * Renders an outlined button.
   */
  outlined?: boolean;
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
}

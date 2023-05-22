import { ColorProps, IconVariant, StyleProps, TestableProps } from "@/types";

/**
 * Defines props for an icon.
 */
export interface IconDisplayProps
  extends ColorProps,
    StyleProps,
    TestableProps {
  /**
   * The icon variant to render.
   */
  variant?: IconVariant;
  /**
   * The id of an icon, if not rendering a preset variant.
   */
  id?: string;
  /**
   * The size of the icon.
   */
  size?: "sm" | "md" | "lg";
  /**
   * How much to rotate the icon (in degrees).
   */
  rotate?: number;
}

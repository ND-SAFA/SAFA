import {
  ClassNameProps,
  ClickableProps,
  ColorProps,
  IconProps,
  OutlinedProps,
  RemovableProps,
  StyleProps,
  TestableProps,
} from "@/types";

/**
 * Defines props for a chip component.
 */
export interface ChipProps
  extends ClassNameProps,
    ColorProps,
    StyleProps,
    OutlinedProps,
    ClickableProps,
    RemovableProps,
    TestableProps {
  /**
   * A chip label to display.
   */
  label?: string;
  /**
   * If true, the chip is displayed more compactly.
   */
  dense?: boolean;
}

/**
 * Defines props for an attribute chip component.
 */
export interface AttributeChipProps
  extends ColorProps,
    IconProps,
    RemovableProps,
    TestableProps {
  /**
   * The chip text.
   */
  value: string | number;
  /**
   * If true, the chip text will be converted from "camelCase" to "Display Case".
   */
  format?: boolean;
  /**
   * Whether this chip is for an artifact type, customizing the display and icon.
   */
  artifactType?: boolean;
  /**
   * Whether this chip is for a delta type, customizing the display and icon.
   */
  deltaType?: boolean;
  /**
   * Whether this chip is for an approval type, customizing the display and icon.
   */
  approvalType?: boolean;
  /**
   * Whether to render a confidence score instead of a chip.
   */
  confidenceScore?: boolean;
  /**
   * If true, the chip is displayed more compactly.
   */
  dense?: boolean;
}

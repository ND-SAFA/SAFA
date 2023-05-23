import { AlignType, JustifyType, MarginProps, SizeType } from "@/types";

/**
 * Defines props for a flex container.
 */
export interface FlexBoxProps extends MarginProps {
  /**
   * How to align the content.
   */
  align?: AlignType;
  /**
   * How to justify the content.
   */
  justify?: JustifyType;
  /**
   * The max width to set (in pixels)
   */
  maxWidth?: number;
  /**
   * Whether to expand to full width.
   */
  fullWidth?: boolean;
  /**
   * Whether to render as a flex column instead of row.
   */
  column?: boolean;
  /**
   * Whether to allow the items to wrap.
   * @default Unset unless an explicit boolean true or false is set.
   */
  wrap?: boolean;
}

/**
 * Defines props for a flex container item.
 */
export interface FlexItemProps extends MarginProps {
  /**
   * How many parts this column should take up, out of 12.
   */
  parts?: SizeType | "auto";
  /**
   * Whether to expand to full width.
   */
  fullWidth?: boolean;
}

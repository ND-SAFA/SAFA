import { AttributeLayoutSchema, AttributeSchema } from "@/types";

/**
 * The props for displaying an attribute layout.
 */
export interface AttributeLayoutProps {
  /**
   * The attribute layout to display or edit.
   */
  layout?: AttributeLayoutSchema;
}

/**
 * The props for displaying an artifact attribute.
 */
export interface AttributeProps {
  /**
   * The attribute to display or edit.
   */
  attribute?: AttributeSchema;
}

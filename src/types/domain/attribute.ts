/**
 * Defines a custom attribute being tracked for a project.
 */
export interface AttributeModel {
  /**
   * The key to this attribute within an artifact's `customFields` object.
   */
  key: string;
  /**
   * The label for this attribute
   */
  label: string;
  /**
   * The type of data represented by this attribute.
   */
  type:
    | "string"
    | "select"
    | "multiselect"
    | "date"
    | "int"
    | "float"
    | "boolean";
  /**
   * Any pre-set options for this custom field to choose from.
   */
  options?: string[];
  /**
   * The min-value for a number field.
   */
  min?: number;
  /**
   * The max-value for a number field.
   */
  max?: number;
}

/**
 * A list of the attributes to lay out and their positions.
 */
export interface AttributePositionModel {
  /**
   * The attribute key for this item.
   */
  key: string;
  /**
   * The x position in the layout.
   */
  x: number;
  /**
   * The y position in the layout.
   */
  y: number;
  /**
   * The height in the layout.
   */
  height: number;
  /**
   * The width in the layout.
   */
  width: number;
}

/**
 * Defines a layout of custom attributes for some set of artifact types.
 */
export interface AttributeLayoutModel {
  /**
   * The list of artifact types to display this attribute layout on.
   * If empty, this attribute will be displayed for all.
   */
  artifactTypes: string[];
  /**
   * A list of the attributes to lay out and their positions.
   */
  positions: AttributePositionModel[];
}

/**
 * Defines all attributes on a project.
 */
export interface ProjectAttributesModel {
  /**
   * A list of custom artifact attributes.
   */
  items: AttributeModel[];
  /**
   * A list of custom attribute layouts.
   * This list should always contain at least one item with empty artifact types,
   * used as the default layout.
   */
  layouts: AttributeLayoutModel[];
}

/**
 * Represents a collection of custom attributes, keyed by their `key` value.
 */
export type CustomAttributeCollection = Record<
  string,
  string | string[] | number | boolean | undefined
>;

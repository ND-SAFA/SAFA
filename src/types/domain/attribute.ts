/**
 * Enumerates the type of attribute properties.
 */
export type AttributeType =
  | "text" // String
  | "paragraph" // String
  | "select" // String
  | "multiselect" // String Array
  | "relation" // String Array
  | "date" // ISO Date String
  | "int" // Integer
  | "float" // Float
  | "boolean"; // Boolean

/**
 * Defines a custom attribute being tracked for a project.
 */
export interface AttributeSchema {
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
  type: AttributeType;
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
export interface AttributePositionSchema {
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
export interface AttributeLayoutSchema {
  /**
   * The ID of this attribute layout.
   */
  id: string;
  /**
   * The name of this attribute layout.
   */
  name: string;
  /**
   * The list of artifact types to display this attribute layout on.
   * If empty, this attribute will be displayed for all.
   */
  artifactTypes: string[];
  /**
   * A list of the attributes to lay out and their positions.
   */
  positions: AttributePositionSchema[];
}

/**
 * Represents all possible data types of an attribute.
 */
export type AttributeDataType =
  | string
  | string[]
  | number
  | boolean
  | null
  | undefined;

/**
 * Represents a collection of custom attributes, keyed by their `key` value.
 */
export type AttributeCollectionSchema = Record<string, AttributeDataType>;

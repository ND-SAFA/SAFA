/**
 * Defines a custom attribute being tracked for a project.
 */
export interface CustomAttributeModel {
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
  type: "string" | "number" | "select" | "multiselect";
  /**
   * The list of artifact types to display this attribute on.
   * If empty, this attribute will be displayed for all.
   */
  artifactTypes: string[];
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

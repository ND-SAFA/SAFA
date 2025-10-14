import {
  ArtifactSchema,
  AttributeCollectionSchema,
  AttributeLayoutSchema,
  AttributeSchema,
} from "@/types";

/**
 * The props for displaying an attribute.
 */
export interface AttributeDisplayProps {
  /**
   * The collection of attribute values to display from.
   */
  values: AttributeCollectionSchema;
  /**
   * The attribute from the collection to display.
   */
  attribute: AttributeSchema;
  /**
   * If true, the attribute name will be displayed above the value.
   */
  showName?: boolean;
}

/**
 * The props for displaying an attribute grid.
 */
export interface AttributeGridProps {
  /**
   * The layout of attributes to display.
   */
  layout: AttributeLayoutSchema;
  /**
   * Whether the attribute grid is editable.
   */
  editable?: boolean;
}

/**
 * The props for displaying an attribute list.
 */
export interface AttributeListProps {
  /**
   * The artifact to display the custom attributes of.
   */
  artifact: ArtifactSchema;
}

/**
 * Package: 'vue3-drr-grid-layout'
 * Defines component props.
 */
export interface GridItemData {
  x: number;
  y: number;
  w: number;
  h: number;
  i: string;
}

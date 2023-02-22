/**
 * A column within a data table.
 */
export interface TableColumn<T = Record<string, unknown>> {
  /**
   * The column field id.
   */
  name: keyof T | string;
  /**
   * The column display name.
   */
  label: string;
  /**
   * A function for returning the field id from a row item.
   */
  field(row: T): unknown;
  /**
   * Whether this column is required and cannot be hidden.
   */
  required?: boolean;
  /**
   * Whether this column is sortable.
   */
  sortable?: boolean;
}

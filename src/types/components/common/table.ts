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
  /**
   * How to align the text content.
   */
  align?: "left" | "center";
  /**
   * A function for formatting the cell text.
   */
  format?(value: unknown): string;
  /**
   * A function for comparing two rows when sorting by this column.
   */
  sort?(a: unknown, b: unknown): number;
}

/**
 * A generic row of a table.
 */
export type TableRow = Record<string, unknown>;

/**
 * A generic row of a table, or a group header.
 */
export type TableGroupRow =
  | TableRow
  | {
      /**
       * The field name that is being grouped by.
       */
      $groupBy: string;
      /**
       * The field value that all rows share for this group.
       */
      $groupValue: string;
      /**
       * The number of rows in this group.
       */
      $groupRows: number;
    };

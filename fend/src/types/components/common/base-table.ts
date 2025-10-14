/**
 * A column within a data table.
 */
export interface TableColumn<Row = Record<string, unknown>> {
  /**
   * The column field id.
   */
  name: keyof Row | string;
  /**
   * The column display name.
   */
  label: string;
  /**
   * A function for returning the field id from a row item.
   */
  field(row: Row): unknown;
  /**
   * Whether this column is required and cannot be hidden.
   */
  required?: boolean;
  /**
   * Whether this column is sortable.
   */
  sortable?: boolean;
  /**
   * Whether this column is groupable.
   */
  groupable?: boolean;
  /**
   * How to align the text content.
   */
  align?: "left" | "center" | "right";
  /**
   * Any classes to apply.
   */
  classes?: string;
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
      /**
       * The sort index of this row.
       */
      $sortIdx: number;
    };

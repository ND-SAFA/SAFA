import {
  ExpandableProps,
  IconVariant,
  LoadingProps,
  MinimalProps,
  TableColumn,
  TableGroupRow,
  TableRow,
  TestableProps,
} from "@/types";

/**
 * The props for a table component.
 */
export interface TableProps<Row = TableRow>
  extends LoadingProps,
    TestableProps {
  /**
   * The columns to render in the table.
   */
  columns: TableColumn<Row>[];
  /**
   * The column names that are currently visible, if not all of them.
   */
  visibleColumns?: string[];
  /**
   * The rows of the table.
   */
  rows: Row[];
  /**
   * The field on each row that is unique.
   */
  rowKey: string | ((row: Row) => string);
  /**
   * The number of rows to display per page.
   */
  rowsPerPage?: number;
  /**
   * Enables selection of rows.
   */
  selection?: "single" | "multiple";
  /**
   * The values of selected rows.
   */
  selected?: Row[];
  /**
   * The ids of expanded rows.
   */
  expanded?: string[];
  /**
   * The text to filter by.
   */
  filterText?: string;
  /**
   * A function to filter the table with.
   */
  filter?: (
    rows: Row[],
    filterText: string | undefined,
    cols: TableColumn[]
  ) => Row[];
  /**
   * Which attribute to sort by.
   */
  sortBy?: string;
  /**
   * Whether to sort descending.
   */
  sortDesc?: boolean;
  /**
   * A function to sort the table with.
   */
  sort?(rows: Row[], sortBy: string, descending: boolean): Row[];
  /**
   * Where to place separators. Defaults to horizontal.
   */
  separator?: "horizontal" | "vertical" | "cell" | "none";
  /**
   * Any cells can be customized through the slot `body-cell-[name]`.
   */
  customCells?: (string | symbol | number)[];
  /**
   * Whether to display densely.
   */
  dense?: boolean;
  /**
   * If true, virtual scroll will be enabled.
   */
  virtualScroll?: boolean;
}

/**
 * The props for a table component that can display groups of rows.
 */
export interface GroupableTableProps
  extends Pick<
      TableProps,
      "columns" | "rows" | "rowKey" | "loading" | "expanded"
    >,
    Partial<Pick<TableProps, "customCells">>,
    ExpandableProps {
  /**
   * The name of an item.
   */
  itemName?: string;
  /**
   * The default row key to group by.
   */
  defaultGroupBy?: string;
  /**
   * The default row keys to sort by.
   */
  defaultSortBy?: string;
  /**
   * The default sort direction.
   */
  defaultSortDesc?: boolean;
  /**
   * Determines whether a row should be visible.
   */
  filterRow?(row: TableRow): boolean;
}

/**
 * The props for a table header component on groupable tables.
 */
export interface GroupableTableHeaderProps {
  /**
   * The columns to render in the table.
   */
  columns: TableColumn[];
  /**
   * The search text to filter with.
   */
  searchText: string | null;
  /**
   * The label for the searchbar.
   */
  searchLabel: string;
  /**
   * The row key to group by.
   */
  groupBy: string | undefined;
  /**
   * The row keys to sort by.
   */
  sortBy: string | undefined;
  /**
   * Whether to sort in descending order.
   */
  sortDesc: boolean;
  /**
   * Whether the table is in fullscreen mode.
   */
  inFullscreen: boolean;
}

/**
 * The props for a groupable table row component.
 */
export interface GroupableTableRowProps extends ExpandableProps {
  /**
   * Props passed in from the quasar table.
   */
  quasarProps: Record<string, unknown>;
  /**
   A generic row of a table, or a group header.
   */
  row: TableGroupRow;
  /**
   * The visible table columns.
   */
  columns: TableColumn[];
  /**
   * Whether the row is expanded.
   */
  expand?: boolean;
}

/**
 * The props for a table component that can display selectable rows.
 */
export interface SelectorTableProps
  extends Pick<TableProps, "columns" | "rows" | "rowKey" | "loading">,
    Partial<Pick<TableProps, "customCells">>,
    MinimalProps {
  /**
   * The values of selected rows.
   */
  selected?: TableRow[];
  /**
   * The name of an item.
   */
  itemName?: string;
  /**
   * Whether elements can be added.
   */
  addable?: boolean;
  /**
   * Whether these rows are editable.
   */
  editable?: boolean | ((row: TableRow) => boolean);
  /**
   * Whether these rows are deletable.
   */
  deletable?: boolean | ((row: TableRow) => boolean);
  /**
   * A hint to display beneath the searchbar.
   */
  searchHint?: string;
  /**
   * Optional icons to use for the add, edit, and delete buttons.
   */
  icons?: {
    add: IconVariant;
    edit: IconVariant;
    delete: IconVariant;
  };
}

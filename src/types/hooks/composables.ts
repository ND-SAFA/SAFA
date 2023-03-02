import { ComputedRef, Ref, WritableComputedRef } from "vue";
import { TableColumn } from "@/types";

/**
 * Defines a hook for using the app theme.
 */
export interface ThemeHook<Theme> {
  /**
   * The current theme.
   */
  theme: Theme;
  /**
   * Whether the app is in dark mode.
   */
  darkMode: WritableComputedRef<boolean>;
  /**
   * Toggles whether the theme is in dark mode.
   * @param dark - The explicit mode to set.
   *        If none is given, the current mode is toggled.
   */
  toggleDarkMode(dark?: boolean): void;
}

/**
 * Props for creating a table filter hook.
 */
export interface TableFilterProps {
  /**
   * The columns to render in the table.
   */
  columns: TableColumn[];
  /**
   * The rows of the table.
   */
  rows: Record<string, unknown>[];
  /**
   * The name of an item.
   */
  itemName?: string;
}

/**
 * Defines a hook for filtering table rows.
 */
export interface TableFilterHook {
  /**
   * The table rows after filtering.
   */
  filteredRows: ComputedRef<Record<string, unknown>[]>;
  /**
   * The table search text.
   */
  searchText: Ref<string | null>;
  /**
   * The table search label.
   */
  searchLabel: ComputedRef<string>;
}

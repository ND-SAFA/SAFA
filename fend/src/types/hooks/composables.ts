import { ComputedRef, Ref, WritableComputedRef } from "vue";
import { QVueGlobals, Screen } from "quasar/dist/types";
import { TableColumn } from "@/types";

/**
 * Defines a hook for using the app theme.
 */
export interface ThemeHook {
  /**
   * The current theme.
   */
  theme: QVueGlobals;
  /**
   * Whether the app is in dark mode.
   */
  darkMode: WritableComputedRef<boolean>;
  /**
   * Loads the stored dark mode setting.
   */
  loadDarkMode(): void;
  /**
   * Toggles whether the theme is in dark mode.
   * @param dark - The explicit mode to set.
   *        If none is given, the current mode is toggled.
   *        If "auto" is given, the mode is set based on the time of day.
   */
  toggleDarkMode(dark?: boolean | "auto"): void;
}

/**
 * Defines a hook for managing changes with the screen size.
 */
export interface ScreenHook {
  /**
   * Whether the current window is small enough to
   * collapse content vertically.
   */
  smallWindow: ComputedRef<boolean>;
  /**
   * The quasar screen hook.
   */
  screen: ComputedRef<Screen>;
}

/**
 * The properties for the time display.
 */
export interface TimeDisplayProps {
  /**
   * The start of the duration, as an ISO timestamp.
   */
  getStart: () => string;
  /**
   * The end of the duration, as an ISO timestamp.
   * Set as empty string to display the current time.
   */
  getEnd: () => string;
}

/**
 * A hook for managing the display of a timestamp that updates in real-time.
 */
export interface TimeDisplayHook {
  /**
   * The current time.
   */
  displayTime: ComputedRef<string>;
  /**
   * Updates the time display manually.
   */
  resetTime(): void;
  /**
   * Stops the time display from updating.
   */
  stopTime(): void;
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
  /**
   * Determines whether a row should be visible.
   */
  filterRow?(row: Record<string, unknown>): boolean;
  /**
   * The default row keys to sort by.
   */
  defaultSortBy?: string;
  /**
   * The default sort direction.
   */
  defaultSortDesc?: boolean;
}

/**
 * Defines a hook for sorting and filtering table rows.
 */
export interface TableFilterHook {
  /**
   * The table search text.
   */
  searchText: Ref<string | null>;
  /**
   * The table search label.
   */
  searchLabel: ComputedRef<string>;
  /**
   * The table search sort field.
   */
  sortBy: Ref<string | undefined>;
  /**
   * The table search sort direction.
   */
  sortDesc: Ref<boolean>;
  /**
   * The table rows after filtering.
   */
  filteredRows: ComputedRef<Record<string, unknown>[]>;
}

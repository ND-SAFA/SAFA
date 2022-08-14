import { DataTableHeader } from "vuetify";

/**
 * Represents the render info for a data table group header.
 */
export interface DataTableGroup<T> {
  group: string;
  groupBy: (keyof T)[];
  isMobile: boolean;
  items: T[];
  headers: DataTableHeader[];
  isOpen: boolean;
  toggle: () => void;
  remove: () => void;
}

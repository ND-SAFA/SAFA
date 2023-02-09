import { FlatArtifact, FlatTraceLink } from "@/types";

/**
 * A Vue 3 Data Table Header.
 */
export interface DataTableHeader<T = FlatTraceLink | FlatArtifact> {
  text: string;
  value: string;
  align?: "start" | "center" | "end";
  sortable?: boolean;
  filterable?: boolean;
  groupable?: boolean;
  divider?: boolean;
  class?: string | string[];
  cellClass?: string | string[];
  width?: string | number;
  filter?: (value: T, search: string, item: T) => boolean;
  sort?: (a: T, b: T) => number;
}

export type ArtifactTableHeader = DataTableHeader<FlatArtifact>;
export type TraceTableHeader = DataTableHeader<FlatTraceLink>;

/**
 * Represents the render info for a data table group header.
 */
export interface DataTableGroup<T = FlatTraceLink | FlatArtifact> {
  group: string;
  groupBy: (keyof T)[];
  isMobile: boolean;
  items: T[];
  headers: DataTableHeader<T>[];
  isOpen: boolean;
  toggle: () => void;
  remove: () => void;
}

export type ArtifactTableGroup = DataTableGroup<FlatArtifact>;
export type TraceTableGroup = DataTableGroup<FlatTraceLink>;

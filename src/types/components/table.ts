import { DataTableHeader } from "vuetify";
import { FlatArtifact, FlatTraceLink } from "@/types";

/**
 * Represents the render info for a data table group header.
 */
export interface DataTableGroup<T = FlatTraceLink | FlatArtifact> {
  group: string;
  groupBy: (keyof T)[];
  isMobile: boolean;
  items: T[];
  headers: DataTableHeader[];
  isOpen: boolean;
  toggle: () => void;
  remove: () => void;
}

export type ArtifactTableGroup = DataTableGroup<FlatArtifact>;
export type TraceTableGroup = DataTableGroup<FlatTraceLink>;

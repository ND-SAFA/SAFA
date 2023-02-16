import { ArtifactSchema, IconVariant } from "@/types";

/**
 * Represents an item in an artifact search list.
 */
export type ArtifactSearchItem =
  | ArtifactSchema
  | { header: string }
  | { divider: boolean };

/**
 * Defines a navigation option that links to a page.
 */
export interface NavOption {
  /**
   * The option's name.
   */
  label: string;
  /**
   * The option's icon id.
   */
  icon: IconVariant;
  /**
   * If true, a divider will be displayed above this option.
   */
  divider?: boolean;
  /**
   * If true, this option will be hidden.
   */
  disabled?: boolean;
  /**
   * The navigation path corresponding to this option.
   */
  path:
    | string
    | { path: string; query: Record<string, string | (string | null)[]> };
}

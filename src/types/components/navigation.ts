import { IconVariant, URLQuery } from "@/types";

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
  path: string | { path: string; query: URLQuery };
}

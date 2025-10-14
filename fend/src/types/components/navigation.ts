import { IconVariant, ThemeColor, URLQuery } from "@/types";

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
   * A name to optionally display below the icon.
   */
  iconTitle?: string;
  /**
   * If true, a divider will be displayed above this option.
   */
  divider?: boolean;
  /**
   * If true, this option will be hidden.
   */
  disabled?: boolean;
  /**
   * The color to display for this option.
   */
  color?: ThemeColor;
  /**
   * The subtitle to display for this option, beneath the label.
   */
  subtitle?: string;
  /**
   * The navigation path corresponding to this option.
   */
  path: string | { path: string; query: URLQuery };
  /**
   * The tooltip to display on option when hovered.
   */
  tooltip?: string;
  /**
   * Additional classes to display.
   */
  class?: string;
}

/**
 * The props for displaying an authenticated page.
 */
export interface PrivatePageProps {
  /**
   * Whether to display in full window mode.
   */
  fullWindow?: boolean;
  /**
   * Whether to display in small window mode.
   */
  smallWindow?: boolean;
  /**
   * Whether a cytoscape graph is being displayed.
   */
  graph?: boolean;
  /**
   * The page title to display.
   */
  title?: string;
  /**
   * The page subtitle to display.
   */
  subtitle?: string;
  /**
   * Whether to display a back button to the project graph.
   */
  backToProject?: boolean;
}

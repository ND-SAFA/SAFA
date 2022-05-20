import { ArtifactData, CytoEvent } from "@/types";
import { EventObject } from "cytoscape";

/**
 * Depicts options given to cytoscape context menu plugin options.
 */
export interface ContextMenuOptions {
  /**
   * The event triggering when the context menu appears.
   */
  evtType: CytoEvent;
  /**
   * List of initial menu item
   * A menu item must have either onClickFunction or submenu or both
   */
  menuItems: MenuItem[];
  /**
   * CSS classes that menu items will have
   */
  menuItemClasses: string[];
  /**
   * CSS classes that context menu will have
   */
  contextMenuClasses: string[];
  /**
   * Indicates that the menu item has a submenu.
   * If not provided default one will be used
   */
  submenuIndicator?: ContextIconDefinition;
}

/**
 * Submenu Icon Definition
 */
export interface ContextIconDefinition {
  /**
   * Relative path to icon to be used for submenu
   */
  src: string;
  /**
   * Width of icon in pixels
   */
  width: number;
  /**
   * Height of icon in pixels
   */
  height: number;
}
/**
 * Depicts item in the cytoscape context menu.
 * Docs taken from: https://github.com/iVis-at-Bilkent/cytoscape.js-context-menus
 */
export interface MenuItem {
  /**
   * A unique identifier for this item.
   */
  id: string;
  /**
   * Display content of the menu item
   */
  content: string;
  /**
   * Tooltip text for menu item
   */
  tooltipText: string;
  /**
   * Filters the elements to have this menu item on cxttap
   * If the selector is not truthy no elements will have this menu item on cxttap
   */
  selector?: string;
  /**
   * Item Icon
   */
  image?: ContextIconDefinition;

  /**
   * The function to be executed on click.
   */
  onClickFunction?: (event: EventObject) => void;
  /**
   * Returns whether item should be displayed in context menu
   * at start of event.
   */
  isVisible?: (artifact: ArtifactData | undefined) => boolean;
  /**
   * Whether the item will be created as disabled.
   */
  disabled?: boolean;
  /**
   * Whether the item will be shown or not.
   */
  show?: boolean;
  /**
   * Whether the item will have a trailing divider.
   */
  hasTrailingDivider?: boolean;
  /**
   * Whether core instance will have this item on cxttap
   */
  coreAsWell?: boolean;
  /**
   * Shows the listed menuItems as a submenu for this item.
   * Item must have either submenu or onClickFucntion or both.
   */
  submenu?: MenuItem[];
}

/**
 * Defines the cytoscape context menu instance.
 */
export interface CytoContextMenu {
  /**
   * Shows a menu item.
   * @param id - The item id to show.
   */
  showMenuItem(id: string): void;
  /**
   * Hides a menu item.
   * @param id - The item id to hide.
   */
  hideMenuItem(id: string): void;
}

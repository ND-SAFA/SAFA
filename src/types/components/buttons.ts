import { EmptyLambda } from "@/types";

/**
 * Enumerates button types.
 */
export enum ButtonType {
  ICON = "icon",
  TEXT = "text",
  CHECKMARK_MENU = "checkmarkmenu",
  LIST_MENU = "listmenu",
}

/**
 * Defines a general button definition.
 */
export type ButtonDefinition =
  | IconDefinition
  | ListMenuDefinition
  | CheckmarkMenuDefinition;

/**
 * BaseButtonDefinition
 */

export interface BaseButtonDefinition {
  label: string;
  isDisabled?: boolean;
  buttonColor?: string;
  isHidden?: boolean;
}

/**
 * Defines an icon button.
 */
export interface IconDefinition extends BaseButtonDefinition {
  type: ButtonType.ICON;
  handler?: EmptyLambda;
  icon?: string;
}

/**
 * Local representation of generated menu items.
 */
export interface ButtonMenuItem {
  name: string;
  tooltip?: string;
  onClick: EmptyLambda;
}

/**
 * Defines an menu button.
 */
interface MenuDefinition extends BaseButtonDefinition {
  menuItems?: ButtonMenuItem[];
  buttonIsText?: boolean;
  itemColor?: string;
  showSelectedValue?: boolean;
}

/**
 * Defines an list menu button.
 */
export interface ListMenuDefinition extends MenuDefinition {
  type: ButtonType.LIST_MENU;
  selectedItem?: string;
}

/**
 * Defines an checkmark menu button.
 */
export interface CheckmarkMenuDefinition extends MenuDefinition {
  type: ButtonType.CHECKMARK_MENU;
  icon?: string;
  checkmarkValues: boolean[];
}

/**
 * Represents an option for a select menu.
 */
export interface SelectOption {
  /**
   * The iud of the option to use as a stored.
   */
  id: string;
  /**
   * The name of the option to display.
   */
  name: string;
}

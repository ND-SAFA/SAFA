export enum ButtonType {
  ICON = "icon",
  TEXT = "text",
  CHECKMARK_MENU = "checkmarkmenu",
  LIST_MENU = "listmenu",
}

type EmptyHandler = () => void;

export type ButtonDefinition =
  | IconDefinition
  | ListMenuDefinition
  | CheckmarkMenuDefinition;

export interface IconDefinition {
  type: ButtonType.ICON;
  handler?: EmptyHandler;
  label: string;
  icon?: string;
}

interface MenuDefinition {
  label: string;
  menuItems?: string[];
  menuHandlers?: EmptyHandler[];
  buttonColor?: string;
  buttonIsText?: boolean;
  itemColor?: string;
  showSelectedValue?: boolean;
}
export interface ListMenuDefinition extends MenuDefinition {
  type: ButtonType.LIST_MENU;
}

export interface CheckmarkMenuDefinition extends MenuDefinition {
  type: ButtonType.CHECKMARK_MENU;
  icon?: string;
  checkmarkValues: boolean[];
}

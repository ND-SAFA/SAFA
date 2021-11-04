import { Artifact } from "@/types/domain/artifact";
import { Link, TraceLink } from "@/types/domain/links";
import { ProjectIdentifier, ProjectVersion } from "@/types/domain/project";

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
  isDisabled?: boolean;
}

export interface CheckmarkMenuDefinition extends MenuDefinition {
  type: ButtonType.CHECKMARK_MENU;
  icon?: string;
  checkmarkValues: boolean[];
}

export type OptionalProjectIdentifier = ProjectIdentifier | undefined;
export type OptionalProjectVersion = ProjectVersion | undefined;
export type ModalSize = "xxs" | "xs" | "s" | "m" | "l";
export type StepState = [string, boolean];

export interface ProjectFile {
  file?: File;
  errors: string[];
}
export interface ArtifactFile extends ProjectFile {
  type: string;
  artifacts: Artifact[];
}

export interface TraceFile extends ProjectFile {
  source: string;
  target: string;
  isGenerated: boolean;
  traces: TraceLink[];
}

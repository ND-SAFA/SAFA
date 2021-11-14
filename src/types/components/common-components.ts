import { Artifact } from "@/types";
import { TraceLink } from "@/types";
import { ProjectIdentifier, ProjectVersion } from "@/types";

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
 * Defines an empty handler.
 */
type EmptyHandler = () => void;

/**
 * Defines a general button definition.
 */
export type ButtonDefinition =
  | IconDefinition
  | ListMenuDefinition
  | CheckmarkMenuDefinition;

/**
 * Defines an icon button.
 */
export interface IconDefinition {
  type: ButtonType.ICON;
  handler?: EmptyHandler;
  label: string;
  icon?: string;
}

/**
 * Defines an menu button.
 */
interface MenuDefinition {
  label: string;
  menuItems?: string[];
  menuHandlers?: EmptyHandler[];
  buttonColor?: string;
  buttonIsText?: boolean;
  itemColor?: string;
  showSelectedValue?: boolean;
}

/**
 * Defines an list menu button.
 */
export interface ListMenuDefinition extends MenuDefinition {
  type: ButtonType.LIST_MENU;
  isDisabled?: boolean;
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
 * An optional project identifier.
 */
export type OptionalProjectIdentifier = ProjectIdentifier | undefined;

/**
 * An optional project version.
 */
export type OptionalProjectVersion = ProjectVersion | undefined;

/**
 * Defines the possible modal sizes.
 */
export type ModalSize = "xxs" | "xs" | "s" | "m" | "l";

/**
 * Defines the name of a step and whether the step is currently valid.
 */
export type StepState = [string, boolean];

/**
 * Defines a project file.
 */
export interface ProjectFile {
  /**
   * The file, if loaded.
   */
  file?: File;
  /**
   * Any errors with the file.
   */
  errors: string[];
  isValid: boolean;
}

/**
 * Defines a project artifact file.
 */
export interface ArtifactFile extends ProjectFile {
  /**
   * The artifact type.
   */
  type: string;
  /**
   * A list of artifacts from the file.
   */
  artifacts: Artifact[];
}

/**
 * Defines a project trace file.
 */
export interface TraceFile extends ProjectFile {
  /**
   * The source type of the trace file.
   */
  source: string;
  /**
   * The target type of the trace file.
   */
  target: string;
  /**
   * If true, the trace file should be generated.
   */
  isGenerated: boolean;
  /**
   * A list of traces from the file.
   */
  traces: TraceLink[];
}

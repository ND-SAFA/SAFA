import { Artifact, EmptyLambda } from "@/types";
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
 * Defines an menu button.
 */
interface MenuDefinition extends BaseButtonDefinition {
  menuItems?: string[];
  menuHandlers?: EmptyLambda[];
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
  sourceId: string;
  /**
   * The target type of the trace file.
   */
  targetId: string;
  /**
   * If true, the trace file should be generated.
   */
  isGenerated: boolean;
  /**
   * A list of traces from the file.
   */
  traces: TraceLink[];
}

/**
 * Defines a toggleable item of data.
 */
export interface DataItem<T> {
  /**
   * Whether this item is enabled.
   */
  value: boolean;
  /**
   * The item of data.
   */
  item: T;
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

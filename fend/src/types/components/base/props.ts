import {
  ArtifactSchema,
  IconVariant,
  IdentifierSchema,
  ThemeColor,
  TraceLinkSchema,
} from "@/types";

/**
 * The possible increments for spacing.
 */
export type SizeType =
  | ""
  | "1"
  | "2"
  | "3"
  | "4"
  | "5"
  | "6"
  | "7"
  | "8"
  | "9"
  | "10"
  | "11"
  | "12";

/**
 * Defines props for a component with margins.
 */
export interface MarginProps {
  /**
   * The x margin.
   */
  x?: SizeType;
  /**
   * The y margin.
   */
  y?: SizeType;
  /**
   * The left margin.
   */
  l?: SizeType;
  /**
   * The right margin.
   */
  r?: SizeType;
  /**
   * The top margin.
   */
  t?: SizeType;
  /**
   * The bottom margin.
   */
  b?: SizeType;
}

/**
 * Defines props for a component that can display a label.
 */
export interface LabelProps {
  /**
   * The label to display.
   */
  label?: string;
}

/**
 * Defines props for a component with a color.
 */
export interface ColorProps {
  /**
   * The color to render the component with.
   */
  color?: ThemeColor;
}

/**
 * Defines props for a component with a css class name.
 */
export interface ClassNameProps {
  /**
   * The classnames to include on this component.
   */
  class?: string;
}

/**
 * Defines props for a component with a css style.
 */
export interface StyleProps {
  /**
   * The css style to apply.
   */
  style?: string;
}

/**
 * Defines props for a component with an icon.
 */
export interface IconProps {
  /**
   * The type of icon to render.
   */
  icon?: IconVariant;
}

/**
 * Defines props for a component that can load.
 */
export interface LoadingProps {
  /**
   * Whether the component is loading.
   */
  loading?: boolean;
}

/**
 * Defines props for a component that can be disabled.
 */
export interface DisabledProps {
  /**
   * Whether the component is disabled.
   */
  disabled?: boolean;
}

/**
 * Defines props for a component that can be small or large.
 */
export interface SizeProps {
  /**
   * Renders a smaller component.
   */
  small?: boolean;
  /**
   * Renders a larger component.
   */
  large?: boolean;
}

/**
 * Defines props for a component that can be outlined.
 */
export interface OutlinedProps {
  /**
   * If true, the component will be rendered as outlined.
   */
  outlined?: boolean;
}

/**
 * Defines props for a component that can be clicked.
 */
export interface ClickableProps {
  /**
   * Whether the component is clickable.
   */
  clickable?: boolean;
}

/**
 * Defines props for a component that can be removed.
 */
export interface RemovableProps {
  /**
   * Whether the component is removable, displaying a remove button.
   */
  removable?: boolean;
}

/**
 * Defines props for a component that can be made minimal.
 */
export interface MinimalProps {
  /**
   * Whether the component should be displayed with minimal information.
   */
  minimal?: boolean;
}

/**
 * Defines props for a component that can be expanded.
 */
export interface ExpandableProps {
  /**
   * Whether the component can be expanded.
   */
  expandable?: boolean;
}

/**
 * Defines props for a component that can be opened.
 */
export interface OpenableProps {
  /**
   * Whether the component is open.
   */
  open: boolean;
}

/**
 * Defines props for a component that can display an error.
 */
export interface ErrorMessageProps {
  /**
   * An error message to display, if one exists.
   */
  errorMessage?: string | false;
}

/**
 * Defines props for a component that can have multiple items instead of one.
 */
export interface MultipleProps {
  /**
   * Whether to allow multiple items.
   */
  multiple?: boolean;
}

/**
 * Defines props for a component that can be selected in tests.
 */
export interface TestableProps {
  /**
   * The testing selector to set.
   */
  dataCy?: string;
}

/**
 * Defines props for a component that displays a project.
 */
export interface ProjectIdProps {
  /**
   * The project to display or edit.
   */
  project: IdentifierSchema;
}

/**
 * Defines props for a component that displays an artifact.
 */
export interface ArtifactProps {
  /**
   * The artifact to display or edit.
   */
  artifact: ArtifactSchema;
}

/**
 * Defines props for a component that displays a trace link.
 */
export interface TraceProps {
  /**
   * The trace link to display or edit.
   */
  trace: TraceLinkSchema;
}

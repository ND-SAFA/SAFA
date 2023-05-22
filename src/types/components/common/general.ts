import { IconVariant } from "@/types";

/**
 * The methods of alignment.
 */
export type AlignType = "start" | "center" | "end";

/**
 * The methods of justifying.
 */
export type JustifyType = AlignType | "between" | "around";

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

export type ThemeColor =
  | "primary"
  | "secondary"
  | "accent"
  | "positive"
  | "negative"
  | string;

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
 * Defines props for a component that can be selected in tests.
 */
export interface TestableProps {
  /**
   * The testing selector to set.
   */
  dataCy?: string;
}

/**
 * Defines emits for a clickable component.
 */
export interface ClickableEmits {
  /**
   * Called when clicked.
   */
  (e: "click"): void;
}

/**
 * Defines emits for a component updating a model.
 */
export interface ModelEmits<T> {
  /**
   * Called when the model is updated.
   */
  (e: "update:modelValue", value: T): void;
}

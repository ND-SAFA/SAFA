import {
  ArtifactSchema,
  ArtifactTypeSchema,
  AttributeCollectionSchema,
  AttributeSchema,
  ClassNameProps,
  ColorProps,
  DisabledProps,
  ErrorMessageProps,
  LabelProps,
  MarginProps,
  MultipleProps,
  OutlinedProps,
  SelectOption,
  TestableProps,
} from "@/types";

/**
 * Defines the text input component props.
 */
export interface TextInputProps
  extends LabelProps,
    ClassNameProps,
    ErrorMessageProps,
    Pick<MarginProps, "b">,
    DisabledProps,
    TestableProps {
  /**
   * The model value.
   */
  modelValue?: string | number | null;
  /**
   * A hint to display below the input.
   */
  hint?: string;
  /**
   * Whether to hide the hint.
   */
  hideHint?: boolean;
  /**
   * The base input component type to use.
   */
  type?:
    | "text"
    | "password"
    | "textarea"
    | "email"
    | "search"
    | "tel"
    | "file"
    | "number"
    | "url"
    | "time"
    | "date";
  /**
   * The number of rows to display when the type is `textarea`.
   */
  rows?: number;
}

/**
 * Defines the file input component props.
 */
export interface FileInputProps
  extends ErrorMessageProps,
    MultipleProps,
    TestableProps {
  /**
   * The synchronized files value.
   */
  modelValue?: File | File[] | null;
}

/**
 * Defines the select input component props.
 */
export interface SelectInputProps
  extends OutlinedProps,
    LabelProps,
    DisabledProps {
  /**
   * The selected option to manage.
   */
  modelValue?: unknown;
  /**
   * The options to select from.
   */
  options: unknown[];
  /**
   * The key of an option's id.
   */
  optionValue?: string | ((opt: unknown) => string);
  /**
   * The key of an option's display label.
   */
  optionLabel?: string | ((opt: unknown) => string);
  /**
   * Only saves the option's value, not the entire object.
   */
  optionToValue?: boolean;
}

/**
 * Defines the multiselect input component props.
 */
export interface MultiselectInputProps
  extends Pick<
      SelectInputProps,
      | "label"
      | "optionValue"
      | "optionLabel"
      | "optionToValue"
      | "outlined"
      | "disabled"
    >,
    Pick<TextInputProps, "hint">,
    ErrorMessageProps,
    ClassNameProps,
    Pick<MarginProps, "b">,
    TestableProps {
  /**
   The selected options to manage.
   */
  modelValue: unknown[];
  /**
   * The options to select from.
   */
  options: string[] | SelectOption[] | unknown[];
  /**
   * If true, new options can be created by pressing enter.
   */
  addValues?: boolean;
  /**
   * Whether to display a button to clear the input.
   */
  clearable?: boolean;
}

/**
 * Defines the password input component props.
 */
export interface PasswordInputProps extends LabelProps, ErrorMessageProps {
  /**
   * The model value.
   */
  modelValue: string;
}

/**
 * Defines the project input component props.
 */
export interface ProjectInputProps extends MultipleProps {
  modelValue: string[] | string | undefined;
  excludeCurrentProject?: boolean;
}

/**
 * Defines the searchbar component props.
 */
export interface SearchbarProps extends LabelProps {
  /**
   * The search text to manage.
   */
  modelValue: string;
  /**
   * A hint to display below the input.
   */
  hint?: string;
}

/**
 * Defines the switch input component props.
 */
export interface SwitchInputProps extends LabelProps, ColorProps {
  /**
   * The switch value to manage.
   */
  modelValue: boolean;
}

/**
 * Defines the artifact input component props.
 */
export interface ArtifactInput extends LabelProps, MultipleProps {
  /**
   * The artifact(s) to manage.
   */
  modelValue: string[] | string | undefined;
  /**
   * If true, only artifacts in the current view are displayed.
   */
  onlyDocumentArtifacts?: boolean;
  /**
   * If set, these artifacts will be removed from the list.
   */
  hiddenArtifactIds?: string[];
  /**
   * If set, these types will be hidden from the initial artifact list.
   */
  defaultHiddenTypes?: string[];
}

/**
 * Defines the artifact type input component props.
 */
export interface ArtifactTypeInputProps
  extends MultipleProps,
    LabelProps,
    ErrorMessageProps,
    Pick<TextInputProps, "hint"> {
  /**
   * The artifact type(s) to manage.
   */
  modelValue: string[] | string | null;
  /**
   * If true, the number of artifacts matching this type is displayed.
   */
  showCount?: boolean;
  /**
   * If true, the input and chips are displayed more compactly.
   */
  dense?: boolean;
}

/**
 * Defines the attribute input component props.
 */
export interface AttributeInputProps {
  /**
   * The collection of attribute values.
   */
  attributes: AttributeCollectionSchema;
  /**
   * The attribute being edited.
   */
  attribute: AttributeSchema;
}

/**
 * Defines the attribute list input component props.
 */
export interface AttributeListInputProps {
  /**
   * The artifact to manage the collection of attributes within.
   */
  artifact: ArtifactSchema;
}

/**
 * Defines the artifact level input component props.
 */
export interface ArtifactLevelInputProps {
  /**
   * The artifact level to display and allow editing of.
   */
  artifactType: ArtifactTypeSchema;
}

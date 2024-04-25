import {
  ArtifactSchema,
  ClassNameProps,
  ClickableProps,
  ColorProps,
  IconProps,
  SelectOption,
  TestableProps,
  URLQuery,
} from "@/types";

/**
 * Defines props for a component that displays an artifact list item.
 */
export interface ArtifactListItemProps extends ClickableProps {
  /**
   * The artifact to display.
   */
  artifact: ArtifactSchema;
  /**
   * Whether to display the title.
   */
  displayTitle?: boolean;
  /**
   * Whether to display a divider between the content.
   */
  displayDivider?: boolean;
  /**
   * Whether to default the artifact content to expanded.
   */
  defaultExpanded?: boolean;
  /**
   * Whether to expand to full width.
   */
  fullWidth?: boolean;
}

/**
 * Defines props for a component that displays an artifact list.
 */
export interface ArtifactListProps extends TestableProps {
  /**
   * The artifacts to display.
   */
  artifacts: ArtifactSchema[];
  /**
   * A selector for each list item.
   */
  itemDataCy?: string;
  /**
   * How many action columns to display.
   */
  actionCols?: number;
  /**
   * Whether to display at full width.
   */
  fullWidth?: boolean;
}

/**
 * Defines props for a component that displays a expansion item.
 */
export interface ExpansionItemProps {
  /**
   * The label to display.
   */
  label: string;
  /**
   * The caption ti display under the label.
   */
  caption?: string;
}

/**
 * Defines props for a component that displays a list of components.
 */
export interface ListProps {
  /**
   * Whether to add a border to the list.
   */
  bordered?: boolean;
  /**
   * The number of pixels to set the scroll area height to.
   */
  scrollHeight?: number;
}

/**
 * Defines props for a component that displays a list item.
 */
export interface ListItemProps
  extends ClickableProps,
    IconProps,
    ColorProps,
    TestableProps {
  /**
   * The item title, instead of using the `default` slot.
   */
  title?: string;
  /**
   * The item subtitle, instead of using the `subtitle` slot.
   */
  subtitle?: string;
  /**
   * The icon id, if not using an icon variant name.
   */
  iconId?: string;
  /**
   * A name to optionally display below the icon.
   */
  iconTitle?: string;
  /**
   * The item tooltip.
   * If set to true, a tooltip will be generated based on the title and subtitle.
   */
  tooltip?: true | string;
  /**
   * Where the list item navigates to when clicked.
   */
  to?: string | { path: string; query: URLQuery };
  /**
   * Whether to render a divider between the title and subtitle.
   */
  divider?: boolean;
  /**
   * The optional number of columns ot take up with the action space, out of 12.
   */
  actionCols?: number;
}

/**
 * Defines props for a component that displays a set of tabs.
 */
export interface TabListProps extends ClassNameProps {
  /**
   * The tab id currently selected.
   */
  modelValue: string;
  /**
   * The tabs to display.
   */
  tabs: SelectOption[];
  /**
   * Whether to display tab options to the left side, instead of the top.
   */
  vertical?: boolean;
}

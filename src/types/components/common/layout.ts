import {
  ClassNameProps,
  ColorProps,
  DetailsOpenState,
  IconProps,
} from "@/types";

/**
 * Defines props for the right sidebar detail panel.
 */
export interface DetailsPanelProps {
  /**
   * The panel being controlled.
   */
  panel: DetailsOpenState;
}

/**
 * Defines props for displaying a panel of content.
 */
export interface PanelCardProps extends ColorProps, IconProps, ClassNameProps {
  /**
   * A title to render on the card.
   */
  title?: string;
  /**
   * A subtitle title to render on the card.
   */
  subtitle?: string;
  /**
   * The panel's container's classes.
   */
  containerClass?: string;
  /**
   * Whether this card should be displayed minimally.
   */
  minimal?: boolean;
  /**
   * Whether this card should display an icon to collapse content and just show the title.
   */
  collapsable?: boolean;
  /**
   * Whether this card should display no border.
   */
  borderless?: boolean;
}

import { SearchMode } from "@/types";

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

/**
 * Represents an option for searching modes.
 */
export interface SearchSelectOption extends SelectOption {
  /**
   * The iud of the option to use as a stored.
   */
  id: SearchMode;
  /**
   * Describes this search mode.
   */
  description: string;
  /**
   * The placeholder for the search input.
   */
  placeholder: string;
  /**
   * Whether this mode searches for artifacts.
   */
  artifactSearch?: boolean;
}

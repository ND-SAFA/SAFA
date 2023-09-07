import { SearchMode } from "@/types";

/**
 * Represents an option for a select menu.
 */
export interface SelectOption<T extends string = string> {
  /**
   * The iud of the option to use as a stored.
   */
  id: T;
  /**
   * The name of the option to display.
   */
  name: string;
}

/**
 * Represents an option for searching modes.
 */
export interface SearchSelectOption extends SelectOption<SearchMode> {
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

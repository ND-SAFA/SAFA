import { WritableComputedRef } from "vue";

/**
 * Defines a hook for using the app theme.
 */
export interface ThemeHook<Theme> {
  /**
   * The current theme.
   */
  theme: Theme;
  /**
   * Whether the app is in dark mode.
   */
  darkMode: WritableComputedRef<boolean>;
  /**
   * Toggles whether the theme is in dark mode.
   * @param dark - The explicit mode to set.
   *        If none is given, the current mode is toggled.
   */
  toggleDarkMode(dark?: boolean): void;
}

import { ComputedRef } from "vue";

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
  darkMode: ComputedRef<boolean>;
  /**
   * Toggles whether the theme is in dark mode.
   */
  toggleDarkMode(): void;
}

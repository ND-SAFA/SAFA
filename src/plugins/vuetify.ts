import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import { LocalStorageKeys } from "@/types";
import { ThemeColors } from "@/util";

const variants = {
  light: "light",
  dark: "dark",
};

export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme:
      localStorage.getItem(LocalStorageKeys.darkMode) === variants.dark
        ? variants.dark
        : variants.light,
    themes: {
      [variants.light]: {
        dark: false,
        colors: {
          primary: ThemeColors.primary,
          secondary: ThemeColors.secondary,
          accent: ThemeColors.accent,

          info: ThemeColors.primary,
          warning: ThemeColors.warning,
          error: ThemeColors.error,
          success: ThemeColors.added,

          text: ThemeColors.textLight,
          neutral: ThemeColors.white,
          background: ThemeColors.backgroundLight,
          selected: ThemeColors.selectedLight,

          addedLight: ThemeColors.addedLight,
          modifiedLight: ThemeColors.modifiedLight,
          removedLight: ThemeColors.removedLight,
        },
      },
      [variants.dark]: {
        dark: true,
        colors: {
          primary: ThemeColors.primaryDark,
          secondary: ThemeColors.secondary,
          accent: ThemeColors.accent,

          info: ThemeColors.primary,
          warning: ThemeColors.warning,
          error: ThemeColors.error,
          success: ThemeColors.added,

          text: ThemeColors.textDark,
          neutral: ThemeColors.black,
          background: ThemeColors.backgroundDark,
          selected: ThemeColors.selectedDark,

          addedLight: ThemeColors.addedLight,
          modifiedLight: ThemeColors.modifiedLight,
          removedLight: ThemeColors.removedLight,
        },
      },
    },
  },
});

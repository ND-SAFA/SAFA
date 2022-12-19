import Vue from "vue";
import Vuetify from "vuetify/lib/framework";
import { LocalStorageKeys } from "@/types";
import { ThemeColors } from "@/util";

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    dark: localStorage.getItem(LocalStorageKeys.darkMode) === "true",
    options: { customProperties: true },
    themes: {
      light: {
        primary: {
          base: ThemeColors.primary,
          lighten5: ThemeColors.backgroundLight,
        },
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
      dark: {
        primary: {
          base: ThemeColors.primaryDark,
          lighten5: ThemeColors.backgroundDark,
        },
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
});

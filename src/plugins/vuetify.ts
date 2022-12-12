import Vue from "vue";
import Vuetify from "vuetify/lib/framework";
import { ThemeColors } from "@/util";

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: {
          base: ThemeColors.primary,
          lighten5: ThemeColors.background,
        },
        secondary: ThemeColors.secondary,
        accent: ThemeColors.accent,
        info: ThemeColors.primary,
        warning: ThemeColors.warning,
        error: ThemeColors.error,
        success: ThemeColors.added,
      },
    },
  },
});

import iconSet from "quasar/icon-set/mdi-v4.js";
import "@quasar/extras/mdi-v4/mdi-v4.css";
import { LocalStorageKeys } from "@/types";
import { darkPalette, lightPalette } from "@/util";

// To be used on app.use(Quasar, { ... })
export default {
  config: {
    brand:
      localStorage.getItem(LocalStorageKeys.darkMode) === "true"
        ? darkPalette
        : lightPalette,
  },
  plugins: {},
  iconSet: iconSet,
};

import iconSet from "quasar/icon-set/mdi-v4.js";
import "@quasar/extras/mdi-v4/mdi-v4.css";
import { Notify } from "quasar";
import type { QuasarPluginOptions } from "quasar";
import { lightPalette } from "@/util";

const quasarOptions: Partial<QuasarPluginOptions> = {
  config: {
    brand: lightPalette,
    notify: {},
  },
  plugins: {
    Notify,
  },
  iconSet: iconSet,
};

// To be used on app.use(Quasar, { ... })
export default quasarOptions;

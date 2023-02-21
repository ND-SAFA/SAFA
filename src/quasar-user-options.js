import iconSet from "quasar/icon-set/mdi-v4.js";
import "@quasar/extras/mdi-v4/mdi-v4.css";
import { lightPalette } from "@/util";

// To be used on app.use(Quasar, { ... })
export default {
  config: {
    brand: lightPalette,
  },
  plugins: {},
  iconSet: iconSet,
};

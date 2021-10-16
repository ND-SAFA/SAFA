import {
  PRIMARY_COLOR,
  SECONDARY_COLOR,
  ACCENT_COLOR,
} from "@/cytoscape/styles/config/theme";
import Vue from "vue";
import Vuetify from "vuetify/lib/framework";

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: PRIMARY_COLOR,
        secondary: SECONDARY_COLOR,
        accent: ACCENT_COLOR,
      },
    },
  },
});

import { createApp } from "vue";

import "@/plugins/vue-cytoscape";
import "@mdi/font/css/materialdesignicons.css";

import { router } from "@/router";
import App from "@/App.vue";
import { vuetify, pinia } from "@/plugins";

export default createApp(App)
  .use(vuetify)
  .use(pinia)
  // .use(router)
  .mount("#app");

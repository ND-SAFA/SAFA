import { createApp } from "vue";

import "@mdi/font/css/materialdesignicons.css";
import "vue3-drr-grid-layout/dist/style.css";

import { Quasar } from "quasar";
import { router } from "@/router";
import { vuetify, pinia, gridLayout, codeDiff } from "@/plugins";
import App from "@/App.vue";
import quasarUserOptions from "./quasar-user-options";

const app = createApp(App);

app
  .use(vuetify)
  .use(pinia)
  .use(router)
  .use(gridLayout)
  .use(codeDiff)
  .use(Quasar, quasarUserOptions);

app.mount("#app");

export default app;

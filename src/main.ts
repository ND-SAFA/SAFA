import { createApp } from "vue";

import "@mdi/font/css/materialdesignicons.css";
import "vue3-drr-grid-layout/dist/style.css";
import "@quasar/quasar-ui-qmarkdown/dist/index.css";

import { Quasar } from "quasar";
import { default as QMarkdown } from "@quasar/quasar-ui-qmarkdown";
import { router } from "@/router";
import { pinia, gridLayout, codeDiff, quasarOptions } from "@/plugins";
import App from "@/App.vue";

const app = createApp(App);

app
  .use(pinia)
  .use(router)
  .use(gridLayout)
  .use(codeDiff)
  .use(Quasar, quasarOptions)
  .use(QMarkdown);

app.mount("#app");

export default app;

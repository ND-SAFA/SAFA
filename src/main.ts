import { createApp } from "vue";

import "@mdi/font/css/materialdesignicons.css";
import "vue3-drr-grid-layout/dist/style.css";

import { Quasar } from "quasar";
import VueHighlightJS from "vue3-highlightjs";
import Markdown from "vue3-markdown-it";
import { router } from "@/router";
import { pinia, gridLayout, codeDiff, quasarOptions } from "@/plugins";
import App from "@/App.vue";

const app = createApp(App);

app
  .use(pinia)
  .use(router)
  .use(gridLayout)
  .use(codeDiff)
  .use(VueHighlightJS)
  .use(Markdown)
  .use(Quasar, quasarOptions);

app.mount("#app");

export default app;

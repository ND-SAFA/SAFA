import { createApp } from "vue";

import "@mdi/font/css/materialdesignicons.css";
import "vue3-drr-grid-layout/dist/style.css";

import { router } from "@/router";
import { vuetify, pinia, gridLayout, codeDiff } from "@/plugins";
import App from "@/App.vue";

const app = createApp(App);

app.use(vuetify).use(pinia).use(router).use(gridLayout).use(codeDiff);

app.mount("#app");

export default app;

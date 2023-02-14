import { configureCompat, createApp } from "vue";

import "@mdi/font/css/materialdesignicons.css";

import { router } from "@/router";
import { vuetify, pinia } from "@/plugins";
import App from "@/App.vue";

configureCompat({
  COMPONENT_ASYNC: false,
  COMPONENT_V_MODEL: false,
});

const app = createApp(App);

app.use(vuetify).use(pinia).use(router).mount("#app");

export default app;

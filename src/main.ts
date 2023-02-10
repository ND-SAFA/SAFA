import { configureCompat, createApp } from "vue";

import "@/plugins/vue-cytoscape";
import "@mdi/font/css/materialdesignicons.css";

import { router } from "@/router";
import { vuetify, pinia } from "@/plugins";
import App from "@/App.vue";

configureCompat({
  COMPONENT_ASYNC: false,
  COMPONENT_V_MODEL: false,
  OPTIONS_DESTROYED: false,
  COMPONENT_FUNCTIONAL: false,
  INSTANCE_EVENT_HOOKS: false,
  INSTANCE_EVENT_EMITTER: false,
});

const app = createApp(App);

app.use(vuetify).use(pinia).use(router).mount("#app");

export default app;

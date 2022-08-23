import Vue from "vue";

import "@/plugins/vue-cytoscape";
import "@mdi/font/css/materialdesignicons.css";

import App from "@/App.vue";
import { router } from "@/router";
import { vuetify, pinia } from "@/plugins";

Vue.config.productionTip = false;

export default new Vue({
  router,
  vuetify,
  pinia,
  render: (h) => h(App),
}).$mount("#app");

import Vue from "vue";
import App from "@/App.vue";
import "@/plugins/vue-cytoscape";
import vuetify from "@/plugins/vuetify";
import "@/registerServiceWorker";
import router from "@/router";
import store from "@/store";
import "@mdi/font/css/materialdesignicons.css";

Vue.config.productionTip = false;

export default new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");

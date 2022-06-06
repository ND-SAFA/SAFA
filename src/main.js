"use strict";
exports.__esModule = true;
var vue_1 = require("vue");
var App_vue_1 = require("@/App.vue");
require("@/plugins/vue-cytoscape");
var vuetify_1 = require("@/plugins/vuetify");
var store_1 = require("@/store");
var router_1 = require("@/router");
require("@mdi/font/css/materialdesignicons.css");
vue_1["default"].config.productionTip = false;
exports["default"] = new vue_1["default"]({
    router: router_1.router,
    store: store_1["default"],
    vuetify: vuetify_1["default"],
    render: function (h) { return h(App_vue_1["default"]); }
}).$mount("#app");

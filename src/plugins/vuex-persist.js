"use strict";
exports.__esModule = true;
exports.vuexLocal = void 0;
var vuex_persist_1 = require("vuex-persist");
exports.vuexLocal = new vuex_persist_1["default"]({
    storage: window.localStorage,
    modules: ["session"]
});

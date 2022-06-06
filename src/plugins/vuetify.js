"use strict";
exports.__esModule = true;
var vue_1 = require("vue");
var framework_1 = require("vuetify/lib/framework");
var util_1 = require("@/util");
vue_1["default"].use(framework_1["default"]);
exports["default"] = new framework_1["default"]({
    theme: {
        themes: {
            light: {
                primary: util_1.ThemeColors.primary,
                secondary: util_1.ThemeColors.secondary,
                accent: util_1.ThemeColors.accent
            }
        }
    }
});

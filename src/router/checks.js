"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
exports.__esModule = true;
exports.routerChecks = void 0;
var types_1 = require("@/types");
var routes_1 = require("@/router/routes");
var store_1 = require("@/store");
var api_1 = require("@/api");
/**
 * Defines list of functions that are run before navigating to a new page.
 * This serves as the central location for setting any state a page might
 * expect to be in.
 *
 * Note, these checks are prioritized in the order they are defined meaning
 * that once a check has used the `next` function the remaining checks
 * are ignored.
 */
exports.routerChecks = {
    redirectToLoginIfNoSessionFound: function (to, from, next) {
        var _a;
        if (store_1.sessionModule.getDoesSessionExist || routes_1.routesPublic.includes(to.path)) {
            return;
        }
        next({
            path: routes_1.Routes.LOGIN_ACCOUNT,
            query: __assign(__assign({}, to.query), (_a = {}, _a[routes_1.QueryParams.LOGIN_PATH] = to.path, _a))
        });
    },
    requireProjectForRoutes: function (to, from, next) {
        if (store_1.projectModule.isProjectDefined ||
            !routes_1.routesWithRequiredProject.includes(to.path))
            return;
        store_1.logModule.onWarning("Please select a project.");
        next(routes_1.Routes.HOME);
    },
    closePanelsIfNotInGraph: function (to) {
        if (to.path === routes_1.Routes.ARTIFACT)
            return;
        store_1.appModule.closePanel(types_1.PanelType.left);
        store_1.appModule.closePanel(types_1.PanelType.right);
    },
    clearProjectIfOpenCreate: function (to) {
        if (to.path !== routes_1.Routes.PROJECT_CREATOR)
            return;
        api_1.handleClearProject();
    }
};

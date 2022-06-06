"use strict";
exports.__esModule = true;
exports.Routes = void 0;
var vue_1 = require("vue");
var vue_router_1 = require("vue-router");
var routes_1 = require("./routes");
exports.Routes = routes_1.Routes;
var views_1 = require("@/views");
var checks_1 = require("@/router/checks");
vue_1["default"].use(vue_router_1["default"]);
var routes = [
    {
        path: routes_1.Routes.LOGIN_ACCOUNT,
        name: "Login",
        component: views_1.LoginView
    },
    {
        path: routes_1.Routes.CREATE_ACCOUNT,
        name: "Create Account",
        component: views_1.CreateAccountView
    },
    {
        path: routes_1.Routes.FORGOT_PASSWORD,
        name: "Forgot Password",
        component: views_1.ForgotPasswordView
    },
    {
        path: routes_1.Routes.RESET_PASSWORD,
        name: "Reset Password",
        component: views_1.ResetPasswordView
    },
    {
        path: routes_1.Routes.HOME,
        name: "Home",
        component: views_1.ProjectCreatorView
    },
    {
        path: routes_1.Routes.ARTIFACT,
        name: "Project",
        component: views_1.ArtifactView
    },
    {
        path: routes_1.Routes.TRACE_LINK,
        name: "Trace Links",
        component: views_1.ApproveLinksView
    },
    {
        path: routes_1.Routes.PROJECT_CREATOR,
        name: "Project Creator",
        component: views_1.ProjectCreatorView
    },
    {
        path: routes_1.Routes.PROJECT_SETTINGS,
        name: "Project Settings",
        component: views_1.ProjectSettingsView
    },
    {
        path: routes_1.Routes.ERROR,
        name: "Error Page",
        component: views_1.ErrorPageView
    },
    {
        path: routes_1.Routes.UPLOAD_STATUS,
        name: "Upload Status",
        component: views_1.UploadStatusView
    },
];
var router = new vue_router_1["default"]({
    mode: "history",
    base: process.env.BASE_URL,
    routes: routes
});
/**
 * Iterates through each router checks and exits after the first check
 * uses the next function.
 */
router.beforeResolve(function (to, from, next) {
    var exit = false;
    for (var _i = 0, _a = Object.values(checks_1.routerChecks); _i < _a.length; _i++) {
        var check = _a[_i];
        if (exit)
            return;
        check(to, from, function (p) {
            next(p);
            exit = true;
        });
    }
    next();
});
exports["default"] = router;

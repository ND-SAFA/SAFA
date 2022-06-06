"use strict";
exports.__esModule = true;
exports.routesPublic = exports.routesWithRequiredProject = exports.QueryParams = exports.Routes = void 0;
/**
 * Enumerates the possible routes within the app.
 */
var Routes;
(function (Routes) {
    Routes["LOGIN_ACCOUNT"] = "/login";
    Routes["CREATE_ACCOUNT"] = "/create-account";
    Routes["FORGOT_PASSWORD"] = "/forgot";
    Routes["RESET_PASSWORD"] = "/reset";
    Routes["HOME"] = "/";
    Routes["ARTIFACT"] = "/project";
    Routes["PROJECT_SETTINGS"] = "/project/settings";
    Routes["TRACE_LINK"] = "/links";
    Routes["ERROR"] = "/error";
    Routes["PROJECT_CREATOR"] = "/create";
    Routes["UPLOAD_STATUS"] = "/uploads";
})(Routes = exports.Routes || (exports.Routes = {}));
/**
 * Enumerates query parameters used in the app.
 */
var QueryParams;
(function (QueryParams) {
    QueryParams["LOGIN_PATH"] = "to";
    QueryParams["TAB"] = "tab";
    QueryParams["VERSION"] = "version";
    QueryParams["JIRA_TOKEN"] = "code";
    QueryParams["GITHUB_TOKEN"] = "code";
})(QueryParams = exports.QueryParams || (exports.QueryParams = {}));
exports.routesWithRequiredProject = [
    Routes.TRACE_LINK,
    Routes.PROJECT_SETTINGS,
];
exports.routesPublic = [
    Routes.LOGIN_ACCOUNT,
    Routes.CREATE_ACCOUNT,
    Routes.FORGOT_PASSWORD,
    Routes.RESET_PASSWORD,
];

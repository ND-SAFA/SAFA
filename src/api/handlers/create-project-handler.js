"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
exports.__esModule = true;
exports.handleImportGitHubProject = exports.handleImportJiraProject = exports.handleBulkImportProject = exports.handleImportProject = void 0;
var router_1 = require("@/router");
var store_1 = require("@/store");
var api_1 = require("@/api");
/**
 * Creates a new project, sets related app state, and logs the status.
 *
 * @param project - The project to create.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
function handleImportProject(project, _a) {
    var _this = this;
    var onSuccess = _a.onSuccess, onError = _a.onError;
    store_1.appModule.onLoadStart();
    api_1.saveProject(project)
        .then(function (projectCreated) { return __awaiter(_this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    store_1.logModule.onSuccess("Project has been created: " + project.name);
                    return [4 /*yield*/, router_1.navigateTo(router_1.Routes.ARTIFACT)];
                case 1:
                    _a.sent();
                    return [4 /*yield*/, api_1.handleSetProject(projectCreated)];
                case 2:
                    _a.sent();
                    onSuccess === null || onSuccess === void 0 ? void 0 : onSuccess();
                    return [2 /*return*/];
            }
        });
    }); })["catch"](function (e) {
        store_1.logModule.onError("Unable to import project: " + project.name);
        store_1.logModule.onDevError(e);
        onError === null || onError === void 0 ? void 0 : onError(e);
    })["finally"](function () { return store_1.appModule.onLoadEnd(); });
}
exports.handleImportProject = handleImportProject;
/**
 * Creates a new project from files, sets related app state, and logs the status.
 *
 * @param project - The project to create.
 * @param files - The files to upload.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
function handleBulkImportProject(project, files, _a) {
    var _this = this;
    var onSuccess = _a.onSuccess, onError = _a.onError;
    store_1.appModule.onLoadStart();
    api_1.saveProject(project)
        .then(function (project) { return __awaiter(_this, void 0, void 0, function () {
        var _a;
        return __generator(this, function (_b) {
            return [2 /*return*/, api_1.handleUploadProjectVersion(project.projectId, ((_a = project.projectVersion) === null || _a === void 0 ? void 0 : _a.versionId) || "", files, true)];
        });
    }); })
        .then(onSuccess)["catch"](onError)["finally"](function () { return store_1.appModule.onLoadEnd(); });
}
exports.handleBulkImportProject = handleBulkImportProject;
/**
 * Imports a Jira project, sets related app state, and logs the status.
 *
 * @param cloudId - The Jira cloud id for this project.
 * @param projectId - The Jira project id to import.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
function handleImportJiraProject(cloudId, projectId, _a) {
    var _this = this;
    var onSuccess = _a.onSuccess, onError = _a.onError;
    store_1.appModule.onLoadStart();
    api_1.createJiraProject(cloudId, projectId)
        .then(function (job) { return __awaiter(_this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, api_1.handleJobSubmission(job)];
                case 1:
                    _a.sent();
                    store_1.logModule.onSuccess("Jira project has been created: " + projectId);
                    return [4 /*yield*/, router_1.navigateTo(router_1.Routes.UPLOAD_STATUS)];
                case 2:
                    _a.sent();
                    onSuccess === null || onSuccess === void 0 ? void 0 : onSuccess();
                    return [2 /*return*/];
            }
        });
    }); })["catch"](function (e) {
        store_1.logModule.onError("Unable to import jira project: " + projectId);
        store_1.logModule.onDevError(e.message);
        onError === null || onError === void 0 ? void 0 : onError(e);
    })["finally"](function () { return store_1.appModule.onLoadEnd(); });
}
exports.handleImportJiraProject = handleImportJiraProject;
/**
 * Imports a GitHub project, sets related app state, and logs the status.
 *
 * @param credentials - The access token received from authorizing GitHub.
 * @param orgId - The GitHub organization id for the current company.
 * @param projectId - The GitHub project id to import.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
function handleImportGitHubProject(
// eslint-disable-next-line @typescript-eslint/no-unused-vars
credentials, 
// eslint-disable-next-line @typescript-eslint/no-unused-vars
orgId, 
// eslint-disable-next-line @typescript-eslint/no-unused-vars
projectId, 
// eslint-disable-next-line @typescript-eslint/no-unused-vars
_a) {
    var onSuccess = _a.onSuccess, onError = _a.onError;
    store_1.logModule.onDevMessage("Importing from GitHub is not yet enabled.");
}
exports.handleImportGitHubProject = handleImportGitHubProject;

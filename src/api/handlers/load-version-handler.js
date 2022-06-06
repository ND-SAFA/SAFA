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
exports.handleReloadWarnings = exports.handleReloadTraceLinks = exports.handleReloadArtifacts = exports.handleLoadVersion = void 0;
var store_1 = require("@/store");
var router_1 = require("@/router");
var api_1 = require("@/api");
/**
 * Load the given project version of given Id. Navigates to the artifact
 * tree page in order to show the new project.
 *
 * @param versionId - The id of the version to retrieve and load.
 */
function handleLoadVersion(versionId) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            store_1.appModule.onLoadStart();
            return [2 /*return*/, router_1.navigateTo(router_1.Routes.ARTIFACT)
                    .then(function () { return api_1.getProjectVersion(versionId); })
                    .then(api_1.handleSetProject)["finally"](store_1.appModule.onLoadEnd)];
        });
    });
}
exports.handleLoadVersion = handleLoadVersion;
/**
 * Call this function whenever artifacts need to be re-downloaded.
 * Reloads project artifacts for the given version.
 *
 * @param versionId - The project version to load from.
 */
function handleReloadArtifacts(versionId) {
    return __awaiter(this, void 0, void 0, function () {
        var artifacts, currentArtifactCount;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, api_1.getArtifactsInVersion(versionId)];
                case 1:
                    artifacts = _a.sent();
                    currentArtifactCount = store_1.projectModule.getProject.artifacts.length;
                    return [4 /*yield*/, store_1.projectModule.addOrUpdateArtifacts(artifacts)];
                case 2:
                    _a.sent();
                    return [4 /*yield*/, api_1.handleLoadTraceMatrices()];
                case 3:
                    _a.sent();
                    if (!(artifacts.length > currentArtifactCount)) return [3 /*break*/, 5];
                    return [4 /*yield*/, store_1.viewportModule.setArtifactTreeLayout()];
                case 4:
                    _a.sent();
                    _a.label = 5;
                case 5: return [2 /*return*/];
            }
        });
    });
}
exports.handleReloadArtifacts = handleReloadArtifacts;
/**
 * Call this function whenever trace links need to be re-downloaded.
 * Reloads project traces for the given version.
 *
 * @param versionId - The project version to load from.
 */
function handleReloadTraceLinks(versionId) {
    return __awaiter(this, void 0, void 0, function () {
        var traces;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, api_1.getTracesInVersion(versionId)];
                case 1:
                    traces = _a.sent();
                    return [4 /*yield*/, store_1.projectModule.addOrUpdateTraceLinks(traces)];
                case 2:
                    _a.sent();
                    return [4 /*yield*/, api_1.handleLoadTraceMatrices()];
                case 3:
                    _a.sent();
                    store_1.viewportModule.applyAutomove();
                    return [2 /*return*/];
            }
        });
    });
}
exports.handleReloadTraceLinks = handleReloadTraceLinks;
/**
 * Call this function whenever warnings need to be re-downloaded.
 *
 * @param versionId - The project version to load from.
 */
function handleReloadWarnings(versionId) {
    return __awaiter(this, void 0, void 0, function () {
        var warnings;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, api_1.getWarningsInProjectVersion(versionId)];
                case 1:
                    warnings = _a.sent();
                    store_1.errorModule.setArtifactWarnings(warnings);
                    return [2 /*return*/];
            }
        });
    });
}
exports.handleReloadWarnings = handleReloadWarnings;

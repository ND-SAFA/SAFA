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
exports.handleReloadProject = exports.handleSetProject = exports.handleClearProject = exports.handleProjectSubscription = exports.handleResetGraph = void 0;
var util_1 = require("@/util");
var router_1 = require("@/router");
var store_1 = require("@/store");
var api_1 = require("@/api");
var cytoscape_1 = require("@/cytoscape");
var artifact_type_api_1 = require("@/api/endpoints/artifact-type-api");
/**
 * Resets graph state when some or all of a project gets reloaded.
 *
 * @param isDifferentProject - If true, all nodes will be unhidden and the viewport will be reset.
 */
function handleResetGraph(isDifferentProject) {
    if (isDifferentProject === void 0) { isDifferentProject = true; }
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    if (!isDifferentProject) return [3 /*break*/, 3];
                    return [4 /*yield*/, store_1.subtreeModule.resetHiddenNodes()];
                case 1:
                    _a.sent();
                    return [4 /*yield*/, store_1.viewportModule.setArtifactTreeLayout()];
                case 2:
                    _a.sent();
                    _a.label = 3;
                case 3:
                    cytoscape_1.disableDrawMode();
                    store_1.artifactSelectionModule.clearSelections();
                    store_1.deltaModule.clearDelta();
                    store_1.appModule.closeSidePanels();
                    return [2 /*return*/];
            }
        });
    });
}
exports.handleResetGraph = handleResetGraph;
/**
 1. Sets a new project.
 2. Subscribes to the new project's version.
 3. Clears any deltas to previous projects and their settings.
 *
 * @param project - The project to set.
 */
function handleProjectSubscription(project) {
    var _a;
    return __awaiter(this, void 0, void 0, function () {
        var projectId, versionId, isDifferentProject, _b;
        return __generator(this, function (_c) {
            switch (_c.label) {
                case 0:
                    projectId = project.projectId;
                    versionId = ((_a = project.projectVersion) === null || _a === void 0 ? void 0 : _a.versionId) || "";
                    isDifferentProject = store_1.projectModule.versionId !== versionId;
                    _b = project;
                    return [4 /*yield*/, artifact_type_api_1.getProjectArtifactTypes(projectId)];
                case 1:
                    _b.artifactTypes = _c.sent();
                    return [4 /*yield*/, api_1.handleSelectVersion(projectId, versionId)];
                case 2:
                    _c.sent();
                    return [4 /*yield*/, store_1.projectModule.initializeProject(project)];
                case 3:
                    _c.sent();
                    return [4 /*yield*/, handleResetGraph(isDifferentProject)];
                case 4:
                    _c.sent();
                    return [4 /*yield*/, api_1.handleLoadTraceMatrices()];
                case 5:
                    _c.sent();
                    return [4 /*yield*/, router_1.updateParam(router_1.QueryParams.VERSION, versionId)];
                case 6:
                    _c.sent();
                    return [2 /*return*/];
            }
        });
    });
}
exports.handleProjectSubscription = handleProjectSubscription;
/**
 * Clears project store data.
 */
function handleClearProject() {
    return __awaiter(this, void 0, void 0, function () {
        var project;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    project = util_1.createProject();
                    return [4 /*yield*/, store_1.projectModule.initializeProject(project)];
                case 1:
                    _a.sent();
                    return [4 /*yield*/, handleResetGraph()];
                case 2:
                    _a.sent();
                    store_1.typeOptionsModule.clearData();
                    return [4 /*yield*/, store_1.subtreeModule.clearSubtrees()];
                case 3:
                    _a.sent();
                    return [2 /*return*/];
            }
        });
    });
}
exports.handleClearProject = handleClearProject;
/**
 * Sets a newly created project.
 *
 * @param project - Project created containing entities.
 */
function handleSetProject(project) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, handleProjectSubscription(project)];
                case 1:
                    _a.sent();
                    store_1.errorModule.setArtifactWarnings(project.warnings);
                    return [4 /*yield*/, setCurrentDocument(project)];
                case 2:
                    _a.sent();
                    return [2 /*return*/];
            }
        });
    });
}
exports.handleSetProject = handleSetProject;
/**
 * Reloads the current project.
 */
function handleReloadProject() {
    return __awaiter(this, void 0, void 0, function () {
        var document;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    document = store_1.documentModule.document;
                    return [4 /*yield*/, api_1.handleLoadVersion(store_1.projectModule.versionId)];
                case 1:
                    _a.sent();
                    return [4 /*yield*/, store_1.documentModule.switchDocuments(document)];
                case 2:
                    _a.sent();
                    return [2 /*return*/];
            }
        });
    });
}
exports.handleReloadProject = handleReloadProject;
/**
 * Moves user to the document if one is set by currentDocumentId
 * Otherwise default document would continue to be in view.
 * @param project The project possibly containing a currentDocumentId
 */
function setCurrentDocument(project) {
    return __awaiter(this, void 0, void 0, function () {
        var document_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    if (!project.currentDocumentId) return [3 /*break*/, 2];
                    document_1 = util_1.getSingleQueryResult(project.documents.filter(function (d) { return d.documentId === project.currentDocumentId; }), "documents");
                    return [4 /*yield*/, store_1.documentModule.switchDocuments(document_1)];
                case 1:
                    _a.sent();
                    _a.label = 2;
                case 2: return [2 /*return*/];
            }
        });
    });
}

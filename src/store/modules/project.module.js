"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
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
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
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
var __spreadArrays = (this && this.__spreadArrays) || function () {
    for (var s = 0, i = 0, il = arguments.length; i < il; i++) s += arguments[i].length;
    for (var r = Array(s), k = 0, i = 0; i < il; i++)
        for (var a = arguments[i], j = 0, jl = a.length; j < jl; j++, k++)
            r[k] = a[j];
    return r;
};
exports.__esModule = true;
var vuex_module_decorators_1 = require("vuex-module-decorators");
var util_1 = require("@/util");
var store_1 = require("@/store");
var api_1 = require("@/api");
var ProjectModule = /** @class */ (function (_super) {
    __extends(ProjectModule, _super);
    /**
     * This module tracks the currently loaded project.
     */
    function ProjectModule() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * The currently loaded project.
         */
        _this.project = util_1.createProject();
        return _this;
    }
    ProjectModule.prototype.initializeProject = function (project) {
        return __awaiter(this, void 0, void 0, function () {
            var _this = this;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.SAVE_PROJECT(project);
                        store_1.documentModule.initializeProject(project);
                        store_1.typeOptionsModule.initializeTypeIcons(project.artifactTypes);
                        return [4 /*yield*/, setTimeout(function () { return __awaiter(_this, void 0, void 0, function () {
                                return __generator(this, function (_a) {
                                    switch (_a.label) {
                                        case 0: 
                                        // Not sure why this needs any wait, but it doesnt work without it.
                                        return [4 /*yield*/, store_1.subtreeModule.initializeProject(project)];
                                        case 1:
                                            // Not sure why this needs any wait, but it doesnt work without it.
                                            _a.sent();
                                            return [2 /*return*/];
                                    }
                                });
                            }); }, 100)];
                    case 1:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    ProjectModule.prototype.addOrUpdateArtifacts = function (newArtifacts) {
        return __awaiter(this, void 0, void 0, function () {
            var newIds, updatedArtifacts;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        newIds = newArtifacts.map(function (_a) {
                            var id = _a.id;
                            return id;
                        });
                        updatedArtifacts = __spreadArrays(this.project.artifacts.filter(function (_a) {
                            var id = _a.id;
                            return !newIds.includes(id);
                        }), newArtifacts);
                        this.SET_ARTIFACTS(updatedArtifacts);
                        return [4 /*yield*/, api_1.handleDocumentReload()];
                    case 1:
                        _a.sent();
                        return [4 /*yield*/, store_1.artifactModule.addOrUpdateArtifacts(updatedArtifacts)];
                    case 2:
                        _a.sent();
                        return [4 /*yield*/, store_1.subtreeModule.updateSubtreeMap()];
                    case 3:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    ProjectModule.prototype.deleteArtifacts = function (artifacts) {
        return __awaiter(this, void 0, void 0, function () {
            var deletedNames;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (artifacts.length === 0)
                            return [2 /*return*/];
                        deletedNames = artifacts.map(function (_a) {
                            var name = _a.name;
                            return name;
                        });
                        this.SET_ARTIFACTS(this.project.artifacts.filter(function (_a) {
                            var name = _a.name;
                            return !deletedNames.includes(name);
                        }));
                        return [4 /*yield*/, store_1.artifactModule.deleteArtifacts(artifacts)];
                    case 1:
                        _a.sent();
                        return [4 /*yield*/, store_1.subtreeModule.updateSubtreeMap()];
                    case 2:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    ProjectModule.prototype.addOrUpdateTraceLinks = function (newTraces) {
        return __awaiter(this, void 0, void 0, function () {
            var newIds, updatedTraces;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        newIds = newTraces.map(function (_a) {
                            var traceLinkId = _a.traceLinkId;
                            return traceLinkId;
                        });
                        updatedTraces = __spreadArrays(this.project.traces.filter(function (_a) {
                            var traceLinkId = _a.traceLinkId;
                            return !newIds.includes(traceLinkId);
                        }), newTraces);
                        this.SET_TRACES(updatedTraces);
                        return [4 /*yield*/, store_1.traceModule.addOrUpdateTraceLinks(updatedTraces)];
                    case 1:
                        _a.sent();
                        return [4 /*yield*/, store_1.subtreeModule.updateSubtreeMap()];
                    case 2:
                        _a.sent();
                        store_1.viewportModule.applyAutomove();
                        return [2 /*return*/];
                }
            });
        });
    };
    ProjectModule.prototype.deleteTraceLinks = function (traceLinks) {
        return __awaiter(this, void 0, void 0, function () {
            var deletedIds;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (traceLinks.length === 0)
                            return [2 /*return*/];
                        deletedIds = traceLinks.map(function (_a) {
                            var traceLinkId = _a.traceLinkId;
                            return traceLinkId;
                        });
                        this.SET_TRACES(this.project.traces.filter(function (_a) {
                            var traceLinkId = _a.traceLinkId;
                            return !deletedIds.includes(traceLinkId);
                        }));
                        return [4 /*yield*/, store_1.traceModule.deleteTraceLinks(traceLinks)];
                    case 1:
                        _a.sent();
                        return [4 /*yield*/, store_1.subtreeModule.updateSubtreeMap()];
                    case 2:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    /**
     * Adds a new artifact type.
     *
     * @param artifactType - The artifact type to add.
     */
    ProjectModule.prototype.addOrUpdateArtifactType = function (artifactType) {
        var unaffectedTypes = this.project.artifactTypes.filter(function (a) { return a.typeId !== artifactType.typeId; });
        var allArtifactTypes = __spreadArrays(unaffectedTypes, [artifactType]);
        this.SET_ARTIFACT_TYPES(allArtifactTypes);
        store_1.typeOptionsModule.SET_TYPES(allArtifactTypes);
    };
    /**
     * Updates the project identifier.
     *
     * @param project - The new project to track.
     */
    ProjectModule.prototype.SET_PROJECT_IDENTIFIER = function (project) {
        this.project = __assign(__assign({}, this.project), { name: project.name, description: project.description });
    };
    /**
     * Sets a new project.
     *
     * @param project - The new project to track.
     */
    ProjectModule.prototype.SAVE_PROJECT = function (project) {
        this.project = project;
    };
    /**
     * Sets the members of current project.
     */
    ProjectModule.prototype.SET_MEMBERS = function (members) {
        this.project.members = members;
    };
    /**
     * Sets the current artifacts in the project.
     */
    ProjectModule.prototype.SET_ARTIFACTS = function (artifacts) {
        this.project.artifacts = artifacts;
    };
    /**
     * Sets the current trace links in the project.
     */
    ProjectModule.prototype.SET_TRACES = function (traces) {
        this.project.traces = traces;
    };
    /**
     * Sets the current documents in the project.
     */
    ProjectModule.prototype.SET_DOCUMENTS = function (documents) {
        this.project.documents = documents;
    };
    /**
     * Sets the current artifact type in the project.
     */
    ProjectModule.prototype.SET_ARTIFACT_TYPES = function (artifactTypes) {
        this.project.artifactTypes = artifactTypes;
    };
    Object.defineProperty(ProjectModule.prototype, "getProject", {
        /**
         * @return The current project.
         */
        get: function () {
            return this.project;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectModule.prototype, "projectId", {
        /**
         * @return The current project id.
         */
        get: function () {
            return this.project.projectId;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectModule.prototype, "versionId", {
        /**
         * @return The current version id.
         */
        get: function () {
            var _a;
            return ((_a = this.project.projectVersion) === null || _a === void 0 ? void 0 : _a.versionId) || "";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectModule.prototype, "versionIdWithLog", {
        /**
         * Returns the version ID, and logs an error if there isn't one.
         *
         * @return The current version id.
         */
        get: function () {
            if (!this.versionId) {
                store_1.logModule.onWarning("Please select a project version.");
                return "";
            }
            return this.versionId;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectModule.prototype, "isProjectDefined", {
        /**
         * @returns Whether project is defined.
         */
        get: function () {
            return this.project.projectId !== "";
        },
        enumerable: false,
        configurable: true
    });
    __decorate([
        vuex_module_decorators_1.Action
    ], ProjectModule.prototype, "initializeProject");
    __decorate([
        vuex_module_decorators_1.Action
    ], ProjectModule.prototype, "addOrUpdateArtifacts");
    __decorate([
        vuex_module_decorators_1.Action
    ], ProjectModule.prototype, "deleteArtifacts");
    __decorate([
        vuex_module_decorators_1.Action
    ], ProjectModule.prototype, "addOrUpdateTraceLinks");
    __decorate([
        vuex_module_decorators_1.Action
    ], ProjectModule.prototype, "deleteTraceLinks");
    __decorate([
        vuex_module_decorators_1.Action
    ], ProjectModule.prototype, "addOrUpdateArtifactType");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ProjectModule.prototype, "SET_PROJECT_IDENTIFIER");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ProjectModule.prototype, "SAVE_PROJECT");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ProjectModule.prototype, "SET_MEMBERS");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ProjectModule.prototype, "SET_ARTIFACTS");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ProjectModule.prototype, "SET_TRACES");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ProjectModule.prototype, "SET_DOCUMENTS");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ProjectModule.prototype, "SET_ARTIFACT_TYPES");
    ProjectModule = __decorate([
        vuex_module_decorators_1.Module({ namespaced: true, name: "project" })
        /**
         * This module tracks the currently loaded project.
         */
    ], ProjectModule);
    return ProjectModule;
}(vuex_module_decorators_1.VuexModule));
exports["default"] = ProjectModule;

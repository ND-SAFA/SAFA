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
exports.__esModule = true;
var vuex_module_decorators_1 = require("vuex-module-decorators");
var util_1 = require("@/util");
var store_1 = require("@/store");
var ArtifactModule = /** @class */ (function (_super) {
    __extends(ArtifactModule, _super);
    /**
     * This module defines the state of the currently visible artifacts.
     */
    function ArtifactModule() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * All artifacts in the project.
         */
        _this.projectArtifacts = [];
        /**
         * The currently visible artifacts.
         */
        _this.currentArtifacts = [];
        return _this;
    }
    /**
     * Initializes the artifacts visible in the current document.
     */
    ArtifactModule.prototype.initializeArtifacts = function (documentArtifacts) {
        var _a = documentArtifacts.artifacts, artifacts = _a === void 0 ? this.projectArtifacts : _a, currentArtifactIds = documentArtifacts.currentArtifactIds;
        this.SET_PROJECT_ARTIFACTS(artifacts);
        this.SET_CURRENT_ARTIFACTS(currentArtifactIds
            ? artifacts.filter(function (_a) {
                var id = _a.id;
                return currentArtifactIds.includes(id);
            })
            : artifacts);
    };
    ArtifactModule.prototype.addOrUpdateArtifacts = function (updatedArtifacts) {
        return __awaiter(this, void 0, void 0, function () {
            var visibleIds, visibleArtifacts, selectedArtifact, query;
            return __generator(this, function (_a) {
                visibleIds = store_1.documentModule.document.artifactIds;
                visibleArtifacts = updatedArtifacts.filter(function (_a) {
                    var id = _a.id;
                    return visibleIds.includes(id);
                });
                this.SET_PROJECT_ARTIFACTS(updatedArtifacts);
                this.SET_CURRENT_ARTIFACTS(visibleArtifacts);
                selectedArtifact = store_1.artifactSelectionModule.getSelectedArtifact;
                if (selectedArtifact !== undefined) {
                    query = updatedArtifacts.filter(function (_a) {
                        var name = _a.name;
                        return name === selectedArtifact.name;
                    });
                    if (query.length > 0) {
                        store_1.artifactSelectionModule.selectArtifact(query[0].id);
                    }
                }
                return [2 /*return*/];
            });
        });
    };
    ArtifactModule.prototype.deleteArtifacts = function (artifacts) {
        return __awaiter(this, void 0, void 0, function () {
            var deletedNames, removeArtifact;
            return __generator(this, function (_a) {
                deletedNames = artifacts.map(function (_a) {
                    var name = _a.name;
                    return name;
                });
                removeArtifact = function (currentArtifacts) {
                    return currentArtifacts.filter(function (_a) {
                        var name = _a.name;
                        return !deletedNames.includes(name);
                    });
                };
                this.SET_PROJECT_ARTIFACTS(removeArtifact(this.projectArtifacts));
                this.SET_CURRENT_ARTIFACTS(removeArtifact(this.currentArtifacts));
                return [2 /*return*/];
            });
        });
    };
    /**
     * Sets the project artifacts.
     */
    ArtifactModule.prototype.SET_PROJECT_ARTIFACTS = function (artifacts) {
        this.projectArtifacts = artifacts;
    };
    /**
     * Sets the current artifacts.
     */
    ArtifactModule.prototype.SET_CURRENT_ARTIFACTS = function (artifacts) {
        this.currentArtifacts = artifacts;
    };
    Object.defineProperty(ArtifactModule.prototype, "allArtifacts", {
        /**
         * @return All artifacts in the project.
         */
        get: function () {
            return this.projectArtifacts;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ArtifactModule.prototype, "artifacts", {
        /**
         * @return The artifacts for the current document.
         */
        get: function () {
            return this.currentArtifacts;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ArtifactModule.prototype, "flatArtifacts", {
        /**
         * @return The flattened artifacts for the current document.
         */
        get: function () {
            return this.currentArtifacts.map(function (artifact) {
                return (__assign(__assign({}, artifact), artifact.customFields));
            });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ArtifactModule.prototype, "getArtifactByName", {
        /**
         * @return A function for finding an artifact by name.
         * @throws If more or less than 1 artifact is found to match.
         */
        get: function () {
            var _this = this;
            return function (artifactName) {
                var query = _this.artifacts.filter(function (a) { return a.name === artifactName; });
                return util_1.getSingleQueryResult(query, "Find by name: " + artifactName);
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ArtifactModule.prototype, "getArtifactById", {
        /**
         * @return A function for finding an artifact by id.
         * @throws If more or less than 1 artifact is found to match.
         */
        get: function () {
            var _this = this;
            return function (targetArtifactId) {
                var query = _this.allArtifacts.filter(function (a) { return a.id === targetArtifactId; });
                return util_1.getSingleQueryResult(query, "Find by id: " + targetArtifactId);
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ArtifactModule.prototype, "getArtifactsById", {
        /**
         * @return A collection of artifacts, keyed by their id.
         */
        get: function () {
            return this.artifacts
                .map(function (artifact) {
                var _a;
                return (_a = {}, _a[artifact.id] = artifact, _a);
            })
                .reduce(function (acc, cur) { return (__assign(__assign({}, acc), cur)); }, {});
        },
        enumerable: false,
        configurable: true
    });
    __decorate([
        vuex_module_decorators_1.Action
    ], ArtifactModule.prototype, "initializeArtifacts");
    __decorate([
        vuex_module_decorators_1.Action
    ], ArtifactModule.prototype, "addOrUpdateArtifacts");
    __decorate([
        vuex_module_decorators_1.Action
    ], ArtifactModule.prototype, "deleteArtifacts");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ArtifactModule.prototype, "SET_PROJECT_ARTIFACTS");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ArtifactModule.prototype, "SET_CURRENT_ARTIFACTS");
    ArtifactModule = __decorate([
        vuex_module_decorators_1.Module({ namespaced: true, name: "artifact" })
        /**
         * This module defines the state of the currently visible artifacts.
         */
    ], ArtifactModule);
    return ArtifactModule;
}(vuex_module_decorators_1.VuexModule));
exports["default"] = ArtifactModule;

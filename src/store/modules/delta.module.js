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
var types_1 = require("@/types");
var util_1 = require("@/util");
var cytoscape_1 = require("@/cytoscape");
var store_1 = require("@/store");
var ErrorModule = /** @class */ (function (_super) {
    __extends(ErrorModule, _super);
    /**
     * This module defines state variables for tracking artifact deltas.
     */
    function ErrorModule() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Whether the artifact delta view is currently enabled.
         */
        _this.isDeltaViewEnabled = false;
        /**
         * A collection of all added artifacts.
         */
        _this.projectDelta = util_1.createProjectDelta();
        return _this;
    }
    /**
     * Sets whether the delta view is enabled.
     *
     * @param isDeltaViewEnabled - Whether to enable this view.
     */
    ErrorModule.prototype.setIsDeltaViewEnabled = function (isDeltaViewEnabled) {
        this.SET_DELTA_IN_VIEW(isDeltaViewEnabled);
        if (isDeltaViewEnabled) {
            cytoscape_1.disableDrawMode();
        }
    };
    ErrorModule.prototype.setDeltaPayload = function (payload) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.removeDeltaAdditions()];
                    case 1:
                        _a.sent();
                        this.SET_DELTA_PAYLOAD(payload);
                        return [4 /*yield*/, store_1.projectModule.addOrUpdateArtifacts(__spreadArrays(Object.values(payload.artifacts.added), Object.values(payload.artifacts.removed)))];
                    case 2:
                        _a.sent();
                        return [4 /*yield*/, store_1.projectModule.addOrUpdateTraceLinks(__spreadArrays(Object.values(payload.traces.added), Object.values(payload.traces.removed)))];
                    case 3:
                        _a.sent();
                        return [4 /*yield*/, store_1.subtreeModule.restoreHiddenNodesAfter(store_1.viewportModule.setArtifactTreeLayout)];
                    case 4:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    /**
     * Sets the version that deltas are made to.
     *
     * @param version - The new version.
     */
    ErrorModule.prototype.setAfterVersion = function (version) {
        this.SET_AFTER_VERSION(version);
    };
    /**
     * Clears the current collections of artifact deltas.
     */
    ErrorModule.prototype.clearDelta = function () {
        this.SET_DELTA_PAYLOAD(util_1.createProjectDelta());
        this.SET_DELTA_IN_VIEW(false);
        this.setIsDeltaViewEnabled(false);
        store_1.appModule.closePanel(types_1.PanelType.right);
    };
    ErrorModule.prototype.removeDeltaAdditions = function () {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, store_1.projectModule.deleteArtifacts(Object.values(this.addedArtifacts))];
                    case 1:
                        _a.sent();
                        return [4 /*yield*/, store_1.projectModule.deleteTraceLinks(Object.values(this.addedTraces))];
                    case 2:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    /**
     * Sets whether the delta view is enabled.
     *
     * @param deltaInView - Whether to enable this view.
     */
    ErrorModule.prototype.SET_DELTA_IN_VIEW = function (deltaInView) {
        this.isDeltaViewEnabled = deltaInView;
    };
    /**
     * Sets the current artifact deltas.
     *
     * @param projectDelta - The collections of artifact and trace deltas.
     */
    ErrorModule.prototype.SET_DELTA_PAYLOAD = function (projectDelta) {
        this.projectDelta = projectDelta;
    };
    /**
     * Sets the current version to apply deltas to.
     *
     * @param afterVersion - The new version.
     */
    ErrorModule.prototype.SET_AFTER_VERSION = function (afterVersion) {
        this.afterVersion = afterVersion;
    };
    Object.defineProperty(ErrorModule.prototype, "addedArtifacts", {
        /**
         * @return A mapping of artifact IDs and the artifacts added.
         */
        get: function () {
            return this.projectDelta.artifacts.added;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ErrorModule.prototype, "removedArtifacts", {
        /**
         * @return A mapping of artifact IDs and the artifacts removed.
         */
        get: function () {
            return this.projectDelta.artifacts.removed;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ErrorModule.prototype, "modifiedArtifacts", {
        /**
         * @return A collection of modified deltas.
         */
        get: function () {
            return this.projectDelta.artifacts.modified;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ErrorModule.prototype, "addedTraces", {
        /**
         * @return A mapping of trace IDs and the traces added.
         */
        get: function () {
            return this.projectDelta.traces.added;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ErrorModule.prototype, "removedTraces", {
        /**
         * @return A mapping of trace IDs and the traces removed.
         */
        get: function () {
            return this.projectDelta.traces.removed;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ErrorModule.prototype, "deltaVersion", {
        /**
         * @return The current version that deltas are made to.
         */
        get: function () {
            return this.afterVersion;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ErrorModule.prototype, "inDeltaView", {
        /**
         * @return Whether the delta view is currently enabled.
         */
        get: function () {
            return this.isDeltaViewEnabled;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ErrorModule.prototype, "getDeltaStatesByArtifactNames", {
        /**
         * @return All delta states that associated with the artifacts given artifact names.
         */
        get: function () {
            var _this = this;
            return function (names) {
                var deltaStates = new Set();
                for (var _i = 0, names_1 = names; _i < names_1.length; _i++) {
                    var name_1 = names_1[_i];
                    if (name_1 in _this.projectDelta.artifacts.added) {
                        deltaStates.add(types_1.ArtifactDeltaState.ADDED);
                    }
                    else if (name_1 in _this.projectDelta.artifacts.modified) {
                        deltaStates.add(types_1.ArtifactDeltaState.MODIFIED);
                    }
                    else if (name_1 in _this.projectDelta.artifacts.removed) {
                        deltaStates.add(types_1.ArtifactDeltaState.REMOVED);
                    }
                }
                return Array.from(deltaStates);
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ErrorModule.prototype, "getTraceDeltaType", {
        /**
         * @return The delta state of the given trace link id.
         */
        get: function () {
            var _this = this;
            return function (id) {
                if (!_this.inDeltaView) {
                    return undefined;
                }
                else if (id in _this.projectDelta.traces.added) {
                    return types_1.ArtifactDeltaState.ADDED;
                }
                else if (id in _this.projectDelta.traces.modified) {
                    return types_1.ArtifactDeltaState.MODIFIED;
                }
                else if (id in _this.projectDelta.traces.removed) {
                    return types_1.ArtifactDeltaState.REMOVED;
                }
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ErrorModule.prototype, "getArtifactDeltaType", {
        /**
         * @return The delta state of the given artifacts id.
         */
        get: function () {
            var _this = this;
            return function (id) {
                if (!_this.inDeltaView) {
                    return types_1.ArtifactDeltaState.NO_CHANGE;
                }
                else if (id in _this.projectDelta.artifacts.added) {
                    return types_1.ArtifactDeltaState.ADDED;
                }
                else if (id in _this.projectDelta.artifacts.modified) {
                    return types_1.ArtifactDeltaState.MODIFIED;
                }
                else if (id in _this.projectDelta.artifacts.removed) {
                    return types_1.ArtifactDeltaState.REMOVED;
                }
                else {
                    return types_1.ArtifactDeltaState.NO_CHANGE;
                }
            };
        },
        enumerable: false,
        configurable: true
    });
    __decorate([
        vuex_module_decorators_1.Action
    ], ErrorModule.prototype, "setIsDeltaViewEnabled");
    __decorate([
        vuex_module_decorators_1.Action
    ], ErrorModule.prototype, "setDeltaPayload");
    __decorate([
        vuex_module_decorators_1.Action
    ], ErrorModule.prototype, "setAfterVersion");
    __decorate([
        vuex_module_decorators_1.Action
    ], ErrorModule.prototype, "clearDelta");
    __decorate([
        vuex_module_decorators_1.Action
    ], ErrorModule.prototype, "removeDeltaAdditions");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ErrorModule.prototype, "SET_DELTA_IN_VIEW");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ErrorModule.prototype, "SET_DELTA_PAYLOAD");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], ErrorModule.prototype, "SET_AFTER_VERSION");
    ErrorModule = __decorate([
        vuex_module_decorators_1.Module({ namespaced: true, name: "delta" })
        /**
         * This module defines state variables for tracking artifact deltas.
         */
    ], ErrorModule);
    return ErrorModule;
}(vuex_module_decorators_1.VuexModule));
exports["default"] = ErrorModule;

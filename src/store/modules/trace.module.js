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
exports.__esModule = true;
var vuex_module_decorators_1 = require("vuex-module-decorators");
var types_1 = require("@/types");
var store_1 = require("@/store");
var util_1 = require("@/util");
var TraceModule = /** @class */ (function (_super) {
    __extends(TraceModule, _super);
    /**
     * This module defines the state of the currently visible trace links.
     */
    function TraceModule() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * All trace links in the project.
         */
        _this.projectTraces = [];
        /**
         * The trace links visible artifacts.
         */
        _this.currentTraces = [];
        return _this;
    }
    /**
     * Initializes the trace links visible in the current document.
     */
    TraceModule.prototype.initializeTraces = function (documentTraces) {
        var _a = documentTraces.traces, traces = _a === void 0 ? this.projectTraces : _a, currentArtifactIds = documentTraces.currentArtifactIds;
        this.SET_PROJECT_TRACES(traces);
        this.SET_CURRENT_TRACES(currentArtifactIds
            ? traces.filter(function (_a) {
                var sourceId = _a.sourceId, targetId = _a.targetId;
                return currentArtifactIds.includes(sourceId) &&
                    currentArtifactIds.includes(targetId);
            })
            : traces);
    };
    TraceModule.prototype.addOrUpdateTraceLinks = function (updatedTraces) {
        return __awaiter(this, void 0, void 0, function () {
            var visibleIds, visibleTraces;
            return __generator(this, function (_a) {
                visibleIds = store_1.documentModule.document.artifactIds;
                visibleTraces = updatedTraces.filter(function (_a) {
                    var sourceId = _a.sourceId, targetId = _a.targetId;
                    return visibleIds.includes(sourceId) && visibleIds.includes(targetId);
                });
                this.SET_PROJECT_TRACES(updatedTraces);
                this.SET_CURRENT_TRACES(visibleTraces);
                return [2 /*return*/];
            });
        });
    };
    TraceModule.prototype.deleteTraceLinks = function (traceLinks) {
        return __awaiter(this, void 0, void 0, function () {
            var deletedIds, removeLink;
            return __generator(this, function (_a) {
                deletedIds = traceLinks.map(function (_a) {
                    var traceLinkId = _a.traceLinkId;
                    return traceLinkId;
                });
                removeLink = function (currentTraces) {
                    return currentTraces.filter(function (_a) {
                        var traceLinkId = _a.traceLinkId;
                        return !deletedIds.includes(traceLinkId);
                    });
                };
                this.SET_PROJECT_TRACES(removeLink(this.projectTraces));
                this.SET_CURRENT_TRACES(removeLink(this.currentTraces));
                return [2 /*return*/];
            });
        });
    };
    /**
     * Sets the project trace links.
     */
    TraceModule.prototype.SET_PROJECT_TRACES = function (traces) {
        this.projectTraces = traces;
    };
    /**
     * Sets the current trace links.
     */
    TraceModule.prototype.SET_CURRENT_TRACES = function (traces) {
        this.currentTraces = traces;
    };
    Object.defineProperty(TraceModule.prototype, "allTraces", {
        /**
         * @return All trace links in the project.
         */
        get: function () {
            return this.projectTraces;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(TraceModule.prototype, "traces", {
        /**
         * @return The trace links for the current document.
         */
        get: function () {
            return this.currentTraces;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(TraceModule.prototype, "nonDeclinedTraces", {
        /**
         * @return All non-declined trace links.
         */
        get: function () {
            return this.currentTraces.filter(function (t) { return t.approvalStatus != types_1.TraceApproval.DECLINED; });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(TraceModule.prototype, "getTraceLinkByArtifacts", {
        /**
         * @return Returns a function to query a single trace link by the
         * source and target artifact ids.
         */
        get: function () {
            var _this = this;
            return function (sourceId, targetId) {
                var traceQuery = _this.allTraces.filter(function (trace) { return trace.sourceId === sourceId && trace.targetId === targetId; });
                if (traceQuery.length === 0) {
                    throw Error("Could not find trace link with id: " + util_1.getTraceId(sourceId, targetId));
                }
                return traceQuery[0];
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(TraceModule.prototype, "doesLinkExist", {
        /**
         * @return A function that determines whether a link with the given source and target IDs exists.
         */
        get: function () {
            var _this = this;
            return function (sourceId, targetId) {
                var traceLinkQuery = _this.traces.filter(function (trace) {
                    return (trace.sourceId === sourceId && trace.targetId === targetId) ||
                        (trace.targetId === sourceId && trace.sourceId === targetId);
                });
                return traceLinkQuery.length > 0;
            };
        },
        enumerable: false,
        configurable: true
    });
    __decorate([
        vuex_module_decorators_1.Action
    ], TraceModule.prototype, "initializeTraces");
    __decorate([
        vuex_module_decorators_1.Action
    ], TraceModule.prototype, "addOrUpdateTraceLinks");
    __decorate([
        vuex_module_decorators_1.Action
    ], TraceModule.prototype, "deleteTraceLinks");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], TraceModule.prototype, "SET_PROJECT_TRACES");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], TraceModule.prototype, "SET_CURRENT_TRACES");
    TraceModule = __decorate([
        vuex_module_decorators_1.Module({ namespaced: true, name: "trace" })
        /**
         * This module defines the state of the currently visible trace links.
         */
    ], TraceModule);
    return TraceModule;
}(vuex_module_decorators_1.VuexModule));
exports["default"] = TraceModule;

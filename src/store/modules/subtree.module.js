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
var store_1 = require("@/store");
var cytoscape_1 = require("@/cytoscape");
var types_1 = require("@/types");
var SubtreeModule = /** @class */ (function (_super) {
    __extends(SubtreeModule, _super);
    /**
     * This module defines the functions used to hide and show subtrees.
     */
    function SubtreeModule() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * A map containing root artifact names as keys and children names are values.
         */
        _this.subtreeMap = {};
        /**
         * List of phantom links used when hiding subtrees.
         */
        _this.subtreeLinks = [];
        /**
         * List of nodes currently hidden within subtrees
         */
        _this.hiddenSubtreeNodes = [];
        /**
         * List of nodes whose children are currently hidden.
         */
        _this.collapsedParentNodes = [];
        return _this;
    }
    SubtreeModule.prototype.updateSubtreeMap = function (artifacts) {
        if (artifacts === void 0) { artifacts = store_1.artifactModule.allArtifacts; }
        return __awaiter(this, void 0, void 0, function () {
            var _this = this;
            return __generator(this, function (_a) {
                cytoscape_1.artifactTreeCyPromise.then(function (cy) { return __awaiter(_this, void 0, void 0, function () {
                    var subtreeMap;
                    return __generator(this, function (_a) {
                        switch (_a.label) {
                            case 0: return [4 /*yield*/, cytoscape_1.createSubtreeMap(cy, artifacts)];
                            case 1:
                                subtreeMap = _a.sent();
                                this.SET_SUBTREE_MAP(subtreeMap);
                                return [2 /*return*/];
                        }
                    });
                }); });
                return [2 /*return*/];
            });
        });
    };
    SubtreeModule.prototype.resetHiddenNodes = function () {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                this.SET_COLLAPSED_PARENT_NODES([]);
                this.SET_HIDDEN_SUBTREE_NODES([]);
                cytoscape_1.cyDisplayAll();
                return [2 /*return*/];
            });
        });
    };
    SubtreeModule.prototype.clearSubtrees = function () {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.SET_SUBTREE_MAP({});
                        this.SET_SUBTREE_LINKS([]);
                        return [4 /*yield*/, this.resetHiddenNodes()];
                    case 1:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    SubtreeModule.prototype.restoreHiddenNodesAfter = function (cb) {
        return __awaiter(this, void 0, void 0, function () {
            var collapsedParents, _i, collapsedParents_1, id;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        collapsedParents = this.collapsedParentNodes;
                        return [4 /*yield*/, this.resetHiddenNodes()];
                    case 1:
                        _a.sent();
                        return [4 /*yield*/, cb()];
                    case 2:
                        _a.sent();
                        _i = 0, collapsedParents_1 = collapsedParents;
                        _a.label = 3;
                    case 3:
                        if (!(_i < collapsedParents_1.length)) return [3 /*break*/, 6];
                        id = collapsedParents_1[_i];
                        if (this.hiddenSubtreeNodes.includes(id))
                            return [3 /*break*/, 5];
                        return [4 /*yield*/, this.hideSubtree(id)];
                    case 4:
                        _a.sent();
                        _a.label = 5;
                    case 5:
                        _i++;
                        return [3 /*break*/, 3];
                    case 6: return [2 /*return*/];
                }
            });
        });
    };
    SubtreeModule.prototype.initializeProject = function (project) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.updateSubtreeMap(project.artifacts)];
                    case 1:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    SubtreeModule.prototype.hideSubtree = function (rootId) {
        return __awaiter(this, void 0, void 0, function () {
            var childrenInSubtree, nodesInSubtree, visibleChildren, _i, childrenInSubtree_1, childId, newSubtreeLinks;
            var _this = this;
            return __generator(this, function (_a) {
                childrenInSubtree = this.getSubtreeByArtifactId(rootId);
                nodesInSubtree = __spreadArrays(childrenInSubtree, [rootId]);
                visibleChildren = childrenInSubtree.filter(function (id) { return !_this.hiddenSubtreeNodes.includes(id); });
                for (_i = 0, childrenInSubtree_1 = childrenInSubtree; _i < childrenInSubtree_1.length; _i++) {
                    childId = childrenInSubtree_1[_i];
                    newSubtreeLinks = this.createSubtreeLinks(nodesInSubtree, rootId, childId);
                    this.SET_SUBTREE_LINKS(newSubtreeLinks);
                }
                this.SET_HIDDEN_SUBTREE_NODES(__spreadArrays(this.hiddenSubtreeNodes, visibleChildren));
                this.SET_COLLAPSED_PARENT_NODES(__spreadArrays(this.collapsedParentNodes, [rootId]));
                cytoscape_1.cySetDisplay(visibleChildren, false);
                return [2 /*return*/];
            });
        });
    };
    SubtreeModule.prototype.showSubtree = function (rootId) {
        return __awaiter(this, void 0, void 0, function () {
            var subtreeNodes, hiddenNodes;
            return __generator(this, function (_a) {
                subtreeNodes = this.getSubtreeByArtifactId(rootId);
                hiddenNodes = this.hiddenSubtreeNodes.filter(function (n) { return !subtreeNodes.includes(n); });
                this.SET_HIDDEN_SUBTREE_NODES(hiddenNodes);
                this.SET_COLLAPSED_PARENT_NODES(this.collapsedParentNodes.filter(function (n) { return n !== rootId; }));
                this.SET_SUBTREE_LINKS(this.subtreeLinks.filter(function (link) {
                    return link.rootNode !== rootId &&
                        // Make sure that phantom links created by other parent nodes are removed.
                        (hiddenNodes.includes(link.sourceId) ||
                            hiddenNodes.includes(link.targetId));
                }));
                cytoscape_1.cySetDisplay(subtreeNodes, true);
                return [2 /*return*/];
            });
        });
    };
    /**
     * Sets current subtree map.
     *
     * @param subtreeMap The map of all the subtrees in project.
     */
    SubtreeModule.prototype.SET_SUBTREE_MAP = function (subtreeMap) {
        this.subtreeMap = subtreeMap;
    };
    /**
     * Sets the current subtree links.
     *
     * @param subtreeLinks The list of phantom links used for hiding subtrees.
     */
    SubtreeModule.prototype.SET_SUBTREE_LINKS = function (subtreeLinks) {
        this.subtreeLinks = subtreeLinks;
    };
    /**
     * Sets the current nodes hidden by subtrees.
     *
     * @param hiddenSubtreeNodes The list of nodes currently being hidden in a subtree.
     */
    SubtreeModule.prototype.SET_HIDDEN_SUBTREE_NODES = function (hiddenSubtreeNodes) {
        this.hiddenSubtreeNodes = hiddenSubtreeNodes;
    };
    /**
     * Sets the current nodes with hidden subtrees.
     *
     * @param collapsedParentNodes The list of nodes currently having their children hidden.
     */
    SubtreeModule.prototype.SET_COLLAPSED_PARENT_NODES = function (collapsedParentNodes) {
        this.collapsedParentNodes = collapsedParentNodes;
    };
    Object.defineProperty(SubtreeModule.prototype, "getSubtreeMap", {
        /**
          * A map between a root node id and it's children.
      \   */
        get: function () {
            return this.subtreeMap;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SubtreeModule.prototype, "getSubtreeByArtifactId", {
        /**
         * @returns the pre-computed artifacts in the subtree of root specified.
         */
        get: function () {
            var _this = this;
            return function (artifactId) { return _this.getSubtreeMap[artifactId] || []; };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SubtreeModule.prototype, "getSubtreeLinks", {
        /**
         * @returns list of phantom links used for hiding subtrees.
         */
        get: function () {
            return this.subtreeLinks;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SubtreeModule.prototype, "getHiddenSubtreeIds", {
        /**
         * @returns list of artifact ids currently hidden in a subtree.
         */
        get: function () {
            return this.hiddenSubtreeNodes;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SubtreeModule.prototype, "createSubtreeLinks", {
        /**
         * TODO: this is very inefficient.
         * @returns a constructor for creating phantom links from artifacts.
         */
        get: function () {
            var _this = this;
            return function (nodesInSubtree, rootId, childId) {
                var traces = store_1.traceModule.traces;
                var subtreeLinkIds = _this.subtreeLinks.map(function (_a) {
                    var traceLinkId = _a.traceLinkId;
                    return traceLinkId;
                });
                var subtreeLinkCreator = function (isIncoming) {
                    return traces
                        .filter(function (link) {
                        var value = isIncoming ? link.targetId : link.sourceId;
                        var oppoValue = isIncoming ? link.sourceId : link.targetId;
                        var doesNotExist = !subtreeLinkIds.includes(link.traceLinkId + "-phantom");
                        return (doesNotExist &&
                            value === childId &&
                            !nodesInSubtree.includes(oppoValue));
                    })
                        .map(function (link) {
                        var base = __assign(__assign({}, link), { traceLinkId: link.traceLinkId + "-phantom", type: types_1.InternalTraceType.SUBTREE, rootNode: rootId });
                        return isIncoming
                            ? __assign(__assign({}, base), { target: rootId }) : __assign(__assign({}, base), { source: rootId });
                    });
                };
                var incomingPhantom = subtreeLinkCreator(true);
                var outgoingPhantom = subtreeLinkCreator(false);
                return __spreadArrays(_this.subtreeLinks, incomingPhantom, outgoingPhantom);
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SubtreeModule.prototype, "getHiddenChildrenByParentId", {
        /**
         * @return The ids of all hidden children below the given node.
         */
        get: function () {
            var _this = this;
            return function (parentId) {
                var childNodes = _this.getSubtreeByArtifactId(parentId);
                var hiddenNodes = _this.getHiddenSubtreeIds;
                return childNodes.filter(function (id) { return hiddenNodes.includes(id); });
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SubtreeModule.prototype, "getCollapsedParentNodes", {
        /**
         * @return Ids of the parent whose children are collapsed.
         * Used for toggling Show/Hide subtree menu items.
         */
        get: function () {
            return this.collapsedParentNodes;
        },
        enumerable: false,
        configurable: true
    });
    __decorate([
        vuex_module_decorators_1.Action
    ], SubtreeModule.prototype, "updateSubtreeMap");
    __decorate([
        vuex_module_decorators_1.Action
    ], SubtreeModule.prototype, "resetHiddenNodes");
    __decorate([
        vuex_module_decorators_1.Action
    ], SubtreeModule.prototype, "clearSubtrees");
    __decorate([
        vuex_module_decorators_1.Action
    ], SubtreeModule.prototype, "restoreHiddenNodesAfter");
    __decorate([
        vuex_module_decorators_1.Action
    ], SubtreeModule.prototype, "initializeProject");
    __decorate([
        vuex_module_decorators_1.Action
    ], SubtreeModule.prototype, "hideSubtree");
    __decorate([
        vuex_module_decorators_1.Action
    ], SubtreeModule.prototype, "showSubtree");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], SubtreeModule.prototype, "SET_SUBTREE_MAP");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], SubtreeModule.prototype, "SET_SUBTREE_LINKS");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], SubtreeModule.prototype, "SET_HIDDEN_SUBTREE_NODES");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], SubtreeModule.prototype, "SET_COLLAPSED_PARENT_NODES");
    SubtreeModule = __decorate([
        vuex_module_decorators_1.Module({ namespaced: true, name: "subtree" })
        /**
         * This module defines the functions used to hide and show subtrees.
         */
    ], SubtreeModule);
    return SubtreeModule;
}(vuex_module_decorators_1.VuexModule));
exports["default"] = SubtreeModule;

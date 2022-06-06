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
var CommitModule = /** @class */ (function (_super) {
    __extends(CommitModule, _super);
    /**
     * Keep track of the commits occurring in this session. Provides api for:
     * 1. Committing an action.
     * 2. Undoing an action.
     */
    function CommitModule() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * The ordered tuples of commits (and its revert) that have occurred
         * during the current session.
         */
        _this.commits = [];
        _this.revertedCommits = [];
        return _this;
    }
    CommitModule.prototype.saveCommit = function (commit) {
        return __awaiter(this, void 0, void 0, function () {
            var revert;
            return __generator(this, function (_a) {
                revert = this.getRevert(commit);
                this.ADD_COMMIT({ commit: commit, revert: revert });
                return [2 /*return*/];
            });
        });
    };
    /**
     * Removes the last commit from the store and attempts to revert the changes.
     * If successful, the commit is stored in previously reverted commits.
     *
     * @return The undone commit.
     */
    CommitModule.prototype.undoLastCommit = function () {
        if (!this.canUndo) {
            var errorMessage = "There are no commits to undo.";
            store_1.logModule.onWarning(errorMessage);
            throw Error(errorMessage);
        }
        var lastCommitIndex = this.commits.length - 1;
        var lastCommitHistory = this.commits[lastCommitIndex];
        this.SET_COMMITS(this.commits.filter(function (c, i) { return i !== lastCommitIndex; }));
        this.ADD_REVERTED_COMMIT(lastCommitHistory);
        return lastCommitHistory.revert;
    };
    /**
     * Removes and returns the last reverted commit.
     *
     * @return The redone commit.
     */
    CommitModule.prototype.redoLastUndoneCommit = function () {
        if (!this.canRedo) {
            var errorMessage = "Cannot redo because no commits have been reverted.";
            store_1.logModule.onWarning(errorMessage);
            throw Error(errorMessage);
        }
        var lastCommitIndex = this.revertedCommits.length - 1;
        var lastCommitHistory = this.revertedCommits[lastCommitIndex];
        this.SET_REVERTED_COMMITS(this.revertedCommits.filter(function (c, i) { return i !== lastCommitIndex; }));
        return lastCommitHistory.commit;
    };
    /**
     * Sets given list as commits.
     * @param commits
     */
    CommitModule.prototype.SET_COMMITS = function (commits) {
        this.commits = commits;
    };
    /**
     * Sets given list as reverted commits
     */
    CommitModule.prototype.SET_REVERTED_COMMITS = function (revertedCommits) {
        this.revertedCommits = revertedCommits;
    };
    /**
     * Adds a commit to the commit history
     */
    CommitModule.prototype.ADD_COMMIT = function (commitHistory) {
        this.commits = __spreadArrays(this.commits, [commitHistory]);
    };
    /**
     * Adds a commit to the commit history
     */
    CommitModule.prototype.ADD_REVERTED_COMMIT = function (commitHistory) {
        this.revertedCommits = __spreadArrays(this.revertedCommits, [commitHistory]);
    };
    Object.defineProperty(CommitModule.prototype, "getRevert", {
        /**
         * Given a commit, all added entities are deleted, all deleted entities are
         * re-added, and modified entities are reverted to their state before the last
         * client change.
         */
        get: function () {
            return function (commit) {
                var originalArtifacts = commit.artifacts.modified.map(function (a) { return store_1.artifactModule.getArtifactById(a.id); });
                var originalTraces = commit.traces.modified.map(function (t) {
                    return store_1.traceModule.getTraceLinkByArtifacts(t.sourceId, t.targetId);
                });
                return __assign(__assign({}, util_1.createCommit(commit.commitVersion)), { artifacts: {
                        added: commit.artifacts.removed,
                        removed: commit.artifacts.added,
                        modified: originalArtifacts
                    }, traces: {
                        added: commit.traces.removed,
                        removed: commit.traces.added,
                        modified: originalTraces
                    } });
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(CommitModule.prototype, "canUndo", {
        /**
         * @return True if at least one commit exists.
         */
        get: function () {
            return this.commits.length > 0;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(CommitModule.prototype, "canRedo", {
        /**
         * @return True if at least one commit has been reverted.
         */
        get: function () {
            return this.revertedCommits.length > 0;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(CommitModule.prototype, "getCommits", {
        /**
         * @return The current commits.
         */
        get: function () {
            return this.commits;
        },
        enumerable: false,
        configurable: true
    });
    __decorate([
        vuex_module_decorators_1.Action({ rawError: true })
    ], CommitModule.prototype, "saveCommit");
    __decorate([
        vuex_module_decorators_1.Action
    ], CommitModule.prototype, "undoLastCommit");
    __decorate([
        vuex_module_decorators_1.Action
    ], CommitModule.prototype, "redoLastUndoneCommit");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], CommitModule.prototype, "SET_COMMITS");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], CommitModule.prototype, "SET_REVERTED_COMMITS");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], CommitModule.prototype, "ADD_COMMIT");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], CommitModule.prototype, "ADD_REVERTED_COMMIT");
    CommitModule = __decorate([
        vuex_module_decorators_1.Module({ namespaced: true, name: "commit" })
        /**
         * Keep track of the commits occurring in this session. Provides api for:
         * 1. Committing an action.
         * 2. Undoing an action.
         */
    ], CommitModule);
    return CommitModule;
}(vuex_module_decorators_1.VuexModule));
exports["default"] = CommitModule;

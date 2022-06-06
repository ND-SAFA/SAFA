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
var util_1 = require("@/util");
var store_1 = require("@/store");
var api_1 = require("@/api");
var DocumentModule = /** @class */ (function (_super) {
    __extends(DocumentModule, _super);
    /**
     * This module defines the state of the currently visible document within a project.
     */
    function DocumentModule() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Whether the document is currently in table view.
         */
        _this.isTableView = false;
        /**
         * The currently visible document.
         */
        _this.currentDocument = util_1.createDocument();
        /**
         * The base document with all artifacts.
         */
        _this.baseDocument = util_1.createDocument();
        /**
         * All project documents.
         */
        _this.allDocuments = [_this.currentDocument];
        return _this;
    }
    /**
     * Initializes the current artifacts and traces visible in the current document.
     */
    DocumentModule.prototype.initializeProject = function (project) {
        var artifacts = project.artifacts, traces = project.traces, _a = project.currentDocumentId, currentDocumentId = _a === void 0 ? this.currentDocument.documentId : _a, _b = project.documents, documents = _b === void 0 ? [] : _b;
        var defaultDocument = util_1.createDocument({
            project: project,
            artifactIds: artifacts.map(function (_a) {
                var id = _a.id;
                return id;
            })
        });
        var loadedDocument = documents.find(function (_a) {
            var documentId = _a.documentId;
            return documentId === currentDocumentId;
        });
        this.SET_ALL_DOCUMENTS(documents);
        this.SET_BASE_DOCUMENT(defaultDocument);
        if (loadedDocument) {
            var currentArtifactIds = loadedDocument.artifactIds;
            this.SET_CURRENT_DOCUMENT(loadedDocument);
            store_1.artifactModule.initializeArtifacts({ artifacts: artifacts, currentArtifactIds: currentArtifactIds });
            store_1.traceModule.initializeTraces({ traces: traces, currentArtifactIds: currentArtifactIds });
        }
        else {
            this.SET_CURRENT_DOCUMENT(defaultDocument);
            store_1.artifactModule.initializeArtifacts({ artifacts: artifacts });
            store_1.traceModule.initializeTraces({ traces: traces });
        }
    };
    DocumentModule.prototype.updateDocuments = function (updatedDocuments) {
        return __awaiter(this, void 0, void 0, function () {
            var updatedDocumentIds, newDocuments, updatedCurrentDocument;
            var _this = this;
            return __generator(this, function (_a) {
                updatedDocumentIds = updatedDocuments.map(function (d) { return d.documentId; });
                newDocuments = __spreadArrays(this.allDocuments.filter(function (_a) {
                    var documentId = _a.documentId;
                    return !updatedDocumentIds.includes(documentId);
                }), updatedDocuments);
                this.SET_ALL_DOCUMENTS(newDocuments);
                if (updatedDocumentIds.includes(this.currentDocument.documentId)) {
                    updatedCurrentDocument = updatedDocuments.filter(function (_a) {
                        var documentId = _a.documentId;
                        return documentId === _this.currentDocument.documentId;
                    })[0];
                    this.SET_CURRENT_DOCUMENT(updatedCurrentDocument);
                }
                return [2 /*return*/];
            });
        });
    };
    DocumentModule.prototype.switchDocuments = function (document) {
        return __awaiter(this, void 0, void 0, function () {
            var currentArtifactIds, _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        currentArtifactIds = document.artifactIds;
                        this.SET_CURRENT_DOCUMENT(document);
                        if (!(document.documentId === "")) return [3 /*break*/, 2];
                        return [4 /*yield*/, api_1.clearCurrentDocument()];
                    case 1:
                        _a = _b.sent();
                        return [3 /*break*/, 4];
                    case 2: return [4 /*yield*/, api_1.setCurrentDocument(document.documentId)];
                    case 3:
                        _a = _b.sent();
                        _b.label = 4;
                    case 4:
                        _a;
                        store_1.artifactModule.initializeArtifacts({ currentArtifactIds: currentArtifactIds });
                        store_1.traceModule.initializeTraces({ currentArtifactIds: currentArtifactIds });
                        return [4 /*yield*/, api_1.handleResetGraph()];
                    case 5:
                        _b.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    DocumentModule.prototype.addDocument = function (document) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.SET_ALL_DOCUMENTS(__spreadArrays(this.allDocuments, [document]));
                        return [4 /*yield*/, this.switchDocuments(document)];
                    case 1:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    DocumentModule.prototype.removeDocument = function (document) {
        return __awaiter(this, void 0, void 0, function () {
            var remainingDocuments;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        remainingDocuments = this.allDocuments.filter(function (_a) {
                            var documentId = _a.documentId;
                            return documentId !== document.documentId;
                        });
                        this.SET_ALL_DOCUMENTS(remainingDocuments);
                        if (!(this.currentDocument.documentId === document.documentId)) return [3 /*break*/, 2];
                        return [4 /*yield*/, this.switchDocuments(remainingDocuments[0] || this.baseDocument)];
                    case 1:
                        _a.sent();
                        _a.label = 2;
                    case 2: return [2 /*return*/];
                }
            });
        });
    };
    /**
     * Toggles whether the current document is in table view.
     */
    DocumentModule.prototype.toggleTableView = function () {
        this.SET_TABLE_VIEW(!this.isTableView);
    };
    /**
     * Sets the current document.
     */
    DocumentModule.prototype.SET_ALL_DOCUMENTS = function (documents) {
        this.allDocuments = documents;
    };
    /**
     * Sets the current document.
     */
    DocumentModule.prototype.SET_CURRENT_DOCUMENT = function (document) {
        this.currentDocument = document;
    };
    /**
     * Sets the current document.
     */
    DocumentModule.prototype.SET_BASE_DOCUMENT = function (document) {
        this.baseDocument = document;
    };
    /**
     * Sets whether the document is in table view.
     */
    DocumentModule.prototype.SET_TABLE_VIEW = function (isTableView) {
        this.isTableView = isTableView;
    };
    Object.defineProperty(DocumentModule.prototype, "projectDocuments", {
        /**
         * @return The current document.
         */
        get: function () {
            return __spreadArrays(this.allDocuments, [this.baseDocument]);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DocumentModule.prototype, "document", {
        /**
         * @return The current document.
         */
        get: function () {
            return this.currentDocument;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DocumentModule.prototype, "type", {
        /**
         * @return The current document.
         */
        get: function () {
            return this.currentDocument.type;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DocumentModule.prototype, "defaultDocument", {
        /**
         * @return The default document.
         */
        get: function () {
            return this.baseDocument;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DocumentModule.prototype, "doesDocumentExist", {
        /**
         * Returns whether the given document name already exists.
         */
        get: function () {
            var _this = this;
            return function (newName) {
                return !!_this.projectDocuments.find(function (_a) {
                    var name = _a.name;
                    return name === newName;
                });
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DocumentModule.prototype, "isTableDocument", {
        /**
         * Returns whether the current document type is for rendering a table.
         */
        get: function () {
            return this.isTableView || util_1.isTableDocument(this.currentDocument.type);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DocumentModule.prototype, "tableColumns", {
        /**
         * Returns the column definitions for a table document.
         */
        get: function () {
            return (this.isTableDocument && this.currentDocument.columns) || [];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DocumentModule.prototype, "doesColumnExist", {
        /**
         * Returns whether the given column name already exists.
         */
        get: function () {
            var _this = this;
            return function (newName) {
                return !!_this.tableColumns.find(function (_a) {
                    var name = _a.name;
                    return name === newName;
                });
            };
        },
        enumerable: false,
        configurable: true
    });
    __decorate([
        vuex_module_decorators_1.Action
    ], DocumentModule.prototype, "initializeProject");
    __decorate([
        vuex_module_decorators_1.Action
    ], DocumentModule.prototype, "updateDocuments");
    __decorate([
        vuex_module_decorators_1.Action
    ], DocumentModule.prototype, "switchDocuments");
    __decorate([
        vuex_module_decorators_1.Action
    ], DocumentModule.prototype, "addDocument");
    __decorate([
        vuex_module_decorators_1.Action
    ], DocumentModule.prototype, "removeDocument");
    __decorate([
        vuex_module_decorators_1.Action
    ], DocumentModule.prototype, "toggleTableView");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], DocumentModule.prototype, "SET_ALL_DOCUMENTS");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], DocumentModule.prototype, "SET_CURRENT_DOCUMENT");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], DocumentModule.prototype, "SET_BASE_DOCUMENT");
    __decorate([
        vuex_module_decorators_1.Mutation
    ], DocumentModule.prototype, "SET_TABLE_VIEW");
    DocumentModule = __decorate([
        vuex_module_decorators_1.Module({ namespaced: true, name: "document" })
        /**
         * This module defines the state of the currently visible document within a project.
         */
    ], DocumentModule);
    return DocumentModule;
}(vuex_module_decorators_1.VuexModule));
exports["default"] = DocumentModule;

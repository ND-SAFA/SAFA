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
var __spreadArrays = (this && this.__spreadArrays) || function () {
    for (var s = 0, i = 0, il = arguments.length; i < il; i++) s += arguments[i].length;
    for (var r = Array(s), k = 0, i = 0; i < il; i++)
        for (var a = arguments[i], j = 0, jl = a.length; j < jl; j++, k++)
            r[k] = a[j];
    return r;
};
exports.__esModule = true;
exports.handleColumnDelete = exports.handleColumnSave = exports.handleColumnMove = exports.handleSaveDocument = exports.handleDocumentReload = exports.handleDeleteDocument = exports.handleUpdateDocument = exports.handleCreateDocument = void 0;
var util_1 = require("@/util");
var store_1 = require("@/store");
var api_1 = require("@/api");
/**
 * Creates a new document and updates app state.
 *
 * @param name - The document name create.
 * @param type - The document type create.
 * @param artifactIds - The artifacts shown in the document.
 */
function handleCreateDocument(name, type, artifactIds) {
    return __awaiter(this, void 0, void 0, function () {
        var versionId, createdDocument;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    versionId = store_1.projectModule.versionIdWithLog;
                    return [4 /*yield*/, api_1.saveDocument(versionId, util_1.createDocument({
                            project: store_1.projectModule.getProject,
                            artifactIds: artifactIds,
                            name: name,
                            type: type
                        }))];
                case 1:
                    createdDocument = _a.sent();
                    return [4 /*yield*/, store_1.documentModule.addDocument(createdDocument)];
                case 2:
                    _a.sent();
                    return [2 /*return*/];
            }
        });
    });
}
exports.handleCreateDocument = handleCreateDocument;
/**
 * Updates an existing document and updates app state.
 *
 * @param document - The document to edit.
 */
function handleUpdateDocument(document) {
    return __awaiter(this, void 0, void 0, function () {
        var versionId, updatedDocument;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    versionId = store_1.projectModule.versionIdWithLog;
                    return [4 /*yield*/, api_1.saveDocument(versionId, document)];
                case 1:
                    updatedDocument = _a.sent();
                    return [4 /*yield*/, store_1.documentModule.updateDocuments([updatedDocument])];
                case 2:
                    _a.sent();
                    if (store_1.documentModule.document.documentId !== updatedDocument.documentId)
                        return [2 /*return*/];
                    return [4 /*yield*/, store_1.documentModule.switchDocuments(updatedDocument)];
                case 3:
                    _a.sent();
                    return [2 /*return*/];
            }
        });
    });
}
exports.handleUpdateDocument = handleUpdateDocument;
/**
 * Deletes the document and updates app state.
 * Switches documents if the current one has been deleted.
 *
 * @param document - The document to delete.
 * @param onSuccess - Called if the operation is successful.
 * @param onError - Called if the operation fails.
 */
function handleDeleteDocument(document, _a) {
    var _this = this;
    var onSuccess = _a.onSuccess, onError = _a.onError;
    var name = document.name;
    api_1.deleteDocument(document)
        .then(function () { return __awaiter(_this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, store_1.documentModule.removeDocument(document)];
                case 1:
                    _a.sent();
                    store_1.logModule.onSuccess("Document has been deleted: " + name);
                    onSuccess === null || onSuccess === void 0 ? void 0 : onSuccess();
                    return [2 /*return*/];
            }
        });
    }); })["catch"](function (e) {
        store_1.logModule.onError("Unable to delete document: " + name);
        store_1.logModule.onDevError(e);
        onError === null || onError === void 0 ? void 0 : onError(e);
    });
}
exports.handleDeleteDocument = handleDeleteDocument;
/**
 * Updates the artifact for the all documents.
 *
 * @param projectId - The project to load documents for.
 * @param artifacts - The full list of artifacts.
 */
function handleDocumentReload(projectId, artifacts) {
    if (projectId === void 0) { projectId = store_1.projectModule.projectId; }
    if (artifacts === void 0) { artifacts = store_1.projectModule.getProject.artifacts; }
    return __awaiter(this, void 0, void 0, function () {
        var documents;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, api_1.getDocuments(projectId)];
                case 1:
                    documents = _a.sent();
                    return [4 /*yield*/, store_1.documentModule.updateDocuments(documents)];
                case 2:
                    _a.sent();
                    store_1.documentModule.defaultDocument.artifactIds = artifacts.map(function (_a) {
                        var id = _a.id;
                        return id;
                    });
                    return [2 /*return*/];
            }
        });
    });
}
exports.handleDocumentReload = handleDocumentReload;
/**
 * Creates or updates a document, updates app state, and logs the result.
 *
 * @param document - The document to save.
 * @param isUpdate - Set to true if the document already exists.
 * @param includedChildTypes - The types of child artifacts to include for
 * all parent artifacts attached to this document.
 * @param onSuccess - Called if the operation is successful.
 * @param onError - Called if the operation fails.
 */
function handleSaveDocument(document, isUpdate, includedChildTypes, _a) {
    var _b;
    var onSuccess = _a.onSuccess, onError = _a.onError;
    var name = document.name, type = document.type, artifactIds = document.artifactIds;
    if (includedChildTypes.length > 0) {
        // Add all child artifacts of the artifacts in the document that match the given types.
        var childArtifactIds_1 = new Set();
        document.artifactIds.forEach(function (parentId) {
            store_1.subtreeModule.getSubtreeMap[parentId].forEach(function (childId) {
                var artifact = store_1.artifactModule.getArtifactById(childId);
                if (!includedChildTypes.includes(artifact.type))
                    return;
                childArtifactIds_1.add(childId);
            });
        });
        (_b = document.artifactIds).push.apply(_b, Array.from(childArtifactIds_1));
    }
    if (isUpdate) {
        handleUpdateDocument(document)
            .then(function () {
            store_1.logModule.onSuccess("Document has been edited: " + name);
            onSuccess === null || onSuccess === void 0 ? void 0 : onSuccess();
        })["catch"](function (e) {
            store_1.logModule.onError("Unable to edit document: " + name);
            store_1.logModule.onDevError(e);
            onError === null || onError === void 0 ? void 0 : onError(e);
        });
    }
    else {
        handleCreateDocument(name, type, artifactIds)
            .then(function () {
            store_1.logModule.onSuccess("Document has been created: " + name);
            onSuccess === null || onSuccess === void 0 ? void 0 : onSuccess();
        })["catch"](function (e) {
            store_1.logModule.onError("Unable to create document: " + name);
            store_1.logModule.onDevError(e);
            onError === null || onError === void 0 ? void 0 : onError(e);
        });
    }
}
exports.handleSaveDocument = handleSaveDocument;
/**
 * Changes the order of two columns.
 *
 * @param column - The column to move.
 * @param moveUp - Whether to move the column up or down.
 * @param onSuccess - Called if the operation is successful.
 * @param onError - Called if the operation fails.
 */
function handleColumnMove(column, moveUp, _a) {
    var _b;
    var onSuccess = _a.onSuccess, onError = _a.onError;
    var document = store_1.documentModule.document;
    var currentIndex = (document.columns || []).indexOf(column);
    var swapIndex = moveUp ? currentIndex - 1 : currentIndex + 1;
    var columns = document.columns || [];
    _b = [
        columns[swapIndex],
        columns[currentIndex],
    ], columns[currentIndex] = _b[0], columns[swapIndex] = _b[1];
    document.columns = __spreadArrays(columns);
    handleUpdateDocument(document)
        .then(function () {
        store_1.logModule.onSuccess("Column order has been updated.");
        onSuccess === null || onSuccess === void 0 ? void 0 : onSuccess(document.columns || []);
    })["catch"](function (e) {
        store_1.logModule.onError("Unable to update column order.");
        store_1.logModule.onDevWarning(e);
        onError === null || onError === void 0 ? void 0 : onError(e);
    });
}
exports.handleColumnMove = handleColumnMove;
/**
 * Creates or updates a column.
 *
 * @param column - The column to save.
 * @param isEditMode - If false, this column will be added to the current document.
 * @param onSuccess - Called if the operation is successful.
 * @param onError - Called if the operation fails.
 */
function handleColumnSave(column, isEditMode, _a) {
    var onSuccess = _a.onSuccess, onError = _a.onError;
    var document = store_1.documentModule.document;
    var columnId = column.id, name = column.name;
    if (!isEditMode) {
        document.columns = __spreadArrays((document.columns || []), [column]);
    }
    else if (document.columns) {
        var index = document.columns.findIndex(function (_a) {
            var id = _a.id;
            return id === columnId;
        });
        document.columns[index] = column;
    }
    handleUpdateDocument(document)
        .then(function () {
        store_1.logModule.onSuccess("Column has been updated: " + name);
        onSuccess === null || onSuccess === void 0 ? void 0 : onSuccess();
    })["catch"](function (e) {
        store_1.logModule.onError("Unable to update column: " + name);
        store_1.logModule.onDevError(e);
        onError === null || onError === void 0 ? void 0 : onError(e);
    });
}
exports.handleColumnSave = handleColumnSave;
/**
 * Deletes a column.
 *
 * @param column - The column to delete.
 * @param onSuccess - Called if the operation is successful.
 * @param onError - Called if the operation fails.
 */
function handleColumnDelete(column, _a) {
    var onSuccess = _a.onSuccess, onError = _a.onError;
    var document = store_1.documentModule.document;
    var columnId = column.id, name = column.name;
    document.columns = (document.columns || []).filter(function (_a) {
        var id = _a.id;
        return id !== columnId;
    });
    handleUpdateDocument(document)
        .then(function () {
        store_1.logModule.onSuccess("Column has ben deleted: " + name);
        onSuccess === null || onSuccess === void 0 ? void 0 : onSuccess();
    })["catch"](function (e) {
        store_1.logModule.onError("Unable to delete column: " + name);
        store_1.logModule.onDevError(e);
        onError === null || onError === void 0 ? void 0 : onError(e);
    });
}
exports.handleColumnDelete = handleColumnDelete;

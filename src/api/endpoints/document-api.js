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
exports.clearCurrentDocument = exports.setCurrentDocument = exports.deleteDocumentArtifact = exports.saveDocumentArtifacts = exports.deleteDocument = exports.getDocuments = exports.saveDocument = void 0;
var api_1 = require("@/api");
/**
 * Creates or updates given document under project specified.
 *
 * @param versionId - The version to mark the document as created.
 * @param document - The document to be created.
 * @return The saved document.
 */
function saveDocument(versionId, document) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            return [2 /*return*/, api_1.authHttpClient(api_1.fillEndpoint(api_1.Endpoint.createOrUpdateDocument, {
                    versionId: versionId
                }), {
                    method: "POST",
                    body: JSON.stringify(document)
                })];
        });
    });
}
exports.saveDocument = saveDocument;
/**
 * Returns list of documents associated with given project.
 *
 * @param projectId - The project to get documents for.
 * @return The project's documents.
 */
function getDocuments(projectId) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            return [2 /*return*/, api_1.authHttpClient(api_1.fillEndpoint(api_1.Endpoint.getProjectDocuments, {
                    projectId: projectId
                }), {
                    method: "GET"
                })];
        });
    });
}
exports.getDocuments = getDocuments;
/**
 * Deletes the given document from the database.
 * User must have edit permissions on the project.
 *
 * @param document - The document to be deleted.
 */
function deleteDocument(document) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, api_1.authHttpClient(api_1.fillEndpoint(api_1.Endpoint.deleteDocument, {
                        documentId: document.documentId
                    }), {
                        method: "DELETE"
                    })];
                case 1:
                    _a.sent();
                    return [2 /*return*/];
            }
        });
    });
}
exports.deleteDocument = deleteDocument;
/**
 * Attaches artifacts to a document.
 *
 * @param versionId - The version to mark the addition to.
 * @param documentId - The document to which the artifacts are added to.
 * @param artifacts - The artifacts being added to the document.
 * @return The attached artifacts.
 */
function saveDocumentArtifacts(versionId, documentId, artifacts) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            return [2 /*return*/, api_1.authHttpClient(api_1.fillEndpoint(api_1.Endpoint.addArtifactsToDocument, {
                    versionId: versionId,
                    documentId: documentId
                }), {
                    method: "POST",
                    body: JSON.stringify(artifacts)
                })];
        });
    });
}
exports.saveDocumentArtifacts = saveDocumentArtifacts;
/**
 * Removed artifacts from a document.
 *
 * @param versionId - The version to mark the removal at.
 * @param documentId - The document to remove the artifacts from.
 * @param artifactId - The artifact to remove from the document.
 */
function deleteDocumentArtifact(versionId, documentId, artifactId) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            return [2 /*return*/, api_1.authHttpClient(api_1.fillEndpoint(api_1.Endpoint.removeArtifactFromDocument, {
                    versionId: versionId,
                    documentId: documentId,
                    artifactId: artifactId
                }), {
                    method: "DELETE"
                })];
        });
    });
}
exports.deleteDocumentArtifact = deleteDocumentArtifact;
/**
 * Sets the document to be the user's current document.
 * @param documentId The document to save.
 */
function setCurrentDocument(documentId) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            return [2 /*return*/, api_1.authHttpClient(api_1.fillEndpoint(api_1.Endpoint.setCurrentDocument, {
                    documentId: documentId
                }), {
                    method: "POST"
                })];
        });
    });
}
exports.setCurrentDocument = setCurrentDocument;
/**
 * Removes the current document affiliated with current user.
 */
function clearCurrentDocument() {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            return [2 /*return*/, api_1.authHttpClient(api_1.fillEndpoint(api_1.Endpoint.clearCurrentDocument, {}), {
                    method: "DELETE"
                })];
        });
    });
}
exports.clearCurrentDocument = clearCurrentDocument;

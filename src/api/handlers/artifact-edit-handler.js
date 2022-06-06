"use strict";
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
exports.handleDeleteArtifact = exports.handleDuplicateArtifact = exports.handleSaveArtifact = void 0;
var types_1 = require("@/types");
var store_1 = require("@/store");
var api_1 = require("@/api");
/**
 * Creates or updates an artifact, and updates app state.
 *
 * @param artifact - The artifact to create.
 * @param isUpdate - Whether this operation should label this commit as
 * updating a previously existing artifact.
 * @param parentArtifact - The parent artifact to link to.
 * @param onSuccess - Called if the save is successful.
 * @param onError - Called if the save fails.
 */
function handleSaveArtifact(artifact, isUpdate, parentArtifact, _a) {
    var onSuccess = _a.onSuccess, onError = _a.onError;
    return __awaiter(this, void 0, void 0, function () {
        var versionId, updatedArtifacts, createdArtifacts, _i, createdArtifacts_1, createdArtifact, e_1;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    _b.trys.push([0, 12, , 13]);
                    versionId = store_1.projectModule.versionIdWithLog;
                    if (!isUpdate) return [3 /*break*/, 3];
                    return [4 /*yield*/, api_1.updateArtifact(versionId, artifact)];
                case 1:
                    updatedArtifacts = _b.sent();
                    return [4 /*yield*/, store_1.projectModule.addOrUpdateArtifacts(updatedArtifacts)];
                case 2:
                    _b.sent();
                    return [3 /*break*/, 11];
                case 3: return [4 /*yield*/, api_1.createArtifact(versionId, artifact)];
                case 4:
                    createdArtifacts = _b.sent();
                    return [4 /*yield*/, store_1.projectModule.addOrUpdateArtifacts(createdArtifacts)];
                case 5:
                    _b.sent();
                    return [4 /*yield*/, store_1.artifactSelectionModule.selectArtifact(createdArtifacts[0].id)];
                case 6:
                    _b.sent();
                    return [4 /*yield*/, store_1.viewportModule.setArtifactTreeLayout()];
                case 7:
                    _b.sent();
                    if (!parentArtifact) {
                        onSuccess === null || onSuccess === void 0 ? void 0 : onSuccess();
                        return [2 /*return*/];
                    }
                    _i = 0, createdArtifacts_1 = createdArtifacts;
                    _b.label = 8;
                case 8:
                    if (!(_i < createdArtifacts_1.length)) return [3 /*break*/, 11];
                    createdArtifact = createdArtifacts_1[_i];
                    return [4 /*yield*/, api_1.handleCreateLink({
                            traceLinkId: "",
                            sourceName: createdArtifact.name,
                            sourceId: createdArtifact.id,
                            targetName: parentArtifact.name,
                            targetId: parentArtifact.id,
                            approvalStatus: types_1.TraceApproval.APPROVED,
                            score: 1,
                            traceType: types_1.TraceType.MANUAL
                        })];
                case 9:
                    _b.sent();
                    _b.label = 10;
                case 10:
                    _i++;
                    return [3 /*break*/, 8];
                case 11:
                    onSuccess === null || onSuccess === void 0 ? void 0 : onSuccess();
                    return [3 /*break*/, 13];
                case 12:
                    e_1 = _b.sent();
                    store_1.logModule.onDevError(e_1);
                    store_1.logModule.onError("Unable to create artifact: " + artifact.name);
                    onError === null || onError === void 0 ? void 0 : onError(e_1);
                    return [3 /*break*/, 13];
                case 13: return [2 /*return*/];
            }
        });
    });
}
exports.handleSaveArtifact = handleSaveArtifact;
/**
 * Duplicates an artifact, and updates the app state.
 *
 * @param artifact  - The artifact to duplicate.
 * @param onSuccess - Called if the duplicate is successful.
 * @param onError - Called if the duplicate fails.
 */
function handleDuplicateArtifact(artifact, _a) {
    var onSuccess = _a.onSuccess, onError = _a.onError;
    return handleSaveArtifact(__assign(__assign({}, artifact), { name: artifact.name + " (Copy)", id: "", baseEntityId: "" }), false, undefined, { onSuccess: onSuccess, onError: onError });
}
exports.handleDuplicateArtifact = handleDuplicateArtifact;
/**
 * Deletes an artifact, and updates the app state.
 *
 * @param artifact  - The artifact to delete.
 * @param onSuccess - Called if the delete is successful.
 * @param onError - Called if the delete fails.
 */
function handleDeleteArtifact(artifact, _a) {
    var _this = this;
    var onSuccess = _a.onSuccess, onError = _a.onError;
    return new Promise(function (resolve, reject) {
        store_1.logModule.SET_CONFIRMATION_MESSAGE({
            type: types_1.ConfirmationType.INFO,
            title: "Delete " + artifact.name + "?",
            body: "Deleting this artifact cannot be undone in this version of SAFA.",
            statusCallback: function (isConfirmed) {
                if (!isConfirmed)
                    return;
                api_1.deleteArtifact(artifact)
                    .then(function () { return __awaiter(_this, void 0, void 0, function () {
                    return __generator(this, function (_a) {
                        switch (_a.label) {
                            case 0: return [4 /*yield*/, store_1.projectModule.deleteArtifacts([artifact])];
                            case 1:
                                _a.sent();
                                return [4 /*yield*/, store_1.artifactSelectionModule.UNSELECT_ARTIFACT()];
                            case 2:
                                _a.sent();
                                onSuccess === null || onSuccess === void 0 ? void 0 : onSuccess();
                                resolve();
                                return [2 /*return*/];
                        }
                    });
                }); })["catch"](function (e) {
                    onError === null || onError === void 0 ? void 0 : onError(e);
                    reject(e);
                });
            }
        });
    });
}
exports.handleDeleteArtifact = handleDeleteArtifact;

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
exports.handleDeleteMember = exports.handleInviteMember = void 0;
var types_1 = require("@/types");
var store_1 = require("@/store");
var api_1 = require("@/api");
/**
 * Adds a user to a project and logs the status.
 *
 * @param projectId - The project to add this user to.
 * @param memberEmail - The email of the given user.
 * @param projectRole - The role to set for the given user.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
function handleInviteMember(projectId, memberEmail, projectRole, _a) {
    var onSuccess = _a.onSuccess, onError = _a.onError;
    api_1.saveProjectMember(projectId, memberEmail, projectRole)
        .then(function () {
        store_1.logModule.onSuccess("Member added to the project: " + memberEmail);
        onSuccess === null || onSuccess === void 0 ? void 0 : onSuccess();
    })["catch"](function (e) {
        store_1.logModule.onSuccess("Unable to add member: " + memberEmail);
        store_1.logModule.onDevError(e.message);
        onError === null || onError === void 0 ? void 0 : onError(e);
    });
}
exports.handleInviteMember = handleInviteMember;
/**
 * Opens a confirmation modal to delete the given member.
 *
 * @param member - The member to delete.
 */
function handleDeleteMember(member) {
    var _this = this;
    store_1.logModule.SET_CONFIRMATION_MESSAGE({
        type: types_1.ConfirmationType.INFO,
        title: "Remove User from Project",
        body: "Are you sure you want to remove " + member.email + " from project?",
        statusCallback: function (isConfirmed) { return __awaiter(_this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!isConfirmed)
                            return [2 /*return*/];
                        return [4 /*yield*/, api_1.deleteProjectMember(member)];
                    case 1:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        }); }
    });
}
exports.handleDeleteMember = handleDeleteMember;

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
exports.handleLoadLastProject = void 0;
var router_1 = require("@/router");
var store_1 = require("@/store");
var api_1 = require("@/api");
/**
 * Loads the last stored project.
 */
function handleLoadLastProject() {
    return __awaiter(this, void 0, void 0, function () {
        var versionId, projects;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    versionId = router_1.getParam(router_1.QueryParams.VERSION);
                    if (!!versionId) return [3 /*break*/, 3];
                    return [4 /*yield*/, api_1.getProjects()];
                case 1:
                    projects = _a.sent();
                    if (!(projects.length > 0)) return [3 /*break*/, 3];
                    return [4 /*yield*/, api_1.getCurrentVersion(projects[0].projectId)];
                case 2:
                    versionId = (_a.sent()).versionId;
                    _a.label = 3;
                case 3:
                    if (!(versionId && typeof versionId === "string")) return [3 /*break*/, 6];
                    return [4 /*yield*/, store_1.sessionModule.updateSession({ versionId: versionId })];
                case 4:
                    _a.sent();
                    return [4 /*yield*/, api_1.handleLoadVersion(versionId)["catch"](function () {
                            return router_1.navigateTo(router_1.Routes.PROJECT_CREATOR);
                        })];
                case 5:
                    _a.sent();
                    return [3 /*break*/, 8];
                case 6: return [4 /*yield*/, router_1.navigateTo(router_1.Routes.PROJECT_CREATOR)];
                case 7:
                    _a.sent();
                    _a.label = 8;
                case 8: return [2 /*return*/];
            }
        });
    });
}
exports.handleLoadLastProject = handleLoadLastProject;

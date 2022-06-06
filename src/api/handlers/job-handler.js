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
exports.handleDeleteJob = exports.handleJobSubmission = exports.connectAndSubscribeToJob = void 0;
var api_1 = require("@/api");
var store_1 = require("@/store");
/**
 * Subscribes to updates for job with given id.
 *
 * @param jobId - The id for the job whose updates we want to process.
 */
function connectAndSubscribeToJob(jobId) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    if (!jobId) {
                        return [2 /*return*/];
                    }
                    return [4 /*yield*/, api_1.connect()];
                case 1:
                    _a.sent();
                    api_1.stompClient.subscribe(api_1.fillEndpoint(api_1.Endpoint.jobTopic, { jobId: jobId }), function (frame) {
                        var incomingJob = JSON.parse(frame.body);
                        store_1.jobModule.addOrUpdateJob(incomingJob);
                        store_1.logModule.onDevMessage("New Job message: " + incomingJob.id);
                    });
                    return [2 /*return*/];
            }
        });
    });
}
exports.connectAndSubscribeToJob = connectAndSubscribeToJob;
/**
 * Subscribes to job updates via websocket messages, updates the
 * store, and selects the job.
 */
function handleJobSubmission(job) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, connectAndSubscribeToJob(job.id)];
                case 1:
                    _a.sent();
                    store_1.jobModule.addOrUpdateJob(job);
                    store_1.jobModule.selectJob(job);
                    return [2 /*return*/];
            }
        });
    });
}
exports.handleJobSubmission = handleJobSubmission;
/**
 * Deletes a job.
 *
 * @param job - The job to delete.
 * @param onSuccess - Called if the action is successful.
 * @param onError - Called if the action fails.
 */
function handleDeleteJob(job, _a) {
    var onSuccess = _a.onSuccess, onError = _a.onError;
    api_1.deleteJobById(job.id)
        .then(function () {
        store_1.jobModule.deleteJob(job);
        onSuccess === null || onSuccess === void 0 ? void 0 : onSuccess();
    })["catch"](onError);
}
exports.handleDeleteJob = handleDeleteJob;

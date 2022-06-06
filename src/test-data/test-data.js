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
exports.__esModule = true;
exports.traces = exports.artifactMap = exports.artifacts = void 0;
var types_1 = require("@/types");
var designs_1 = require("@/test-data/designs");
var environmental_assumptions_1 = require("@/test-data/environmental-assumptions");
var hazards_1 = require("@/test-data/hazards");
var requirements_1 = require("@/test-data/requirements");
exports.artifacts = hazards_1.hazards
    .concat(requirements_1.requirements)
    .concat(designs_1.designs)
    .concat(environmental_assumptions_1.environementalAssumptions);
exports.artifactMap = exports.artifacts
    .map(function (artifact) {
    var _a;
    return (_a = {}, _a[artifact.name] = artifact, _a);
})
    .reduce(function (acc, cur) { return (__assign(__assign({}, acc), cur)); }, {});
exports.traces = [
    {
        targetName: "F9",
        targetId: exports.artifactMap["F9"].id,
        sourceName: "F15",
        sourceId: exports.artifactMap["F15"].id,
        traceLinkId: "",
        score: 1,
        approvalStatus: types_1.TraceApproval.APPROVED,
        traceType: types_1.TraceType.MANUAL
    },
    {
        targetId: "",
        sourceId: "",
        targetName: "F15",
        sourceName: "F16",
        traceLinkId: "",
        score: 1,
        approvalStatus: types_1.TraceApproval.APPROVED,
        traceType: types_1.TraceType.MANUAL
    },
    {
        targetId: "",
        sourceId: "",
        targetName: "F15",
        sourceName: "F17",
        traceLinkId: "",
        score: 1,
        approvalStatus: types_1.TraceApproval.APPROVED,
        traceType: types_1.TraceType.MANUAL
    },
    {
        targetName: "F5",
        targetId: "",
        sourceName: "D1",
        sourceId: "",
        traceLinkId: "",
        score: 1,
        approvalStatus: types_1.TraceApproval.APPROVED,
        traceType: types_1.TraceType.MANUAL
    },
    {
        targetName: "F5",
        targetId: "",
        sourceName: "D2",
        sourceId: "",
        traceLinkId: "",
        score: 1,
        approvalStatus: types_1.TraceApproval.APPROVED,
        traceType: types_1.TraceType.MANUAL
    },
    {
        targetName: "F6",
        targetId: "",
        sourceName: "D3",
        sourceId: "",
        traceLinkId: "",
        score: 1,
        approvalStatus: types_1.TraceApproval.APPROVED,
        traceType: types_1.TraceType.MANUAL
    },
    {
        targetName: "F6",
        targetId: "",
        sourceName: "D4",
        sourceId: "",
        traceLinkId: "",
        score: 1,
        approvalStatus: types_1.TraceApproval.APPROVED,
        traceType: types_1.TraceType.MANUAL
    },
    {
        targetName: "F6",
        targetId: "",
        sourceName: "D5",
        sourceId: "",
        traceLinkId: "",
        score: 1,
        approvalStatus: types_1.TraceApproval.APPROVED,
        traceType: types_1.TraceType.MANUAL
    },
    {
        targetName: "F10",
        targetId: "",
        sourceId: "",
        sourceName: "D7",
        traceLinkId: "",
        score: 1,
        approvalStatus: types_1.TraceApproval.APPROVED,
        traceType: types_1.TraceType.MANUAL
    },
    {
        targetId: "",
        sourceId: "",
        targetName: "F10",
        sourceName: "D9",
        traceLinkId: "",
        score: 1,
        approvalStatus: types_1.TraceApproval.APPROVED,
        traceType: types_1.TraceType.MANUAL
    },
    {
        targetId: "",
        sourceId: "",
        targetName: "F11",
        sourceName: "F8",
        traceLinkId: "",
        score: 1,
        approvalStatus: types_1.TraceApproval.APPROVED,
        traceType: types_1.TraceType.MANUAL
    },
    {
        targetId: "",
        sourceId: "",
        targetName: "F11",
        sourceName: "F9",
        traceLinkId: "",
        score: 1,
        approvalStatus: types_1.TraceApproval.APPROVED,
        traceType: types_1.TraceType.MANUAL
    },
    {
        targetId: "",
        sourceId: "",
        targetName: "F1",
        sourceName: "EA1",
        traceLinkId: "",
        score: 1,
        approvalStatus: types_1.TraceApproval.APPROVED,
        traceType: types_1.TraceType.MANUAL
    },
    {
        targetId: "",
        sourceId: "",
        targetName: "F1",
        sourceName: "F2",
        traceLinkId: "",
        score: 1,
        approvalStatus: types_1.TraceApproval.APPROVED,
        traceType: types_1.TraceType.MANUAL
    },
    {
        targetId: "",
        sourceId: "",
        targetName: "F1",
        sourceName: "F3",
        traceLinkId: "",
        score: 1,
        approvalStatus: types_1.TraceApproval.APPROVED,
        traceType: types_1.TraceType.MANUAL
    },
    {
        targetId: "",
        sourceId: "",
        targetName: "F1",
        sourceName: "F4",
        traceLinkId: "",
        score: 1,
        approvalStatus: types_1.TraceApproval.APPROVED,
        traceType: types_1.TraceType.MANUAL
    },
    {
        targetId: "",
        sourceId: "",
        targetName: "F4",
        sourceName: "F20",
        traceLinkId: "",
        score: 1,
        approvalStatus: types_1.TraceApproval.DECLINED,
        traceType: types_1.TraceType.GENERATED
    },
    {
        targetId: "",
        sourceId: "",
        targetName: "F2",
        sourceName: "F5",
        traceLinkId: "",
        score: 1,
        approvalStatus: types_1.TraceApproval.APPROVED,
        traceType: types_1.TraceType.MANUAL
    },
    {
        targetId: "",
        sourceId: "",
        targetName: "F2",
        sourceName: "F6",
        traceLinkId: "",
        score: 1,
        approvalStatus: types_1.TraceApproval.APPROVED,
        traceType: types_1.TraceType.MANUAL
    },
    {
        targetId: "",
        sourceId: "",
        targetName: "F4",
        sourceName: "F11",
        traceLinkId: "",
        score: 1,
        approvalStatus: types_1.TraceApproval.APPROVED,
        traceType: types_1.TraceType.GENERATED
    },
    {
        targetId: "",
        sourceId: "",
        targetName: "F3",
        sourceName: "F10",
        traceLinkId: "",
        score: 1,
        approvalStatus: types_1.TraceApproval.APPROVED,
        traceType: types_1.TraceType.MANUAL
    },
    {
        targetName: "F4",
        targetId: "ce76e8b7-25ef-4e6d-a118-757c3473c2d7",
        sourceName: "F21",
        sourceId: "ce76e8b7-25ef-4e6d-a118-757c3473c2d7",
        traceLinkId: "",
        score: 1,
        approvalStatus: types_1.TraceApproval.APPROVED,
        traceType: types_1.TraceType.GENERATED
    },
];

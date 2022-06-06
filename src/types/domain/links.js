"use strict";
exports.__esModule = true;
exports.InternalTraceType = exports.TraceType = exports.TraceApproval = void 0;
/**
 * Enumerates the type of trace approvals.
 */
var TraceApproval;
(function (TraceApproval) {
    TraceApproval["UNREVIEWED"] = "UNREVIEWED";
    TraceApproval["APPROVED"] = "APPROVED";
    TraceApproval["DECLINED"] = "DECLINED";
})(TraceApproval = exports.TraceApproval || (exports.TraceApproval = {}));
/**
 * Enumerates the type of traces.
 */
var TraceType;
(function (TraceType) {
    TraceType["GENERATED"] = "GENERATED";
    TraceType["MANUAL"] = "MANUAL";
})(TraceType = exports.TraceType || (exports.TraceType = {}));
/**
 * Enumerates the type of traces used internally.
 */
var InternalTraceType;
(function (InternalTraceType) {
    InternalTraceType["SUBTREE"] = "SUBTREE";
})(InternalTraceType = exports.InternalTraceType || (exports.InternalTraceType = {}));

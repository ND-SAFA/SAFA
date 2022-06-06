"use strict";
exports.__esModule = true;
exports.extractTraceId = exports.getTraceId = void 0;
/**
 * Returns the trace ID made from the given source and target IDs.
 *
 * @param source - The source ID.
 * @param target - THe target ID.
 * @return The standardized ID of the source joined to the target.
 */
function getTraceId(source, target) {
    return source + "-" + target;
}
exports.getTraceId = getTraceId;
/**
 * Returns the trace ID made from the given source and target IDs.
 *
 * @param traceLink - The trace link.
 * @return The standardized ID of the source joined to the target.
 */
function extractTraceId(traceLink) {
    return traceLink.sourceName + "-" + traceLink.targetName;
}
exports.extractTraceId = extractTraceId;

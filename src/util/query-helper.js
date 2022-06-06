"use strict";
exports.__esModule = true;
exports.getSingleQueryResult = void 0;
/**
 * Returns the artifact in list if single item exists.
 *
 * @param query - List of artifacts representing some query for an artifact.
 * @param queryName - The name of the operation to log if operation fails.
 * @return The found artifact.
 * @throws Error if query contains multiple or no results.
 */
function getSingleQueryResult(query, queryName) {
    switch (query.length) {
        case 1:
            return query[0];
        case 0:
            throw Error("Query resulted in empty results: " + queryName);
        default:
            throw Error("Found more than one result in query: " + queryName);
    }
}
exports.getSingleQueryResult = getSingleQueryResult;

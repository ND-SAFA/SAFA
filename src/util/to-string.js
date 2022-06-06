"use strict";
exports.__esModule = true;
exports.versionToString = void 0;
/**
 * Stringifies the version number.
 *
 * @param currentVersion - The current version number.
 *
 * @return The stringified version number.
 */
function versionToString(currentVersion) {
    if (currentVersion === undefined) {
        return "X.X.X";
    }
    return currentVersion.majorVersion + "." + currentVersion.minorVersion + "." + currentVersion.revision;
}
exports.versionToString = versionToString;

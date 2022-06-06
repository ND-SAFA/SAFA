"use strict";
exports.__esModule = true;
exports.getJobStatusColor = exports.getBackgroundColor = exports.ThemeColors = void 0;
var types_1 = require("@/types");
/**
 * Defines all colors in the theme.
 */
var ThemeColors;
(function (ThemeColors) {
    ThemeColors["primary"] = "#00304c";
    ThemeColors["secondary"] = "#FFD740";
    ThemeColors["accent"] = "#006aff";
    ThemeColors["error"] = "rgb(255, 82, 82)";
    ThemeColors["menuHighlight"] = "#f0f0f0";
    ThemeColors["artifactDefault"] = "#fafafa";
    ThemeColors["artifactBorder"] = "#888888";
    ThemeColors["artifactAdded"] = "#81c784";
    ThemeColors["artifactRemoved"] = "#e57373";
    ThemeColors["artifactModified"] = "#64b5f6";
})(ThemeColors = exports.ThemeColors || (exports.ThemeColors = {}));
/**
 * Returns the background color for the given delta state.
 * @param deltaState - The delta state to get the color for.
 * @return The color.
 */
function getBackgroundColor(deltaState) {
    switch (deltaState) {
        case types_1.ArtifactDeltaState.ADDED:
            return ThemeColors.artifactAdded;
        case types_1.ArtifactDeltaState.REMOVED:
            return ThemeColors.artifactRemoved;
        case types_1.ArtifactDeltaState.MODIFIED:
            return ThemeColors.artifactModified;
        default:
            return ThemeColors.artifactDefault;
    }
}
exports.getBackgroundColor = getBackgroundColor;
/**
 * Returns the color of a job status.
 *
 * @param status - The job status to get the color of.
 * @returns The display color.
 */
function getJobStatusColor(status) {
    switch (status) {
        case types_1.JobStatus.COMPLETED:
            return ThemeColors.artifactModified;
        case types_1.JobStatus.IN_PROGRESS:
            return "#EEBC3D";
        case types_1.JobStatus.CANCELLED:
            return ThemeColors.artifactRemoved;
        default:
            return "";
    }
}
exports.getJobStatusColor = getJobStatusColor;

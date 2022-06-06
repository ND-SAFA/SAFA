"use strict";
exports.__esModule = true;
exports.timestampToDisplay = exports.enumToDisplay = exports.getArtifactTypePrintName = exports.capitalizeSentence = exports.capitalize = exports.splitIntoLines = void 0;
/**
 * Returns given string with newlines inserted after maxWordCount
 * has been reached.
 *
 * @param str - The original string.
 * @param maxWordCount - The maximum number of words to have per line.
 *
 * @returns The updated input string.
 */
function splitIntoLines(str, maxWordCount) {
    var words = str.split(" ");
    var finalString = "";
    var count = 0;
    words.forEach(function (w) {
        if (count < maxWordCount) {
            finalString += w + " ";
            count++;
        }
        else {
            finalString += w + "\n";
            count = 0;
        }
    });
    return finalString;
}
exports.splitIntoLines = splitIntoLines;
/**
 * Capitalizes the first letter of the given string.
 *
 * @param str - The string to capitalize.
 *
 * @return The capitalized string.
 */
function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}
exports.capitalize = capitalize;
/**
 * Capitalizes the first letter of all words in the given string.
 *
 * @param str - The string to capitalize.
 *
 * @return The capitalized string.
 */
function capitalizeSentence(str) {
    return str
        .split(" ")
        .map(function (word) { return capitalize(word); })
        .join(" ");
}
exports.capitalizeSentence = capitalizeSentence;
/**
 * @deprecated Remove when project creator done.
 *
 * Returns the sentence case name of the artifact type.
 *
 * @param type - The type to stringify.
 *
 * @return The sentence case type name.
 */
function getArtifactTypePrintName(type) {
    var nameMap = {
        requirement: "Requirements",
        design: "Designs",
        hazard: "Hazards",
        environmentalassumption: "Environmental Assumptions",
        safetyrequirement: "Safety Requirement"
    };
    return type
        ? nameMap[type.toLowerCase()] || capitalizeSentence(type.toLowerCase())
        : "Unknown Type";
}
exports.getArtifactTypePrintName = getArtifactTypePrintName;
/**
 * Converts an enum value in capital snake case into a title case string.
 *
 * @param value - The value to convert.
 * @return The displayable value.
 */
function enumToDisplay(value) {
    return value
        .split("_")
        .map(function (word) { return capitalize(word.toLowerCase()); })
        .join(" ");
}
exports.enumToDisplay = enumToDisplay;
/**
 * Converts a timestamp to a display value.
 *
 * @param timestamp - The timestamp to convert.
 * @return The displayable value.
 */
function timestampToDisplay(timestamp) {
    var date = new Date(timestamp);
    var options = {
        year: "numeric",
        month: "long",
        day: "numeric",
        weekday: "long",
        hour: "numeric",
        minute: "numeric"
    };
    return date.toLocaleDateString("en-US", options);
}
exports.timestampToDisplay = timestampToDisplay;

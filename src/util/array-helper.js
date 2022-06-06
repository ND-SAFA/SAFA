"use strict";
exports.__esModule = true;
exports.areArraysEqual = void 0;
/**
 * Returns whether the two given arrays have equal item values.
 *
 * @param array1 - The first array.
 * @param array2 - The second array.
 *
 * @return Whether the two arrays have equal item values.
 */
function areArraysEqual(array1, array2) {
    return (array1.length === array2.length &&
        array1.every(function (value, index) { return value === array2[index]; }));
}
exports.areArraysEqual = areArraysEqual;

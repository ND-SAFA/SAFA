"use strict";
exports.__esModule = true;
exports.ApplicationActivity = void 0;
/**
 * Enumerates the states of parsing.
 */
var ApplicationActivity;
(function (ApplicationActivity) {
    ApplicationActivity[ApplicationActivity["PARSING_TIM"] = 0] = "PARSING_TIM";
    ApplicationActivity[ApplicationActivity["PARSING_ARTIFACTS"] = 1] = "PARSING_ARTIFACTS";
    ApplicationActivity[ApplicationActivity["PARSING_TRACES"] = 2] = "PARSING_TRACES";
    ApplicationActivity[ApplicationActivity["UNKNOWN"] = 3] = "UNKNOWN";
})(ApplicationActivity = exports.ApplicationActivity || (exports.ApplicationActivity = {}));

"use strict";
exports.__esModule = true;
exports.safetyCaseMenuOption = void 0;
var store_1 = require("@/store");
var types_1 = require("@/types");
/**
 * The menu option for creating safety case artifacts.
 */
exports.safetyCaseMenuOption = {
    id: "add-sc-node",
    content: "Add Safety Case Node",
    tooltipText: "Goal, Solution, Context, Evidence",
    onClickFunction: function () {
        store_1.appModule.openArtifactCreatorTo(types_1.SafetyCaseType.GOAL);
    },
    isVisible: function (artifactData) {
        if (artifactData === undefined) {
            return store_1.documentModule.type === types_1.DocumentType.SAFETY_CASE;
        }
        return false;
    },
    submenu: [
        {
            id: "sc-goal-node",
            content: "Goal Node",
            tooltipText: "Define an expected system property.",
            onClickFunction: function () {
                store_1.appModule.openArtifactCreatorTo(types_1.SafetyCaseType.GOAL);
            }
        },
        {
            id: "sc-strategy-node",
            content: "Strategy Node",
            tooltipText: "Define the safety strategy of an argument.",
            onClickFunction: function () {
                store_1.appModule.openArtifactCreatorTo(types_1.SafetyCaseType.STRATEGY);
            }
        },
        {
            id: "sc-context-node",
            content: "Context Node",
            tooltipText: "Define the expected system environment assumptions.",
            onClickFunction: function () {
                store_1.appModule.openArtifactCreatorTo(types_1.SafetyCaseType.CONTEXT);
            }
        },
        {
            id: "sc-evidence-node",
            content: "Evidence Node",
            tooltipText: "Define a container for ground-truth resources.",
            onClickFunction: function () {
                store_1.appModule.openArtifactCreatorTo(types_1.SafetyCaseType.SOLUTION);
            }
        },
    ]
};

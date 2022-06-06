"use strict";
exports.__esModule = true;
exports.ftaMenuItem = void 0;
var store_1 = require("@/store");
var types_1 = require("@/types");
/**
 * The menu item for creating FTA related nodes.
 */
exports.ftaMenuItem = {
    id: "add-fta-node",
    content: "Add FTA Node",
    tooltipText: "Create a logical node (e.g. AND / OR)",
    onClickFunction: function () {
        store_1.appModule.openArtifactCreatorTo(types_1.FTANodeType.AND);
    },
    isVisible: function (artifactData) {
        if (artifactData === undefined) {
            return store_1.documentModule.type === types_1.DocumentType.FTA;
        }
        return false;
    },
    submenu: [
        {
            id: "fta-and-node",
            content: "AND",
            tooltipText: "Asserts all conditions must be met.",
            onClickFunction: function () {
                store_1.appModule.openArtifactCreatorTo(types_1.FTANodeType.AND);
            }
        },
        {
            id: "fta-or-node",
            content: "OR",
            tooltipText: "Asserts at least one condition must be met.",
            onClickFunction: function () {
                store_1.appModule.openArtifactCreatorTo(types_1.FTANodeType.OR);
            }
        },
    ]
};

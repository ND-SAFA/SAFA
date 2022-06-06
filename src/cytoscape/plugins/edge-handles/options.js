"use strict";
exports.__esModule = true;
exports.artifactTreeEdgeHandleOptions = void 0;
var store_1 = require("@/store");
var types_1 = require("@/types");
var util_1 = require("@/util");
// the default values of each option are outlined below:
exports.artifactTreeEdgeHandleOptions = {
    /**
     * Return whether any two nodes can be traced. Criteria includes:
     * - source != target.
     * - trace link between source and target doesn't already exist.
     *
     * @param sourceNode - The source node on the graph.
     * @param targetNode - The target node on the graph.
     * @returns Whether the two nodes can be traced.
     */
    canConnect: function (sourceNode, targetNode) {
        if (sourceNode.data() === undefined || targetNode.data() === undefined) {
            // If either link doesn't have any data, the link cannot be created.
            return false;
        }
        var sourceData = sourceNode.data();
        var targetData = targetNode.data();
        // If this link already exists, the link cannot be created.
        var linkDoesNotExist = !store_1.traceModule.doesLinkExist(sourceData.id, targetData.id);
        // If this link in opposite direct exists, the link cannot be created.
        var oppositeLinkDoesNotExist = !store_1.traceModule.doesLinkExist(targetData.id, sourceData.id);
        // If this link is to itself, the link cannot be created.
        var isNotSameNode = !sourceNode.same(targetNode);
        // If the link is not between allowed artifact directions, thee link cannot be created.
        var linkIsAllowedByType = artifactTypesAreValid(sourceData, targetData);
        return (linkDoesNotExist &&
            isNotSameNode &&
            oppositeLinkDoesNotExist &&
            linkIsAllowedByType);
    },
    /**
     * Handler that determines the data to be added to cytoscape upon the edge snap
     * to a target node.
     *
     * @param sourceNode - The source node on the graph.
     * @param targetNode - The target node on the graph.
     * @returns The created edge.
     */
    edgeParams: function (sourceNode, targetNode) {
        var source = sourceNode.data().id;
        var target = targetNode.data().id;
        return { id: util_1.getTraceId(source, target), source: source, target: target };
    },
    // time spent hovering over a target node before it is considered selected.
    hoverDelay: 0,
    // when enabled, the edge can be drawn by just moving close to a target node (can be confusing on compound graphs).
    snap: true,
    // the target node must be less than or equal to this many pixels away from the cursor/finger.
    snapThreshold: 50,
    // the number of times per second (Hz) that snap checks done (lower is less expensive).
    snapFrequency: 15,
    // set events:no to edges during draws, prevents mouseouts on compounds.
    noEdgeEventsInDraw: true,
    // during an edge drawing gesture, disable browser gestures such as two-finger trackpad swipe and pinch-to-zoom.
    disableBrowserGestures: true
};
/**
 * Returns whether given artifact can traced regarding their artifact types
 * rules.
 * @param sourceData The artifact data of the source artifact.
 * @param targetData The artifact data of the target artifact.
 */
function artifactTypesAreValid(sourceData, targetData) {
    var isSourceDefaultArtifact = !sourceData.safetyCaseType && !sourceData.logicType;
    var isTargetDefaultArtifact = !targetData.safetyCaseType && !targetData.logicType;
    if (isSourceDefaultArtifact) {
        return store_1.typeOptionsModule.isLinkAllowedByType(sourceData.artifactType, targetData.artifactType);
    }
    else if (sourceData.safetyCaseType) {
        switch (sourceData.safetyCaseType) {
            case types_1.SafetyCaseType.STRATEGY:
                return types_1.SafetyCaseType.STRATEGY !== targetData.safetyCaseType;
            case types_1.SafetyCaseType.SOLUTION:
                return types_1.SafetyCaseType.SOLUTION !== targetData.safetyCaseType;
            default:
                return isTargetDefaultArtifact;
        }
    }
    else if (sourceData.logicType) {
        return isTargetDefaultArtifact;
    }
    throw Error("Undefined trace link logic for:" + sourceData.type);
}

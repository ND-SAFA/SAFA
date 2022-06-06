"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var __spreadArrays = (this && this.__spreadArrays) || function () {
    for (var s = 0, i = 0, il = arguments.length; i < il; i++) s += arguments[i].length;
    for (var r = Array(s), k = 0, i = 0; i < il; i++)
        for (var a = arguments[i], j = 0, jl = a.length; j < jl; j++, k++)
            r[k] = a[j];
    return r;
};
exports.__esModule = true;
exports.getRootNode = exports.createSubtreeMap = void 0;
/**
 * Computes the subtree map of given artifacts.
 *
 * @param cy - The cytoscape instance to operate on.
 * @param artifacts - The current artifacts.
 * @return The computed subtree map.
 */
function createSubtreeMap(cy, artifacts) {
    var computedSubtrees = {};
    return artifacts
        .map(function (artifact) {
        var _a;
        return (_a = {},
            _a[artifact.id] = getSubtree(cy, artifact.id, computedSubtrees),
            _a);
    })
        .reduce(function (acc, cur) { return (__assign(__assign({}, acc), cur)); }, {});
}
exports.createSubtreeMap = createSubtreeMap;
/**
 * Returns list of children names for artifact specified.
 *
 * @param cy - The cytoscape instance to operate on.
 * @param artifactId - The id of the root artifact whose subtree is being calculated.
 * @param subtreeMapCache - A cache of previously calculated subtrees.
 * @return The child ids in the subtree.
 */
function getSubtree(cy, artifactId, subtreeMapCache) {
    var currentSubtree = [];
    if (artifactId in subtreeMapCache) {
        return subtreeMapCache[artifactId];
    }
    for (var _i = 0, _a = getChildren(cy, artifactId); _i < _a.length; _i++) {
        var childId = _a[_i];
        if (!(childId in subtreeMapCache)) {
            subtreeMapCache[childId] = getSubtree(cy, childId, subtreeMapCache);
        }
        var childSubtreeIds = __spreadArrays(subtreeMapCache[childId], [childId]);
        var newSubtreeIds = childSubtreeIds.filter(function (id) { return !currentSubtree.includes(id); });
        currentSubtree = __spreadArrays(currentSubtree, newSubtreeIds);
    }
    return currentSubtree;
}
/**
 * Returns list of artifact ids corresponding to children of artifact.
 *
 * @param cy - The cytoscape instance to operate on.
 * @param artifactId - The id of the root artifact whose subtree is being calculated.
 * @return The computed child artifact ids.
 */
function getChildren(cy, artifactId) {
    var nodeEdges = cy.edges("edge[source=\"" + artifactId + "\"]");
    var children = nodeEdges.targets();
    return children.map(function (child) { return child.data().id; });
}
/**
 * Returns the top most parent from all elements in the cytoscape object.
 * Starting at the node with most edges, its parent is followed until no
 * more exist. If a loop is encountered, then the first repeated node is returned.
 *
 * @param cy - The cy instance.
 * @param currentNode - Defines where we are in the tree during recursion.
 * @param traversedNodes - A list of all traversed node IDs to avoid loops.
 * @return The root node.
 */
function getRootNode(cy, currentNode, traversedNodes) {
    if (traversedNodes === void 0) { traversedNodes = []; }
    return __awaiter(this, void 0, void 0, function () {
        var edgesOutOfNode;
        return __generator(this, function (_a) {
            if (cy.nodes().length === 0)
                return [2 /*return*/];
            if (currentNode === undefined) {
                currentNode = getMostConnectedNode(cy);
            }
            // Avoid getting stuck in cycles.
            if (traversedNodes.includes(currentNode.id())) {
                return [2 /*return*/, currentNode];
            }
            else {
                traversedNodes.push(currentNode.id());
            }
            edgesOutOfNode = cy
                .edges()
                .filter(function (e) { return e.target() === currentNode; });
            if (edgesOutOfNode.length === 0) {
                return [2 /*return*/, currentNode];
            }
            else {
                return [2 /*return*/, getRootNode(cy, edgesOutOfNode[0].source(), traversedNodes)];
            }
            return [2 /*return*/];
        });
    });
}
exports.getRootNode = getRootNode;
/**
 * Returns the node in given Cytoscape instance with the most connected edges.
 *
 * @param cy - The cytoscape instance to operate on.
 * @return The found node.
 */
function getMostConnectedNode(cy) {
    var counts = {};
    cy.edges().forEach(function (edge) {
        var sourceName = edge.source().data().id;
        var targetName = edge.target().data().id;
        var increaseCounts = function (name) {
            if (name in counts) {
                counts[name]++;
            }
            else {
                counts[name] = 1;
            }
        };
        increaseCounts(sourceName);
        increaseCounts(targetName);
    });
    var max = -1;
    var maxName = cy.nodes().first().data().name;
    for (var _i = 0, _a = Object.entries(counts); _i < _a.length; _i++) {
        var _b = _a[_i], name_1 = _b[0], count = _b[1];
        if (count > max) {
            max = count;
            maxName = name_1;
        }
    }
    return cy
        .nodes()
        .filter(function (n) { return n.data().id === maxName; })
        .first();
}

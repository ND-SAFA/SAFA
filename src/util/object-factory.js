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
exports.__esModule = true;
exports.createDocument = exports.createDefaultTypeIcons = exports.createCommit = exports.createColumn = exports.createArtifactOfType = exports.createArtifact = exports.createProjectDelta = exports.createProject = exports.createProjectIdentifier = exports.createSession = exports.createConfirmDialogueMessage = exports.createSnackbarMessage = void 0;
var types_1 = require("@/types");
/**
 * @return An empty snackbar message.
 */
function createSnackbarMessage() {
    return {
        errors: [],
        message: "",
        type: types_1.MessageType.CLEAR
    };
}
exports.createSnackbarMessage = createSnackbarMessage;
/**
 * @return An empty confirm dialog message.
 */
function createConfirmDialogueMessage() {
    return {
        type: types_1.ConfirmationType.CLEAR,
        title: "",
        body: "",
        statusCallback: function () { return null; }
    };
}
exports.createConfirmDialogueMessage = createConfirmDialogueMessage;
/**
 * @return An empty session.
 */
function createSession() {
    return {
        token: "",
        versionId: ""
    };
}
exports.createSession = createSession;
/**
 * @return An empty project identifier.
 */
function createProjectIdentifier(identifier) {
    return {
        name: (identifier === null || identifier === void 0 ? void 0 : identifier.name) || "",
        projectId: (identifier === null || identifier === void 0 ? void 0 : identifier.projectId) || "",
        description: (identifier === null || identifier === void 0 ? void 0 : identifier.description) || "",
        owner: (identifier === null || identifier === void 0 ? void 0 : identifier.owner) || "",
        members: (identifier === null || identifier === void 0 ? void 0 : identifier.members) || []
    };
}
exports.createProjectIdentifier = createProjectIdentifier;
/**
 * @return An empty project.
 */
function createProject(project) {
    return __assign(__assign({}, createProjectIdentifier(project)), { artifacts: (project === null || project === void 0 ? void 0 : project.artifacts) || [], traces: (project === null || project === void 0 ? void 0 : project.traces) || [], projectVersion: (project === null || project === void 0 ? void 0 : project.projectVersion) || undefined, artifactTypes: (project === null || project === void 0 ? void 0 : project.artifactTypes) || [], documents: (project === null || project === void 0 ? void 0 : project.documents) || [], warnings: (project === null || project === void 0 ? void 0 : project.warnings) || {} });
}
exports.createProject = createProject;
/**
 * @return An empty project delta.
 */
function createProjectDelta() {
    return {
        artifacts: {
            added: {},
            modified: {},
            removed: {}
        },
        traces: {
            added: {},
            modified: {},
            removed: {}
        }
    };
}
exports.createProjectDelta = createProjectDelta;
/**
 * @return An artifact initialized to the given props.
 */
function createArtifact(artifact) {
    return {
        id: (artifact === null || artifact === void 0 ? void 0 : artifact.id) || "",
        baseEntityId: (artifact === null || artifact === void 0 ? void 0 : artifact.baseEntityId) || "",
        name: (artifact === null || artifact === void 0 ? void 0 : artifact.name) || "",
        summary: (artifact === null || artifact === void 0 ? void 0 : artifact.summary) || "",
        body: (artifact === null || artifact === void 0 ? void 0 : artifact.body) || "",
        type: (artifact === null || artifact === void 0 ? void 0 : artifact.type) || "",
        documentType: (artifact === null || artifact === void 0 ? void 0 : artifact.documentType) || types_1.DocumentType.ARTIFACT_TREE,
        documentIds: (artifact === null || artifact === void 0 ? void 0 : artifact.documentIds) || [],
        safetyCaseType: (artifact === null || artifact === void 0 ? void 0 : artifact.safetyCaseType) || types_1.SafetyCaseType.GOAL,
        logicType: (artifact === null || artifact === void 0 ? void 0 : artifact.logicType) || types_1.FTANodeType.AND,
        customFields: (artifact === null || artifact === void 0 ? void 0 : artifact.customFields) || {}
    };
}
exports.createArtifact = createArtifact;
/**
 * Creates an artifact that may be initialized to a specific document type.
 *
 * @param artifact - The base artifact to create from.
 * @param type - If true or matching no values, a normal artifact will be created.
 *               If equal to an `FTANodeType`, an FTA node will be created.
 *               If equal to a `SafetyCaseType`, a safety case node will be created.
 *               If equal to a `DocumentType.FMEA`, an FMEA node will be created.
 * @return An artifact initialized to the given props.
 */
function createArtifactOfType(artifact, type) {
    if (typeof type === "string") {
        if (type in types_1.FTANodeType) {
            return createArtifact(__assign(__assign({}, artifact), { documentType: types_1.DocumentType.FTA, logicType: type }));
        }
        else if (type in types_1.SafetyCaseType) {
            return createArtifact(__assign(__assign({}, artifact), { documentType: types_1.DocumentType.SAFETY_CASE, safetyCaseType: type }));
        }
        else if (type === types_1.DocumentType.FMEA) {
            return createArtifact(__assign(__assign({}, artifact), { documentType: types_1.DocumentType.FMEA }));
        }
    }
    return createArtifact(artifact);
}
exports.createArtifactOfType = createArtifactOfType;
/**
 * @return An column initialized to the given props.
 */
function createColumn(column) {
    return {
        id: (column === null || column === void 0 ? void 0 : column.id) || "",
        name: (column === null || column === void 0 ? void 0 : column.name) || "",
        dataType: (column === null || column === void 0 ? void 0 : column.dataType) || types_1.ColumnDataType.FREE_TEXT,
        required: (column === null || column === void 0 ? void 0 : column.required) || false
    };
}
exports.createColumn = createColumn;
/**
 * @returns An empty commit.
 */
function createCommit(version) {
    return {
        commitVersion: version,
        artifacts: {
            added: [],
            removed: [],
            modified: []
        },
        traces: {
            added: [],
            removed: [],
            modified: []
        }
    };
}
exports.createCommit = createCommit;
/**
 * @returns A record mapping the lowercase artifact type name to the corresponding default icon.
 */
function createDefaultTypeIcons(artifactTypes) {
    if (artifactTypes === void 0) { artifactTypes = []; }
    return artifactTypes
        .map(function (t) {
        var _a;
        return (_a = {}, _a[t.name] = t.icon, _a);
    })
        .reduce(function (acc, cur) { return (__assign(__assign({}, acc), cur)); }, { "default": "mdi-help" });
}
exports.createDefaultTypeIcons = createDefaultTypeIcons;
/**
 * @return An document initialized to the given props.
 */
function createDocument(document) {
    return {
        documentId: (document === null || document === void 0 ? void 0 : document.documentId) || "",
        project: (document === null || document === void 0 ? void 0 : document.project) || {
            projectId: "",
            name: "",
            description: "",
            owner: "",
            members: []
        },
        name: (document === null || document === void 0 ? void 0 : document.name) || "Default",
        type: (document === null || document === void 0 ? void 0 : document.type) || types_1.DocumentType.ARTIFACT_TREE,
        artifactIds: (document === null || document === void 0 ? void 0 : document.artifactIds) || [],
        description: (document === null || document === void 0 ? void 0 : document.description) || ""
    };
}
exports.createDocument = createDocument;

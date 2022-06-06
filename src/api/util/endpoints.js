"use strict";
exports.__esModule = true;
exports.fillEndpoint = exports.Endpoint = exports.baseURL = void 0;
/**
 * The base URL for the project
 */
exports.baseURL = process.env.VUE_APP_API_ENDPOINT;
/**
 * Enumerates all of the possible endpoint paths.
 */
var Endpoint;
(function (Endpoint) {
    // Accounts
    Endpoint["session"] = "accounts/session";
    Endpoint["login"] = "login";
    Endpoint["createAccount"] = "accounts/create";
    Endpoint["logout"] = "accounts/logout";
    Endpoint["forgotPassword"] = "accounts/forgot";
    Endpoint["resetPassword"] = "accounts/reset";
    // Jobs
    Endpoint["updateProjectThroughFlatFiles"] = "jobs/projects/versions/:versionId";
    Endpoint["getUserJobs"] = "jobs";
    Endpoint["deleteJobById"] = "jobs/:jobId";
    Endpoint["jobTopic"] = "/topic/jobs/:jobId";
    Endpoint["projectTopic"] = "/topic/projects/:projectId";
    Endpoint["versionTopic"] = "/topic/revisions/:versionId";
    // Projects
    Endpoint["project"] = "projects";
    Endpoint["updateProject"] = "projects/:projectId";
    Endpoint["getProjectMembers"] = "projects/:projectId/members";
    Endpoint["deleteProjectMember"] = "projects/members/:projectMemberId";
    Endpoint["jiraCredentials"] = "accounts/jira/credentials";
    Endpoint["jiraProject"] = "projects/import/jira/:cloudId/:projectId";
    // Commits
    Endpoint["commit"] = "projects/versions/:versionId/commit";
    Endpoint["isArtifactNameTaken"] = "projects/versions/:versionId/artifacts/validate/:artifactName";
    // Types
    Endpoint["getProjectArtifactTypes"] = "projects/:projectId/artifactTypes";
    Endpoint["createOrUpdateArtifactType"] = "projects/:projectId/artifactTypes";
    Endpoint["deleteArtifactType"] = "projects/:projectId/artifactTypes/:typeId";
    // Links
    Endpoint["getGeneratedLinks"] = "projects/versions/:versionId/links/generated";
    Endpoint["generateLinks"] = "projects/links/generate";
    // Entity Retrieval
    Endpoint["projectVersion"] = "projects/versions/:versionId";
    Endpoint["getArtifactsInVersion"] = "projects/versions/:versionId/artifacts";
    Endpoint["getTracesInVersion"] = "projects/versions/:versionId/traces";
    // Versions
    Endpoint["getProjectVersions"] = "projects/:projectId/versions";
    Endpoint["getCurrentVersion"] = "projects/:projectId/versions/current";
    Endpoint["createNewMajorVersion"] = "projects/:projectId/versions/major";
    Endpoint["createNewMinorVersion"] = "projects/:projectId/versions/minor";
    Endpoint["createNewRevisionVersion"] = "projects/:projectId/versions/revision";
    // Documents
    Endpoint["createOrUpdateDocument"] = "projects/versions/:versionId/documents";
    Endpoint["getProjectDocuments"] = "projects/:projectId/documents";
    Endpoint["deleteDocument"] = "projects/documents/:documentId";
    // Document Artifacts
    Endpoint["addArtifactsToDocument"] = "projects/versions/:versionId/documents/:documentId/artifacts";
    Endpoint["removeArtifactFromDocument"] = "projects/versions/:versionId/documents/:documentId/artifacts/:artifactId";
    Endpoint["setCurrentDocument"] = "projects/documents/current/:documentId";
    Endpoint["clearCurrentDocument"] = "projects/documents/current";
    // Delta
    Endpoint["getProjectDelta"] = "projects/delta/:sourceVersionId/:targetVersionId";
    // Parse Entities
    Endpoint["parseArtifactFile"] = "projects/parse/artifacts/:artifactType";
    Endpoint["parseTraceFile"] = "projects/parse/traces";
    // Trace Matrices
    Endpoint["createTraceMatrix"] = "projects/:projectId/matrices/:sourceArtifactTypeName/:targetArtifactTypeName";
    Endpoint["deleteTraceMatrix"] = "projects/matrices/:traceMatrixId";
    Endpoint["retrieveTraceMatrices"] = "projects/:projectId/matrices";
    // Warnings
    Endpoint["getWarningsInProjectVersion"] = "projects/versions/:versionId/warnings";
})(Endpoint = exports.Endpoint || (exports.Endpoint = {}));
/**
 * Fills the given endpoint path with the given path variables.
 *
 * @param endpoint - The endpoint path to fill.
 * @param pathVariables - A collection of path variables, keyed by their id in the endpoint path.
 *
 * @return The filled in endpoint path.
 */
function fillEndpoint(endpoint, pathVariables) {
    if (pathVariables === void 0) { pathVariables = {}; }
    var filledPath = endpoint;
    Object.entries(pathVariables).forEach(function (_a) {
        var id = _a[0], value = _a[1];
        filledPath = filledPath.replace(":" + id, value);
    });
    return filledPath;
}
exports.fillEndpoint = fillEndpoint;

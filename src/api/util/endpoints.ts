/**
 * The base URL for the project
 */
export const baseURL = process.env.VUE_APP_API_ENDPOINT;

/**
 * Enumerates all of the possible endpoint paths.
 */
export enum Endpoint {
  // Accounts
  session = "accounts/session",
  login = "login",
  createAccount = "accounts/create",
  logout = "accounts/logout",
  forgotPassword = "accounts/forgot",
  resetPassword = "accounts/reset",
  updatePassword = "accounts/change",
  deleteAccount = "accounts/delete",

  // Jobs
  createProjectJob = "jobs/projects",
  updateProjectThroughFlatFiles = "jobs/projects/versions/:versionId",
  getUserJobs = "jobs",
  deleteJobById = "jobs/:jobId",
  jobTopic = "/topic/:jobId",
  projectTopic = "/topic/:projectId",
  versionTopic = "/topic/:versionId",

  // Projects
  project = "projects",
  updateProject = "projects/:projectId",
  getProjectMembers = "projects/:projectId/members",
  deleteProjectMember = "projects/members/:projectMemberId",
  jiraCredentials = "accounts/jira/credentials",
  githubCredentials = "accounts/github/credentials",
  jiraProject = "projects/import/jira/:cloudId/:projectId",
  githubProject = "projects/import/github/:repositoryName",

  // Commits
  commit = "projects/versions/:versionId/commit",
  isArtifactNameTaken = "projects/versions/:versionId/artifacts/validate/",
  sync = "projects/versions/:versionId/changes",

  // Types
  getProjectArtifactTypes = "projects/:projectId/artifactTypes",
  createOrUpdateArtifactType = "projects/:projectId/artifactTypes",
  deleteArtifactType = "projects/:projectId/artifactTypes/:typeId",

  // Links
  getGeneratedLinks = "projects/versions/:versionId/links/generated",
  generateLinks = "projects/links/generate",
  generateLinksJob = "jobs/projects/links/generate",

  // Entity Retrieval
  projectVersion = "projects/versions/:versionId",
  getArtifactsInVersion = "projects/versions/:versionId/artifacts",
  getTracesInVersion = "projects/versions/:versionId/traces",

  // Versions
  getProjectVersions = "projects/:projectId/versions",
  getCurrentVersion = "projects/:projectId/versions/current",
  createNewMajorVersion = "projects/:projectId/versions/major",
  createNewMinorVersion = "projects/:projectId/versions/minor",
  createNewRevisionVersion = "projects/:projectId/versions/revision",

  // Layout
  refreshLayout = "projects/versions/:versionId/layout",

  // Documents
  createOrUpdateDocument = "projects/versions/:versionId/documents",
  getProjectDocuments = "projects/versions/:versionId/documents",
  deleteDocument = "projects/documents/:documentId",

  // Document Artifacts
  addArtifactsToDocument = "projects/versions/:versionId/documents/:documentId/artifacts",
  removeArtifactFromDocument = "projects/versions/:versionId/documents/:documentId/artifacts/:artifactId",
  setCurrentDocument = "projects/documents/current/:documentId",
  clearCurrentDocument = "projects/documents/current",

  // Delta
  getProjectDelta = "projects/delta/:sourceVersionId/:targetVersionId",

  // Parse Entities
  parseArtifactFile = "projects/parse/artifacts/:artifactType",
  parseTraceFile = "projects/parse/traces",

  // Trace Matrices
  createTraceMatrix = "projects/:projectId/matrices/:sourceType/:targetType",
  deleteTraceMatrix = "projects/:projectId/matrices/:sourceType/:targetType",
  retrieveTraceMatrices = "projects/:projectId/matrices",

  // Warnings
  getWarningsInProjectVersion = "projects/versions/:versionId/warnings",
}

/**
 * Fills the given endpoint path with the given path variables.
 *
 * @param endpoint - The endpoint path to fill.
 * @param pathVariables - A collection of path variables, keyed by their id in the endpoint path.
 *
 * @return The filled in endpoint path.
 */
export function fillEndpoint(
  endpoint: Endpoint,
  pathVariables: Record<string, string> = {}
): string {
  let filledPath: string = endpoint;

  Object.entries(pathVariables).forEach(([id, value]) => {
    filledPath = filledPath.replace(`:${id}`, value);
  });

  return filledPath;
}

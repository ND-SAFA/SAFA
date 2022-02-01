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

  // Projects
  project = "projects",
  updateProject = "projects/:projectId",
  createProjectFromFlatFiles = "projects/flat-files",
  updateProjectThroughFlatFiles = "projects/versions/:versionId/flat-files",
  getProjectMembers = "projects/:projectId/members",
  deleteProjectMember = "projects/members/:projectMemberId",

  //Commits
  commit = "projects/versions/:versionId/commit",
  isArtifactNameTaken = "projects/:projectId/artifacts/validate/:artifactName",

  //Links
  getGeneratedLinks = "projects/versions/:versionId/links/generated",
  generateLinks = "projects/links/generate",

  //Versions
  projectVersion = "projects/versions/:versionId",
  getProjectVersions = "projects/:projectId/versions",
  getCurrentVersion = "projects/:projectId/versions/current",
  createNewMajorVersion = "projects/:projectId/versions/major",
  createNewMinorVersion = "projects/:projectId/versions/minor",
  createNewRevisionVersion = "projects/:projectId/versions/revision",

  //Delta
  getProjectDelta = "projects/delta/:sourceVersionId/:targetVersionId",

  //Parse Entities
  parseArtifactFile = "projects/parse/artifacts/:artifactType",
  parseTraceFile = "projects/parse/traces",

  //Trace Matrices
  createTraceMatrix = "projects/:projectId/matrices/:sourceArtifactTypeName/:targetArtifactTypeName",
  deleteTraceMatrix = "projects/matrices/:traceMatrixId",
  retrieveTraceMatrices = "projects/:projectId/matrices",
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

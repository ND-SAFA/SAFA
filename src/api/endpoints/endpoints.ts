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
  commit = "projects/versions/:versionId/commit",
  project = "projects",
  deleteArtifact = "projects/versions/:versionId/artifacts/:artifactName",
  isArtifactNameTaken = "projects/:projectId/artifacts/validate/:artifactName",
  getGeneratedLinks = "projects/:projectId/links/generated",
  generateLinks = "projects/links/generate",
  approveLink = "projects/links/:traceLinkId/approve",
  declineLink = "projects/links/:traceLinkId/decline",
  createLink = "projects/versions/:versionId/links/create/:sourceId/:targetId",
  createProjectFromFlatFiles = "projects/flat-files",
  updateProjectThroughFlatFiles = "projects/versions/:versionId/flat-files",
  projectVersion = "projects/versions/:versionId",
  updateProject = "projects/:projectId",
  getProjectVersions = "projects/:projectId/versions",
  getCurrentVersion = "projects/:projectId/versions/current",
  createNewMajorVersion = "projects/:projectId/versions/major",
  createNewMinorVersion = "projects/:projectId/versions/minor",
  createNewRevisionVersion = "projects/:projectId/versions/revision",
  getProjectDelta = "projects/delta/:sourceVersionId/:targetVersionId",
  parseArtifactFile = "projects/parse/artifacts/:artifactType",
  parseTraceFile = "projects/parse/traces",
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

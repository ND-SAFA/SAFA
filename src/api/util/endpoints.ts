/**
 * The base URL for the project
 */
export const BASE_URL = process.env.VUE_APP_API_ENDPOINT;

if (!process.env.VUE_APP_API_ENDPOINT) {
  console.error("API Endpoint environment variable not defined.");
}

/**
 * Returns a WebSocket url resolving function. Use only after all modules
 * have been loaded.
 * @constructor
 */
export const WEBSOCKET_URL = (): string => `${BASE_URL}/websocket`;

/**
 * Enumerates all possible endpoint paths.
 */
export enum Endpoint {
  // Accounts

  session = "accounts/session",
  login = "login",
  createAccount = "accounts/create",
  createVerifiedAccount = "accounts/create-verified",
  verifyAccount = "accounts/verify",
  logout = "logout",
  forgotPassword = "accounts/forgot",
  forgotPasswordAdmin = "accounts/forgot/no-email",
  resetPassword = "accounts/reset",
  updatePassword = "accounts/change",
  deleteAccount = "accounts/delete",
  getAccount = "accounts/self",
  editAccountOrg = "accounts/organization",

  // Admin

  setSuperuser = "accounts/superuser",
  activateSuperuser = "accounts/superuser/activate",
  deactivateSuperuser = "accounts/superuser/deactivate",
  onboardingStatistics = "statistics/onboarding",

  // Onboarding

  onboardingStatus = "onboarding",

  // Jobs

  createProjectJob = "jobs/projects",
  createProjectThroughFlatFiles = "jobs/projects/upload",
  updateProjectThroughFlatFiles = "jobs/projects/versions/:versionId",
  getUserJobs = "jobs/user",
  getProjectJobs = "jobs/project/:projectId",
  deleteJobById = "jobs/:jobId",
  getJobLog = "jobs/:jobId/logs",
  jobTopic = "/topic/jobs/:jobId",
  userTopic = "/user/:userId/updates",
  projectTopic = "/topic/project/:projectId",
  versionTopic = "/topic/version/:versionId",

  // Projects

  project = "projects",
  updateProject = "projects/:projectId",
  transferProject = "projects/:projectId/transfer",
  getTeamProjects = "projects/team/:teamId",

  // Project Members

  getProjectMembers = "projects/:projectId/members",
  updateProjectMember = "projects/:projectId/members",
  deleteProjectMember = "projects/members/:projectMemberId",

  // Integrations

  getInstallations = "projects/installations/by-project/:projectId",

  jiraCreateCredentials = "accounts/jira/credentials/:accessCode",
  jiraEditCredentials = "accounts/jira/credentials",
  jiraValidateCredentials = "accounts/jira/credentials/validate",
  jiraGetInstallations = "accounts/jira/installations",
  jiraGetProjects = "projects/jira/:cloudId",
  jiraCreateProject = "projects/import/jira/:cloudId/:id",
  jiraSyncProject = "projects/versions/:versionId/import/jira/:cloudId/:id",

  githubCreateCredentials = "accounts/github/credentials/:accessCode",
  githubEditCredentials = "accounts/github/credentials",
  githubValidateCredentials = "accounts/github/credentials/check",
  githubGetProjects = "integrations/github/repos",
  githubCreateProject = "projects/import/github/:owner/:repositoryName",
  githubSyncProject = "projects/versions/:versionId/import/github/:owner/:repositoryName",

  // Commits

  commit = "projects/versions/:versionId/commit",
  isArtifactNameTaken = "projects/versions/:versionId/artifacts/validate/",
  sync = "projects/versions/:versionId/changes",

  // Types

  createArtifactType = "projects/:projectId/artifactTypes",
  editArtifactType = "projects/:projectId/artifactTypes/:artifactTypeName",
  deleteArtifactType = "projects/:projectId/artifactTypes/:artifactTypeName",

  // Trace Matrices

  createTraceMatrix = "projects/:versionId/matrices/:sourceType/:targetType",
  deleteTraceMatrix = "projects/:versionId/matrices/:sourceType/:targetType",

  // Links

  getGeneratedLinks = "projects/versions/:versionId/links/generated",
  generateLinksJob = "jobs/projects/links/generate",
  trainModelJob = "jobs/projects/:projectId/models/train",

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

  // Attributes

  createAttribute = "projects/:projectId/attributes",
  editAttribute = "projects/:projectId/attributes/:key",
  createAttributeLayout = "projects/:projectId/attribute-layouts",
  editAttributeLayout = "projects/:projectId/attribute-layouts/:id",

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

  // Warnings

  getWarningsInProjectVersion = "projects/versions/:versionId/warnings",

  // Models

  getModels = "projects/:projectId/models",
  createModel = "projects/:projectId/models",
  editModel = "projects/:projectId/models/:modelId",
  deleteModel = "projects/:projectId/models/:modelId",
  shareModel = "projects/models/share",

  // Files

  getProjectFiles = "projects/versions/:versionId/flat-files/:fileType",

  // Search
  search = "search/:versionId",

  // Generation

  summarize = "projects/versions/:versionId/artifacts/summarize",
  prompt = "prompt",
  generateArtifacts = "hgen/:versionId",

  // Orgs

  getAllOrgs = "organizations",
  createOrg = "organizations",
  getPersonalOrg = "organizations/self",
  getOrg = "organizations/:orgId",
  editOrg = "organizations/:orgId",
  deleteOrg = "organizations/:orgId",

  createTeam = "organizations/:orgId/teams",
  editTeam = "organizations/:orgId/teams/:teamId",
  deleteTeam = "organizations/:orgId/teams/:teamId",

  getMembers = "members/:entityId",
  createMember = "members/:entityId",
  editMember = "members/:entityId/:memberId",
  deleteMember = "members/:entityId/:memberId",

  // Billing

  createCostEstimate = "hgen/:versionId/estimate",
  createCheckoutSession = "billing/checkout",
  setOrgPaymentTier = "billing/update-payment-tier",
  deleteCheckoutSession = "stripe/cancel/:sessionId",
  getAllTransactions = "billing/transactions/:orgId",
  getMonthlyTransactions = "billing/transactions/:orgId/month",

  // Comments, Flags, Health Checks

  getComments = "projects/versions/:versionId/comments/artifact/:artifactId",
  createComment = "projects/versions/:versionId/comments",
  editComment = "projects/versions/:versionId/comments/:commentId",
  deleteComment = "projects/versions/:versionId/comments/:commentId",
  resolveComment = "projects/versions/:versionId/comments/:commentId/resolve",
  generateHealthChecks = "projects/versions/:versionId/artifacts/health",

  // Chat

  createChat = "projects/versions/:versionId/chat",
  deleteChat = "projects/versions/:versionId/chat/:chatId",
  getChats = "projects/versions/:versionId/chat",
  getChatMessages = "projects/versions/:versionId/chat/:chatId",
  createChatMessage = "projects/versions/:versionId/chat/:chatId/message",
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
  endpoint: keyof typeof Endpoint,
  pathVariables: Record<string, string> = {}
): string {
  let filledPath: string = Endpoint[endpoint];

  Object.entries(pathVariables).forEach(([id, value]) => {
    filledPath = filledPath.replace(`:${id}`, value);
  });

  return filledPath;
}

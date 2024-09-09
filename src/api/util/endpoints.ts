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
  accountCreate = "accounts/create",
  accountCreateVerified = "accounts/create-verified",
  accountVerify = "accounts/verify",
  logout = "logout",
  accountForgot = "accounts/forgot",
  accountForgotAdmin = "accounts/forgot/no-email",
  accountReset = "accounts/reset",
  accountChange = "accounts/change",
  accountDelete = "accounts/delete",
  accountGet = "accounts/self",
  accountOrg = "accounts/organization",

  // Admin

  accountCollection = "accounts",

  superuser = "accounts/superuser",
  superuserActivate = "accounts/superuser/activate",
  superuserDeactivate = "accounts/superuser/deactivate",

  statisticsOnboarding = "statistics/onboarding",
  statisticsUser = "statistics/onboarding/:userId",

  // Onboarding

  onboardingStatus = "onboarding",

  // Jobs

  jobProjects = "jobs/projects",
  jobProjectsUpload = "jobs/projects/upload",
  jobProjectsVersion = "jobs/projects/versions/:versionId",
  jobsUser = "jobs/user",
  jobsProject = "jobs/project/:projectId",
  job = "jobs/:jobId",
  jobLogs = "jobs/:jobId/logs",
  topicJobs = "/topic/jobs/:jobId",
  topicProject = "/topic/project/:projectId",
  topicVersion = "/topic/version/:versionId",

  // Projects

  projectCollection = "projects",
  project = "projects/:projectId",
  projectTransfer = "projects/:projectId/transfer",
  projectTeam = "projects/team/:teamId",

  // Integrations

  projectInstallations = "projects/installations/by-project/:projectId",

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

  artifactTypeCollection = "projects/:projectId/artifactTypes",
  artifactType = "projects/:projectId/artifactTypes/:artifactTypeName",

  // Trace Matrices

  traceMatrix = "projects/:versionId/matrices/:sourceType/:targetType",

  // Links

  linksGenerated = "projects/versions/:versionId/links/generated",
  jobLinksGenerate = "jobs/projects/links/generate",

  // Entity Retrieval

  version = "projects/versions/:versionId",
  artifacts = "projects/versions/:versionId/artifacts",
  traces = "projects/versions/:versionId/traces",

  // Versions

  versionCollection = "projects/:projectId/versions",
  versionCurrent = "projects/:projectId/versions/current",
  versionMajor = "projects/:projectId/versions/major",
  versionMinor = "projects/:projectId/versions/minor",
  versionRevision = "projects/:projectId/versions/revision",

  // Attributes

  attributeCollection = "projects/:projectId/attributes",
  attribute = "projects/:projectId/attributes/:key",
  attributeLayoutCollection = "projects/:projectId/attribute-layouts",
  attributeLayout = "projects/:projectId/attribute-layouts/:id",

  // Layout

  layout = "projects/versions/:versionId/layout",

  // Documents

  viewCollection = "projects/versions/:versionId/documents",
  view = "projects/documents/:viewId",
  viewCurrent = "projects/documents/current/:viewId",
  viewCurrentClear = "projects/documents/current",

  // Delta

  delta = "projects/delta/:sourceVersionId/:targetVersionId",

  // Parse Entities

  parseArtifacts = "projects/parse/artifacts/:artifactType",
  parseTraces = "projects/parse/traces",

  // Files

  projectFiles = "projects/versions/:versionId/flat-files/:fileType",

  // Search

  search = "search/:versionId",

  // Generation

  summarize = "projects/versions/:versionId/artifacts/summarize",
  prompt = "prompt",
  generateArtifacts = "hgen/:versionId",

  // Orgs

  organizationCollection = "organizations",
  organizationSelf = "organizations/self",
  organization = "organizations/:orgId",

  teamCollection = "organizations/:orgId/teams",
  team = "organizations/:orgId/teams/:teamId",

  memberCollection = "members/:entityId",
  member = "members/:entityId/:memberId",
  memberInvite = "members/:entityId/invite",
  memberInviteAccept = "members/accept-invite",
  memberInviteDecline = "members/decline-invite",

  // Billing

  billingEstimate = "hgen/:versionId/estimate",
  billingCheckout = "billing/checkout",
  billingCheckoutDelete = "stripe/cancel/:sessionId",
  billingTier = "billing/update-payment-tier",
  transactions = "billing/transactions/:orgId",
  transactionsMonthly = "billing/transactions/:orgId/month",

  // Comments, Flags, Health Checks

  commentCollection = "comments/artifact/:artifactId",
  comment = "comments/:commentId",
  commentContent = "comments/:commentId/content",
  commentResolve = "comments/:commentId/resolve",
  healthChecks = "health",

  // Chat

  chatCollection = "chats",
  chat = "chats/:chatId",
  chatProject = "chats/projects/:projectId",
  chatTitle = "chats/:chatId/title",
  chatMessages = "chats/:chatId/messages",
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

/**
 * Enumerates the possible routes within the app.
 */
export enum Routes {
  LOGIN_ACCOUNT = "/login",
  CREATE_ACCOUNT = "/create-account",
  FORGOT_PASSWORD = "/forgot",
  RESET_PASSWORD = "/reset",
  HOME = "/",
  PROJECT_CREATOR = "/create",
  MY_PROJECTS = "/open",
  ARTIFACT = "/project",
  PROJECT_SETTINGS = "/settings",
  PROJECT_MODELS = "/models",
  TRACE_LINK = "/links",
  UPLOAD_STATUS = "/uploads",
  ACCOUNT = "/account",
  ERROR = "/error",
}

/**
 * Enumerates query parameters used in the app.
 */
export enum QueryParams {
  LOGIN_PATH = "to",
  PW_RESET = "token",
  TAB = "tab",
  VERSION = "version",
  JIRA_TOKEN = "code",
  GITHUB_TOKEN = "code",
}

export const routesWithRequiredProject: string[] = [
  Routes.PROJECT_SETTINGS,
  Routes.ARTIFACT,
  Routes.TRACE_LINK,
  Routes.PROJECT_MODELS,
];

export const routesPublic: string[] = [
  Routes.LOGIN_ACCOUNT,
  Routes.CREATE_ACCOUNT,
  Routes.FORGOT_PASSWORD,
  Routes.RESET_PASSWORD,
];

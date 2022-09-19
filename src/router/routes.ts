/**
 * Enumerates the possible routes within the app.
 */
export enum Routes {
  LOGIN_ACCOUNT = "/login",
  CREATE_ACCOUNT = "/create-account",
  FORGOT_PASSWORD = "/forgot",
  RESET_PASSWORD = "/reset",
  HOME = "/",
  ARTIFACT = "/project",
  PROJECT_SETTINGS = "/project/settings",
  TRACE_LINK = "/links",
  ERROR = "/error",
  PROJECT_CREATOR = "/create",
  UPLOAD_STATUS = "/uploads",
  ACCOUNT = "/account",
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
  Routes.TRACE_LINK,
  Routes.PROJECT_SETTINGS,
  Routes.ARTIFACT,
];

export const routesPublic: string[] = [
  Routes.LOGIN_ACCOUNT,
  Routes.CREATE_ACCOUNT,
  Routes.FORGOT_PASSWORD,
  Routes.RESET_PASSWORD,
];

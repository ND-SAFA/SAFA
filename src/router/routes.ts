/**
 * Enumerates the possible routes within the app.
 */
export enum Routes {
  LOGIN_ACCOUNT = "/login",
  CREATE_ACCOUNT = "/create-account",
  FORGOT_PASSWORD = "/forgot",
  RESET_PASSWORD = "/reset",
  HOME = "/",
  ARTIFACT_TREE = "/project",
  TRACE_LINK = "/links",
  ERROR = "/error",
  PROJECT_CREATOR = "/create",
  PROJECT_SETTINGS = "/project/settings",
}

export const routesWithRequiredProject: string[] = [
  Routes.TRACE_LINK,
  Routes.PROJECT_SETTINGS,
];

export const routesPublic: string[] = [
  Routes.LOGIN_ACCOUNT,
  Routes.CREATE_ACCOUNT,
  Routes.FORGOT_PASSWORD,
  Routes.RESET_PASSWORD,
];

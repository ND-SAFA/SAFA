import { RouteRecordRaw } from "vue-router";
import {
  ArtifactView,
  CreateAccountView,
  ErrorPageView,
  ForgotPasswordView,
  HomeView,
  LoginView,
  MyAccountView,
  ProjectCreatorView,
  ProjectSelectorView,
  ProjectSettingsView,
  ResetPasswordView,
  TracePredictionView,
  UploadStatusView,
} from "@/views";

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
];

export const routesPublic: string[] = [
  Routes.LOGIN_ACCOUNT,
  Routes.CREATE_ACCOUNT,
  Routes.FORGOT_PASSWORD,
  Routes.RESET_PASSWORD,
];
export const routes: Array<RouteRecordRaw> = [
  {
    path: Routes.LOGIN_ACCOUNT,
    name: "Login",
    component: LoginView,
  },
  {
    path: Routes.CREATE_ACCOUNT,
    name: "Create Account",
    component: CreateAccountView,
  },
  {
    path: Routes.FORGOT_PASSWORD,
    name: "Forgot Password",
    component: ForgotPasswordView,
  },
  {
    path: Routes.RESET_PASSWORD,
    name: "Reset Password",
    component: ResetPasswordView,
  },

  {
    path: Routes.HOME,
    name: "Home",
    component: HomeView,
  },
  {
    path: Routes.PROJECT_CREATOR,
    name: "Create Project",
    component: ProjectCreatorView,
  },
  {
    path: Routes.MY_PROJECTS,
    name: "My Projects",
    component: ProjectSelectorView,
  },
  {
    path: Routes.ACCOUNT,
    name: "My Account",
    component: MyAccountView,
  },
  {
    path: Routes.ARTIFACT,
    name: "Artifact View",
    component: ArtifactView,
  },
  {
    path: Routes.TRACE_LINK,
    name: "Trace Prediction",
    component: TracePredictionView,
  },
  {
    path: Routes.PROJECT_SETTINGS,
    name: "Project Settings",
    component: ProjectSettingsView,
  },
  {
    path: Routes.ERROR,
    name: "Error Page",
    component: ErrorPageView,
  },
  {
    path: Routes.UPLOAD_STATUS,
    name: "Upload Status",
    component: UploadStatusView,
  },
];

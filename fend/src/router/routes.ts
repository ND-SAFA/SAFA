import { RouteRecordRaw } from "vue-router";
import {
  ArtifactView,
  CreateAccountView,
  DemoView,
  ForgotPasswordView,
  HomeView,
  LoginView,
  MyAccountView,
  MyOrganizationView,
  ProjectCreatorView,
  ProjectSelectorView,
  ProjectSettingsView,
  ResetPasswordView,
  SearchView,
  UploadStatusView,
  MyTeamView,
  AdminView,
} from "@/views";

/**
 * Enumerates the possible routes within the app.
 */
export enum Routes {
  LOGIN_ACCOUNT = "/login",
  CREATE_ACCOUNT = "/create-account",
  VERIFY_ACCOUNT = "/verify-email",
  FORGOT_PASSWORD = "/forgot",
  RESET_PASSWORD = "/reset",
  HOME = "/",
  PROJECT_CREATOR = "/create",
  MY_PROJECTS = "/open",
  ARTIFACT = "/project",
  PROJECT_SETTINGS = "/settings",
  UPLOAD_STATUS = "/uploads",
  ACCOUNT = "/account",
  ORG = "/organization",
  TEAM = "/team",
  SEARCH = "/search",
  PAYMENT = "/payment",
  INVITE = "/accept-invite",

  ADMIN = "/admin",

  DEMO = "/demo",
}

/**
 * Enumerates query parameters used in the app.
 */
export enum QueryParams {
  LOGIN_PATH = "to",
  ACCOUNT_TOKEN = "token",
  INVITE_TOKEN = "token",
  TAB = "tab",
  VERSION = "version",
  VIEW = "view",
  ORG = "org",
  TEAM = "team",
  INTEGRATION_TOKEN = "code",
  PAYMENT_STATUS = "status",
  PAYMENT_SESSION = "session_id",
}

export const routes: Array<RouteRecordRaw> = [
  // Public
  {
    path: Routes.LOGIN_ACCOUNT,
    name: "Login",
    component: LoginView,
    meta: {
      isPublic: true,
    },
  },
  {
    path: Routes.CREATE_ACCOUNT,
    name: "Create Account",
    component: CreateAccountView,
    meta: {
      isPublic: true,
    },
  },
  {
    path: Routes.VERIFY_ACCOUNT,
    name: "Verify Account",
    component: CreateAccountView,
    meta: {
      isPublic: true,
    },
  },
  {
    path: Routes.FORGOT_PASSWORD,
    name: "Forgot Password",
    component: ForgotPasswordView,
    meta: {
      isPublic: true,
    },
  },
  {
    path: Routes.RESET_PASSWORD,
    name: "Reset Password",
    component: ResetPasswordView,
    meta: {
      isPublic: true,
    },
  },
  // Private
  {
    path: Routes.ACCOUNT,
    name: "My Account",
    component: MyAccountView,
    meta: {
      description:
        "Edit account settings such as your password, theme, and integrations.",
    },
  },
  {
    path: Routes.ORG,
    name: "My Organization",
    component: MyOrganizationView,
    meta: {
      description: "Manage organization members and teams.",
    },
  },
  {
    path: Routes.TEAM,
    name: "My Team",
    component: MyTeamView,
    meta: {
      description: "Manage team members and projects.",
    },
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
    meta: {
      description:
        "Create a new project by uploading files or configuring integrations.",
    },
  },
  {
    path: Routes.MY_PROJECTS,
    name: "My Projects",
    component: ProjectSelectorView,
    meta: {
      description:
        "Select a project and version to load, or view past uploads.",
    },
  },
  {
    path: Routes.UPLOAD_STATUS,
    name: "Upload Status",
    component: UploadStatusView,
  },
  {
    path: Routes.INVITE,
    name: "Accept Invite",
    component: HomeView,
  },
  // Project Specific
  {
    path: Routes.ARTIFACT,
    name: "Artifact View",
    component: ArtifactView,
    meta: {
      requiresProject: true,
    },
  },
  {
    path: Routes.PROJECT_SETTINGS,
    name: "Project Settings",
    component: ProjectSettingsView,
    meta: {
      requiresProject: true,
    },
  },
  {
    path: Routes.SEARCH,
    name: "Project Search",
    component: SearchView,
    meta: {
      requiresProject: true,
    },
  },
  {
    path: Routes.PAYMENT,
    name: "Billing",
    component: HomeView,
    meta: {
      requiresProject: true,
    },
  },
  // Admin
  {
    path: Routes.ADMIN,
    name: "Admin",
    component: AdminView,
    meta: {
      requiresSuperuser: true,
    },
  },
  // Demo
  {
    path: Routes.DEMO,
    name: "SAFA Demo",
    component: DemoView,
    meta: {
      isPublic: true,
    },
  },
];

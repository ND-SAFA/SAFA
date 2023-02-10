import { RouteRecordRaw, createRouter, createWebHistory } from "vue-router";
import { routerChecks } from "@/router/checks";
import {
  TracePredictionView,
  ArtifactView,
  CreateAccountView,
  ErrorPageView,
  ForgotPasswordView,
  LoginView,
  ProjectCreatorView,
  ProjectSettingsView,
  ResetPasswordView,
  UploadStatusView,
  HomeView,
  MyAccountView,
  ProjectSelectorView,
} from "@/views";
import { Routes } from "./routes";

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

export const router = createRouter({
  history: createWebHistory(),
  routes,
});

/**
 * Iterates through each router check and exits after the first check
 * uses the next function.
 */
router.beforeResolve((to, from, next) => {
  let exit = false;

  for (const check of Object.values(routerChecks)) {
    if (exit) return;

    check(to, from, (p) => {
      next(p);
      exit = true;
    });
  }
  next();
});

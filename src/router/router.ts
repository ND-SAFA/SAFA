import Vue from "vue";
import VueRouter, { NavigationGuardNext, Route, RouteConfig } from "vue-router";
import { Routes } from "./routes";
import {
  ApproveLinksView,
  ArtifactTreeView,
  CreateAccountView,
  ErrorPageView,
  ForgotPasswordView,
  LoginView,
  ProjectCreatorView,
  ProjectSettings,
  ResetPasswordView,
} from "@/views";
import { routerChecks } from "@/router/checks";
import { NextPayload } from "@/types";

export { Routes };

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
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
    component: ProjectCreatorView,
  },
  {
    path: Routes.ARTIFACT_TREE,
    name: "Artifact Tree",
    component: ArtifactTreeView,
  },
  {
    path: Routes.TRACE_LINK,
    name: "Trace Links",
    component: ApproveLinksView,
  },
  {
    path: Routes.PROJECT_CREATOR,
    name: "Project Creator",
    component: ProjectCreatorView,
  },
  {
    path: Routes.PROJECT_SETTINGS,
    name: "Project Settings",
    component: ProjectSettings,
  },
  {
    path: Routes.ERROR,
    name: "Error Page",
    component: ErrorPageView,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

/**
 * Iterates through each router checks and exits after the first check
 * uses the next function.
 */
router.beforeResolve((to: Route, from: Route, next: NavigationGuardNext) => {
  let exit = false;
  for (const check of Object.values(routerChecks)) {
    if (exit) return;
    check(to, from, (p: NextPayload) => {
      next(p);
      exit = true;
    });
  }
  next();
});

export default router;

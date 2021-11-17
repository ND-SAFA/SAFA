import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import { Routes } from "./routes";
import {
  ApproveLinksView,
  ArtifactTreeView,
  CreateAccountView,
  ErrorPageView,
  ForgotPasswordView,
  LoginView,
  ProjectCreatorView,
  ResetPasswordView,
} from "@/views";

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
 * Navigates app to given route, if app is already on the route then
 * does nothing. This wrapper stops DuplicateNavigation exceptions.
 *
 * @param route - The route to navigate to.
 */
export async function navigateTo(route: Routes): Promise<void> {
  if (router.currentRoute.path === route) {
    return;
  } else {
    await router.push(route);
  }
}
export default router;

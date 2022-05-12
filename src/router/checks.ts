import { PanelType, RouterCheck } from "@/types";
import { NavigationGuardNext, Route } from "vue-router";
import {
  QueryParams,
  Routes,
  routesPublic,
  routesWithRequiredProject,
} from "@/router/routes";
import { appModule, logModule, projectModule, sessionModule } from "@/store";
import { handleClearProject } from "@/api";

/**
 * Defines list of functions that are run before navigating to a new page.
 * This serves as the central location for setting any state a page might
 * expect to be in.
 *
 * Note, these checks are prioritized in the order they are defined meaning
 * that once a check has used the `next` function the remaining checks
 * are ignored.
 */
export const routerChecks: Record<string, RouterCheck> = {
  redirectToLoginIfNoSessionFound(
    to: Route,
    from: Route,
    next: NavigationGuardNext
  ) {
    if (sessionModule.getDoesSessionExist || routesPublic.includes(to.path)) {
      return;
    }

    next({
      path: Routes.LOGIN_ACCOUNT,
      query: {
        ...to.query,
        [QueryParams.LOGIN_PATH]: to.path,
      },
    });
  },
  requireProjectForRoutes(to: Route, from: Route, next: NavigationGuardNext) {
    if (
      projectModule.isProjectDefined ||
      !routesWithRequiredProject.includes(to.path)
    )
      return;

    logModule.onWarning("Please select a project.");
    next(Routes.HOME);
  },
  closePanelsIfNotInGraph(to: Route) {
    if (to.path === Routes.ARTIFACT) return;

    appModule.closePanel(PanelType.left);
    appModule.closePanel(PanelType.right);
  },
  clearProjectIfOpenCreate(to: Route) {
    if (to.path !== Routes.PROJECT_CREATOR) return;

    handleClearProject();
  },
};

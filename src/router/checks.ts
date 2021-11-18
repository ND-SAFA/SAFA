import { PanelType, RouterCheck } from "@/types";
import { NavigationGuardNext, Route } from "vue-router";
import {
  Routes,
  routesPublic,
  routesWithRequiredProject,
} from "@/router/routes";
import { appModule, projectModule } from "@/store";
import { sessionIsLoaded } from "@/store/modules/session.module";

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
    if (!routesPublic.includes(to.path) && !sessionIsLoaded) {
      next({ path: Routes.LOGIN_ACCOUNT, query: { to: to.path } });
      return;
    }
  },
  requireProjectForRoutes(to: Route, from: Route, next: NavigationGuardNext) {
    const isProjectDefined = projectModule.getProject.projectId !== "";
    if (routesWithRequiredProject.includes(to.path) && !isProjectDefined) {
      appModule.onWarning(
        "Project must be selected before approving trace links."
      );
      next(Routes.HOME);
    }
  },
  closePanelsIfNotInGraph(to: Route) {
    if (to.path !== Routes.ARTIFACT_TREE) {
      appModule.closePanel(PanelType.left);
      appModule.closePanel(PanelType.right);
    }
  },
};

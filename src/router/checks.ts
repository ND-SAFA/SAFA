import { NavigationGuardNext, Route } from "vue-router";
import { NavigationGuard } from "vue-router/types/router";
import { appStore, projectStore, sessionStore } from "@/hooks";
import { handleAuthentication, handleLoadVersion } from "@/api";
import {
  QueryParams,
  Routes,
  routesPublic,
  routesWithRequiredProject,
} from "@/router/routes";

/**
 * Defines list of functions that are run before navigating to a new page.
 * This serves as the central location for setting any state a page might
 * expect to be in.
 *
 * Note, these checks are prioritized in the order they are defined meaning
 * that once a check has used the `next` function the remaining checks
 * are ignored.
 */
export const routerChecks: Record<string, NavigationGuard> = {
  async redirectToLoginIfNoSessionFound(
    to: Route,
    from: Route,
    next: NavigationGuardNext
  ) {
    if (sessionStore.doesSessionExist || routesPublic.includes(to.path)) {
      return;
    }

    try {
      await handleAuthentication();

      return;
    } catch (e) {
      next({
        path: Routes.LOGIN_ACCOUNT,
        query: {
          ...to.query,
          [QueryParams.LOGIN_PATH]: to.path,
        },
      });
    }
  },
  requireProjectForRoutes(to: Route) {
    if (
      projectStore.isProjectDefined ||
      !routesWithRequiredProject.includes(to.path)
    )
      return;

    const versionId = to.query[QueryParams.VERSION];

    if (typeof versionId === "string") {
      handleLoadVersion(versionId, undefined, false);
    }
  },
  closePanelsIfNotInGraph(to: Route) {
    if (to.path === Routes.ARTIFACT) return;

    appStore.closeSidePanels();
  },
};

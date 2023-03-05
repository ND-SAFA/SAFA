import { RouteLocationNormalized, RouteLocationRaw } from "vue-router";
import { appStore, projectStore, sessionStore } from "@/hooks";
import { handleAuthentication, handleLoadVersion } from "@/api";
import { QueryParams, Routes } from "@/router/routes";

type RouteChecks = Record<
  string,
  (
    to: RouteLocationNormalized,
    from: RouteLocationNormalized
  ) => Promise<RouteLocationRaw | void>
>;

/**
 * Defines list of functions that are run before navigating to a new page.
 * This serves as the central location for setting any state a page might
 * expect to be in.
 *
 * Note, these checks are prioritized in the order they are defined meaning
 * that once a check has used the `next` function the remaining checks
 * are ignored.
 */
export const routerBeforeChecks: RouteChecks = {
  async redirectToLoginIfNoSessionFound(to) {
    const isPublic = to.matched.some(({ meta }) => meta.isPublic);

    if (sessionStore.doesSessionExist || isPublic) {
      return;
    }

    try {
      await handleAuthentication();

      return;
    } catch (e) {
      return {
        path: Routes.LOGIN_ACCOUNT,
        query: {
          ...to.query,
          [QueryParams.LOGIN_PATH]: to.path,
        },
      };
    }
  },
  async closePanelsIfNotInGraph(to) {
    if (to.path === Routes.ARTIFACT) return;

    appStore.closeSidePanels();
  },
};

export const routerAfterChecks: RouteChecks = {
  async requireProjectForRoutes(to) {
    const requiresProject = to.matched.some(({ meta }) => meta.requiresProject);

    if (projectStore.isProjectDefined || !requiresProject) return;

    const versionId = to.query[QueryParams.VERSION];

    if (typeof versionId !== "string") return;

    await handleLoadVersion(versionId, undefined, false);
  },
};

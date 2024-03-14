import { RouteLocationNormalized, RouteLocationRaw } from "vue-router";
import { PaymentStatus } from "@/types";
import {
  billingApiStore,
  getVersionApiStore,
  sessionApiStore,
} from "@/hooks/api";
import { appStore, sessionStore } from "@/hooks/core";
import {
  artifactStore,
  documentStore,
  projectStore,
  viewsStore,
} from "@/hooks/data";
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
  async resetPublicState(to) {
    const isPublic = to.matched.some(({ meta }) => meta.isPublic);

    if (!isPublic) return;

    sessionApiStore.handleReset();
  },
  async verifyEmail(to) {
    if (to.path !== Routes.VERIFY_ACCOUNT) return;

    const token = to.query[QueryParams.ACCOUNT_TOKEN];

    await sessionApiStore.handleVerifyAccount(String(token));

    return { path: Routes.HOME };
  },
  async redirectToLoginIfNoSessionFound(to) {
    const isPublic = to.matched.some(({ meta }) => meta.isPublic);
    let authenticated = false;

    if (sessionStore.doesSessionExist || isPublic) {
      return;
    }

    await sessionApiStore.handleAuthentication({
      onSuccess: () => (authenticated = true),
    });

    if (!authenticated) {
      // If not authenticated, redirect to login
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
  async acceptPayment(to) {
    if (to.path !== Routes.PAYMENT) return;

    const status = to.query[QueryParams.PAYMENT_STATUS];
    const sessionId = String(to.query[QueryParams.PAYMENT_SESSION]);

    if (status === PaymentStatus.success) {
      await billingApiStore.handleAcceptPayment();
    } else if (status === PaymentStatus.cancel) {
      await billingApiStore.handleCancelPayment(sessionId);
    }

    return { path: Routes.HOME };
  },
};

export const routerAfterChecks: RouteChecks = {
  async requireProjectForRoutes(to) {
    const requiresProject = to.matched.some(({ meta }) => meta.requiresProject);

    if (projectStore.isProjectDefined || !requiresProject) return;

    const versionId = to.query[QueryParams.VERSION];
    const viewId = to.query[QueryParams.VIEW];

    if (typeof versionId !== "string") return;

    await getVersionApiStore.handleLoad(versionId, undefined, false);

    if (!viewId) return;

    const artifact = artifactStore.artifactsById.get(String(viewId));
    const document = documentStore.allDocuments.find(
      ({ documentId }) => documentId === viewId
    );

    if (artifact) {
      await viewsStore.addDocumentOfNeighborhood(artifact);
    } else if (document) {
      await documentStore.switchDocuments(document);
    }
  },
};

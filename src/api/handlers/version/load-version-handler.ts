import { DocumentModel } from "@/types";
import { appStore, warningStore, sessionStore, documentStore } from "@/hooks";
import {
  navigateTo,
  QueryParams,
  router,
  Routes,
  routesWithRequiredProject,
} from "@/router";
import {
  getProjectVersion,
  handleSetProject,
  getWarningsInProjectVersion,
} from "@/api";

/**
 * Load the given project version of given Id. Navigates to the artifact
 * tree page in order to show the new project.
 *
 * @param versionId - The id of the version to retrieve and load.
 * @param document - The document to start with viewing.
 * @param doNavigate - Whether to navigate to the artifact tree if not already on an artifact page.
 */
export async function handleLoadVersion(
  versionId: string,
  document?: DocumentModel,
  doNavigate = true
): Promise<void> {
  appStore.onLoadStart();
  sessionStore.updateSession({ versionId });

  const navigateIfNeeded = async () => {
    if (
      !doNavigate ||
      routesWithRequiredProject.includes(router.currentRoute.path)
    )
      return;

    await navigateTo(Routes.ARTIFACT, { [QueryParams.VERSION]: versionId });
  };

  return getProjectVersion(versionId)
    .then(handleSetProject)
    .then(async () => {
      if (!document) return;

      await documentStore.switchDocuments(document);
    })
    .then(navigateIfNeeded)
    .finally(() => appStore.onLoadEnd());
}

/**
 * Call this function whenever warnings need to be re-downloaded.
 *
 * @param versionId - The project version to load from.
 */
export async function handleReloadWarnings(versionId: string): Promise<void> {
  warningStore.artifactWarnings = await getWarningsInProjectVersion(versionId);
}

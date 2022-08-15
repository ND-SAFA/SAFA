import {
  appModule,
  documentModule,
  errorModule,
  projectModule,
  sessionModule,
  viewportModule,
} from "@/store";
import {
  navigateTo,
  router,
  Routes,
  routesWithRequiredProject,
} from "@/router";
import {
  getArtifactsInVersion,
  getProjectVersion,
  getTracesInVersion,
  handleLoadTraceMatrices,
  handleSetProject,
  getWarningsInProjectVersion,
} from "@/api";
import { DocumentModel } from "@/types";

/**
 * Load the given project version of given Id. Navigates to the artifact
 * tree page in order to show the new project.
 *
 * @param versionId - The id of the version to retrieve and load.
 * @param document - The document to start with viewing.
 */
export async function handleLoadVersion(
  versionId: string,
  document?: DocumentModel
): Promise<void> {
  appModule.onLoadStart();
  await sessionModule.updateSession({ versionId });

  const navigateIfNeeded = async () => {
    if (routesWithRequiredProject.includes(router.currentRoute.path)) return;

    await navigateTo(Routes.ARTIFACT);
  };

  return navigateIfNeeded()
    .then(() => getProjectVersion(versionId))
    .then(handleSetProject)
    .then(async () => {
      if (!document) return;

      await documentModule.switchDocuments(document);
    })
    .finally(() => appModule.onLoadEnd());
}

/**
 * Call this function whenever artifacts need to be re-downloaded.
 * Reloads project artifacts for the given version.
 *
 * @param versionId - The project version to load from.
 */
export async function handleReloadArtifacts(versionId: string): Promise<void> {
  const artifacts = await getArtifactsInVersion(versionId);
  const currentArtifactCount = projectModule.getProject.artifacts.length;

  await projectModule.addOrUpdateArtifacts(artifacts);
  await handleLoadTraceMatrices();

  if (artifacts.length > currentArtifactCount) {
    await viewportModule.setArtifactTreeLayout();
  }
}

/**
 * Call this function whenever trace links need to be re-downloaded.
 * Reloads project traces for the given version.
 *
 * @param versionId - The project version to load from.
 */
export async function handleReloadTraceLinks(versionId: string): Promise<void> {
  const traces = await getTracesInVersion(versionId);

  await projectModule.addOrUpdateTraceLinks(traces);
  await handleLoadTraceMatrices();
  viewportModule.applyAutomove();
}

/**
 * Call this function whenever warnings need to be re-downloaded.
 *
 * @param versionId - The project version to load from.
 */
export async function handleReloadWarnings(versionId: string): Promise<void> {
  const warnings = await getWarningsInProjectVersion(versionId);

  errorModule.setArtifactWarnings(warnings);
}

import { appModule, traceModule, viewportModule } from "@/store";
import { navigateTo, Routes } from "@/router";
import { getProjectVersion, getTracesInVersion } from "@/api/endpoints";
import {
  reloadDocumentArtifacts,
  reloadTraceMatrices,
  setCreatedProject,
} from "@/api";
import { cyCenterNodes } from "@/cytoscape";

/**
 * Load the given project version of given Id. Navigates to the artifact
 * tree page in order to show the new project.
 *
 * @param lastVersionId The id of the version to retrieve and load.
 */
export async function loadVersionIfExistsHandler(
  lastVersionId: string | undefined
): Promise<void> {
  if (lastVersionId) {
    appModule.onLoadStart();

    return navigateTo(Routes.ARTIFACT_TREE)
      .then(() => getProjectVersion(lastVersionId))
      .then(setCreatedProject)
      .finally(appModule.onLoadEnd);
  }
}

/**
 * Call this function whenever artifacts need to be re-downloaded.
 * Reloads project artifacts for the given version.
 *
 * @param versionId - The project version ID of the revision.
 */
export async function reloadArtifactsHandler(versionId: string): Promise<void> {
  await reloadDocumentArtifacts(versionId);
  await reloadTraceMatrices();

  await viewportModule.setArtifactTreeLayout();
  cyCenterNodes();
}

/**
 * Call this function whenever trace links need to be re-downloaded.
 * Reloads project traces for the given version.
 *
 * @param versionId - The project version ID of the revision.
 */
export async function reloadTracesHandler(versionId: string): Promise<void> {
  const traces = await getTracesInVersion(versionId);

  await traceModule.addOrUpdateTraceLinks(traces);
  await reloadTraceMatrices();
}

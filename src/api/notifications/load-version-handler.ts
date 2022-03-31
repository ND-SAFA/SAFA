import { appModule, errorModule, projectModule, viewportModule } from "@/store";
import { navigateTo, QueryParams, Routes } from "@/router";
import {
  getArtifactsInVersion,
  getProjectVersion,
  getTracesInVersion,
} from "@/api/endpoints";
import { reloadTraceMatrices, setCreatedProject } from "@/api";
import { getWarningsInProjectVersion } from "@/api/endpoints/warning-api";

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

    return navigateTo(Routes.ARTIFACT, { [QueryParams.VERSION]: lastVersionId })
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
  const artifacts = await getArtifactsInVersion(versionId);
  const currentArtifactCount = projectModule.getProject.artifacts.length;

  await projectModule.addOrUpdateArtifacts(artifacts);
  await reloadTraceMatrices();

  if (artifacts.length > currentArtifactCount) {
    await viewportModule.setArtifactTreeLayout();
  }
}

/**
 * Call this function whenever trace links need to be re-downloaded.
 * Reloads project traces for the given version.
 *
 * @param versionId - The project version ID of the revision.
 */
export async function reloadTracesHandler(versionId: string): Promise<void> {
  const traces = await getTracesInVersion(versionId);

  await projectModule.addOrUpdateTraceLinks(traces);
  await reloadTraceMatrices();
  viewportModule.applyAutomove();
}

/**
 * Call this function whenever warnings need ot be re-downloaded.
 * @param versionId The id of whose versioned entities' warnings are updated.
 */
export async function reloadWarningsHandler(versionId: string): Promise<void> {
  const warnings = await getWarningsInProjectVersion(versionId);
  errorModule.setArtifactWarnings(warnings);
}

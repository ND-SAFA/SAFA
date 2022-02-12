import {
  appModule,
  artifactModule,
  documentModule,
  traceModule,
} from "@/store";
import { navigateTo, Routes } from "@/router";
import {
  getArtifactsInVersion,
  getProjectVersion,
  getTracesInVersion,
} from "@/api/endpoints";
import { setCreatedProject } from "./set-project-handler";
import { Frame } from "webstomp-client";
import { VersionMessage } from "@/types";

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
 * Reloads project artifacts for the given version.
 *
 * @param versionId - The project version ID of the revision.
 */
export async function reloadArtifactsHandler(versionId: string): Promise<void> {
  const artifacts = await getArtifactsInVersion(versionId);

  documentModule.defaultDocument.artifactIds = artifacts.map(({ id }) => id);

  await artifactModule.addOrUpdateArtifacts(artifacts);
}

/**
 * Reloads project traces for the given version.
 *
 * @param versionId - The project version ID of the revision.
 */
export async function reloadTracesHandler(versionId: string): Promise<void> {
  const traces = await getTracesInVersion(versionId);

  await traceModule.addOrUpdateTraceLinks(traces);
}

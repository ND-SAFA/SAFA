import { Project, ProjectCreationResponse } from "@/types";
import { createProject } from "@/util";
import {
  appModule,
  artifactSelectionModule,
  deltaModule,
  errorModule,
  projectModule,
  subtreeModule,
  viewportModule,
} from "@/store";
import { connectAndSubscribeToVersion } from "@/api/endpoints";
import { loadVersionIfExistsHandler } from "./load-version-if-exists-handler";

/**
 1. Sets a new project.
 2. Subscribes to the new project's version.
 3. Clears any deltas to previous projects and their settings.
 *
 * @param project - The project to set.
 */
export async function setAndSubscribeToProject(
  project: Project
): Promise<void> {
  const isDifferentProject =
    projectModule.getProject.projectId !== project.projectId;
  const projectId = project.projectId;
  const versionId = project.projectVersion?.versionId || "";

  await connectAndSubscribeToVersion(projectId, versionId);
  await artifactSelectionModule.clearSelections();
  projectModule.SAVE_PROJECT(project);

  if (isDifferentProject) {
    await subtreeModule.resetHiddenNodes();
    await viewportModule.setArtifactTreeLayout();
  }

  deltaModule.clearDelta();
  appModule.closeSidePanels();
  await subtreeModule.updateSubtreeMap();
  projectModule.updateAllowedTraceDirections();
  await subtreeModule.initializeProject(project);
}

export async function clearProject(): Promise<void> {
  await setAndSubscribeToProject(createProject());
}

/**
 * Sets a newly created project.
 * @param res - The created project and warnings.
 */
export async function setCreatedProject(
  res: ProjectCreationResponse
): Promise<void> {
  await setAndSubscribeToProject(res.project);
  errorModule.setArtifactWarnings(res.warnings);
}

/**
 * Reloads the current project.
 */
export async function reloadProject(): Promise<void> {
  await loadVersionIfExistsHandler(
    projectModule.getProject.projectVersion?.versionId
  );
}

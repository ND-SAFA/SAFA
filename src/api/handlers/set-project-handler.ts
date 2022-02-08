import { Project, ProjectCreationResponse } from "@/types";
import { createProject } from "@/util";
import {
  appModule,
  artifactSelectionModule,
  deltaModule,
  documentModule,
  errorModule,
  projectModule,
  subtreeModule,
  viewportModule,
} from "@/store";
import { connectAndSubscribeToVersion } from "@/api/endpoints";
import { cyCenterNodes, disableDrawMode } from "@/cytoscape";
import { loadVersionIfExistsHandler } from "./load-version-if-exists-handler";
import { reloadTraceMatrices } from "./trace-matrix-handler";

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
  const isDifferentProject = projectModule.projectId !== project.projectId;
  const projectId = project.projectId;
  const versionId = project.projectVersion?.versionId || "";

  await connectAndSubscribeToVersion(projectId, versionId);
  artifactSelectionModule.clearSelections();
  projectModule.SAVE_PROJECT(project);
  documentModule.initializeProject(project);

  if (isDifferentProject) {
    await subtreeModule.resetHiddenNodes();
    await viewportModule.setArtifactTreeLayout();
    cyCenterNodes();
  }

  disableDrawMode();
  deltaModule.clearDelta();
  appModule.closeSidePanels();
  await subtreeModule.initializeProject(project);
  await reloadTraceMatrices();
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
  await loadVersionIfExistsHandler(projectModule.versionId);
}

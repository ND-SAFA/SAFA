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
import { cyCenterNodes, disableDrawMode } from "@/cytoscape";
import { loadVersionIfExistsHandler } from "./load-version-handler";
import { reloadTraceMatrices } from "./trace-matrix-handler";
import { loadProjectDocuments } from "@/api";

/**
 * Resets graph state when some or all of a project gets reloaded.
 *
 * @param isDifferentProject - If true, all nodes will be unhidden and the viewport will be reset.
 */
export async function resetGraphFocus(
  isDifferentProject = true
): Promise<void> {
  if (isDifferentProject) {
    await subtreeModule.resetHiddenNodes();
    await viewportModule.setArtifactTreeLayout();
    cyCenterNodes();
  }

  disableDrawMode();
  artifactSelectionModule.clearSelections();
  deltaModule.clearDelta();
  appModule.closeSidePanels();
}

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
  await loadProjectDocuments(project);
  projectModule.initializeProject(project);
  await resetGraphFocus(isDifferentProject);
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

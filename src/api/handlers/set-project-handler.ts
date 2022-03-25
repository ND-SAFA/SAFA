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
import {
  connectAndSubscribeToVersion,
  reloadTraceMatrices,
  loadVersionIfExistsHandler,
} from "@/api";
import { disableDrawMode } from "@/cytoscape";

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
  await projectModule.initializeProject(project);
  await resetGraphFocus(isDifferentProject);
  await reloadTraceMatrices();
}

/**
 * Clears project store data.
 */
export async function clearProject(): Promise<void> {
  const project = createProject();

  await projectModule.initializeProject(project);
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
  const document = documentModule.document;

  await loadVersionIfExistsHandler(projectModule.versionId);
  await documentModule.switchDocuments(document);
}

import { Project } from "@/types";
import { createProject } from "@/util";
import { QueryParams, updateParam } from "@/router";
import {
  appModule,
  artifactSelectionModule,
  deltaModule,
  documentModule,
  errorModule,
  projectModule,
  subtreeModule,
  typeOptionsModule,
  viewportModule,
} from "@/store";
import {
  handleSelectVersion,
  handleLoadTraceMatrices,
  handleLoadVersion,
} from "@/api";
import { disableDrawMode } from "@/cytoscape";
import { getProjectArtifactTypes } from "@/api/endpoints/artifact-type-api";

/**
 * Resets graph state when some or all of a project gets reloaded.
 *
 * @param isDifferentProject - If true, all nodes will be unhidden and the viewport will be reset.
 */
export async function handleResetGraph(
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
export async function handleProjectSubscription(
  project: Project
): Promise<void> {
  const projectId = project.projectId;
  const versionId = project.projectVersion?.versionId || "";
  const isDifferentProject = projectModule.versionId !== versionId;

  project.artifactTypes = await getProjectArtifactTypes(projectId);

  await handleSelectVersion(projectId, versionId);
  await projectModule.initializeProject(project);
  await handleResetGraph(isDifferentProject);
  await handleLoadTraceMatrices();
  await updateParam(QueryParams.VERSION, versionId);
}

/**
 * Clears project store data.
 */
export async function handleClearProject(): Promise<void> {
  const project = createProject();

  await projectModule.initializeProject(project);
  await handleResetGraph();
  typeOptionsModule.clearData();
  await subtreeModule.clearSubtrees();
}

/**
 * Sets a newly created project.
 *
 * @param project - Project created containing entities.
 */
export async function handleSetProject(project: Project): Promise<void> {
  await handleProjectSubscription(project);
  errorModule.setArtifactWarnings(project.warnings);
}

/**
 * Reloads the current project.
 */
export async function handleReloadProject(): Promise<void> {
  const document = documentModule.document;

  await handleLoadVersion(projectModule.versionId);
  await documentModule.switchDocuments(document);
}

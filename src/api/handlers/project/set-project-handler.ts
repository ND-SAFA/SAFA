import { ProjectModel } from "@/types";
import { createProject } from "@/util";
import { QueryParams, removeParams, updateParam } from "@/router";
import {
  artifactSelectionModule,
  deltaModule,
  documentModule,
  errorModule,
  projectModule,
  subtreeModule,
  viewportModule,
} from "@/store";
import { appStore, typeOptionsStore } from "@/hooks";
import {
  handleLoadTraceMatrices,
  handleLoadVersion,
  handleSelectVersion,
} from "@/api";
import { disableDrawMode } from "@/cytoscape";
import { getProjectArtifactTypes } from "@/api/endpoints";

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
  appStore.closeSidePanels();
}

/**
 * Clears project store data.
 */
export async function handleClearProject(): Promise<void> {
  const project = createProject();

  await projectModule.initializeProject(project);
  await handleResetGraph();
  typeOptionsStore.clear();
  await subtreeModule.clearSubtrees();
  await removeParams();
}

/**
 * Sets a newly created project.
 *
 * @param project - Project created containing entities.
 */
export async function handleSetProject(project: ProjectModel): Promise<void> {
  const projectId = project.projectId;
  const versionId = project.projectVersion?.versionId || "";
  const isDifferentProject = projectModule.versionId !== versionId;

  project.artifactTypes = await getProjectArtifactTypes(projectId);

  await handleSelectVersion(projectId, versionId);
  artifactSelectionModule.clearSelections();
  await projectModule.initializeProject(project);
  await handleResetGraph(isDifferentProject);
  await handleLoadTraceMatrices();
  errorModule.setArtifactWarnings(project.warnings);
  await setCurrentDocument(project);
  await updateParam(QueryParams.VERSION, versionId);
}

/**
 * Reloads the current project.
 */
export async function handleReloadProject(): Promise<void> {
  await handleLoadVersion(projectModule.versionId, documentModule.document);
}

/**
 * Moves user to the document if one is set by currentDocumentId
 * Otherwise default document would continue to be in view.
 * @param project The project possibly containing a currentDocumentId.
 */
async function setCurrentDocument(project: ProjectModel): Promise<void> {
  if (project.currentDocumentId) {
    const documents = project.documents.filter(
      (d) => d.documentId === project.currentDocumentId
    );
    if (documents.length === 1) {
      const document = documents[0];
      await documentModule.switchDocuments(document);
    }
  }
}

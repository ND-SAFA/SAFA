import { ProjectModel } from "@/types";
import { createProject } from "@/util";
import { QueryParams, removeParams, updateParam } from "@/router";
import {
  appStore,
  layoutStore,
  typeOptionsStore,
  documentStore,
  deltaStore,
  subtreeStore,
  projectStore,
  selectionStore,
} from "@/hooks";
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
    await subtreeStore.resetHiddenNodes();
    await layoutStore.setArtifactTreeLayout();
  }

  disableDrawMode();
  selectionStore.clearSelections();
  deltaStore.clear();
  appStore.closeSidePanels();
}

/**
 * Clears project store data.
 */
export async function handleClearProject(): Promise<void> {
  const project = createProject();

  projectStore.initializeProject(project);
  await handleResetGraph();
  typeOptionsStore.$reset();
  subtreeStore.$reset();
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
  const isDifferentProject = projectStore.versionId !== versionId;

  project.artifactTypes = await getProjectArtifactTypes(projectId);

  await handleSelectVersion(projectId, versionId);
  selectionStore.clearSelections();
  projectStore.initializeProject(project);
  await handleResetGraph(isDifferentProject);
  await handleLoadTraceMatrices();
  await setCurrentDocument(project);
  await updateParam(QueryParams.VERSION, versionId);
}

/**
 * Reloads the current project.
 */
export async function handleReloadProject(): Promise<void> {
  await handleLoadVersion(
    projectStore.versionId,
    documentStore.currentDocument
  );
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
      await documentStore.switchDocuments(document);
    }
  }
}

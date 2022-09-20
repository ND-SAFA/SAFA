import { ProjectModel } from "@/types";
import { createProject } from "@/util";
import { documentStore, subtreeStore, projectStore } from "@/hooks";
import { QueryParams, removeParams, updateParam } from "@/router";
import {
  handleLoadModels,
  handleLoadTraceMatrices,
  handleLoadVersion,
  handleSelectVersion,
} from "@/api";
import { getProjectArtifactTypes } from "@/api/endpoints";

/**
 * Clears project store data.
 */
export async function handleClearProject(): Promise<void> {
  const project = createProject();

  projectStore.initializeProject(project);
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

  project.artifactTypes = await getProjectArtifactTypes(projectId);
  projectStore.initializeProject(project);

  await handleSelectVersion(projectId, versionId);
  await handleLoadTraceMatrices();
  await setCurrentDocument(project);
  await handleLoadModels();
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
 * Moves user to the document if one is set by currentDocumentId.
 * Otherwise default document would continue to be in view.
 *
 * @param project The project possibly containing a currentDocumentId.
 */
async function setCurrentDocument(project: ProjectModel): Promise<void> {
  if (!project.currentDocumentId) return;

  const document = project.documents.find(
    (d) => d.documentId === project.currentDocumentId
  );

  if (!document) return;

  await documentStore.switchDocuments(document);
}

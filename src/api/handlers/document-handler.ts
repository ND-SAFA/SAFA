import { documentModule, projectModule } from "@/store";
import { Project, ProjectDocument } from "@/types";
import {
  createOrUpdateDocument,
  deleteDocument,
  getProjectDocuments,
} from "@/api/endpoints/document-api";
import { createDocument } from "@/util";
import { reloadArtifactsHandler } from "@/api";

/**
 * Adds documents to the given project object.
 *
 * @param project - The project to load documents for.
 */
export async function loadProjectDocuments(
  project: Project = projectModule.getProject
): Promise<void> {
  project.documents = await getProjectDocuments(project.projectId).catch(
    () => []
  );
}

/**
 * Creates a new document.
 *
 * @param documentName - The document name create.
 * @param artifactIds - The artifacts shown in the document.
 */
export async function addNewDocument(
  documentName: string,
  artifactIds: string[]
): Promise<void> {
  const versionId = projectModule.versionIdWithLog;

  if (!versionId) return;

  const createdDocument = await createOrUpdateDocument(
    versionId,
    createDocument(projectModule.getProject, artifactIds, documentName)
  );

  await documentModule.addDocument(createdDocument);
}

/**
 * Edits an existing document.
 *
 * @param document - The document to edit.
 */
export async function editDocument(document: ProjectDocument): Promise<void> {
  const versionId = projectModule.versionIdWithLog;

  if (!versionId) return;

  await createOrUpdateDocument(versionId, document);

  if (documentModule.document === document) {
    await documentModule.switchDocuments(document);
  }
}

/**
 * Deletes the document and switches document's if this one was visible.
 *
 * @param document - The document to delete.
 */
export async function deleteAndSwitchDocuments(
  document: ProjectDocument
): Promise<void> {
  await deleteDocument(document);
  await documentModule.removeDocument(document);
}

/**
 * Updates the artifact IDs for the currently loaded document,
 * and then reloads the project artifacts.
 */
export async function reloadDocumentArtifacts(): Promise<void> {
  const currentDocument = documentModule.document;

  if (currentDocument.documentId) {
    (await getProjectDocuments(projectModule.projectId)).forEach(
      (updatedDocument) => {
        if (updatedDocument.documentId !== currentDocument.documentId) return;

        currentDocument.artifactIds = updatedDocument.artifactIds;
      }
    );
  }

  if (!projectModule.versionId) return;

  await reloadArtifactsHandler(projectModule.versionId);
}

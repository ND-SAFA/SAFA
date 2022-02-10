import { documentModule, projectModule } from "@/store";
import { Project, ProjectDocument } from "@/types";
import {
  createOrUpdateDocument,
  getProjectDocuments,
} from "@/api/endpoints/document-api";

/**
 * Adds documents to the given project object.
 *
 * @param project - The project to load documents for.
 */
export async function loadProjectDocuments(project: Project): Promise<void> {
  project.documents = await getProjectDocuments(project.projectId).catch(
    () => []
  );
}

/**
 * Creates a new document.
 *
 * @param document - The document to create.
 */
export async function addNewDocument(document: ProjectDocument): Promise<void> {
  const createdDocument = await createOrUpdateDocument(
    projectModule.projectId,
    document
  );

  documentModule.addDocument(createdDocument);
}

/**
 * Edits an existing document.
 *
 * @param document - The document to edit.
 */
export async function editDocument(document: ProjectDocument): Promise<void> {
  await createOrUpdateDocument(projectModule.projectId, document);
}

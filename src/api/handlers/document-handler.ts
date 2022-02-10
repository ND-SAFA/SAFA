import { documentModule, projectModule } from "@/store";
import { ProjectDocument } from "@/types";
import { createOrUpdateDocument } from "@/api/endpoints/document-api";

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

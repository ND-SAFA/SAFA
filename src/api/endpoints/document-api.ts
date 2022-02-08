import { Project } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Creates given document under project specified.
 * @param project The project to create the document under.
 * @param document The document to be created.
 */
export async function createOrUpdateDocument(
  project: Project,
  document: Document
): Promise<Document> {
  const url = fillEndpoint(Endpoint.createOrUpdateDocument, {
    projectId: project.projectId,
  });
  return authHttpClient<Document>(url, {
    method: "POST",
    body: JSON.stringify(document),
  });
}

/**
 * Returns list of documents associated with given project.
 * @param project The project whose documents are retrieved.
 */
export async function retrieveProjectDocuments(
  project: Project
): Promise<Document[]> {
  const url = fillEndpoint(Endpoint.getProjectDocuments, {
    projectId: project.projectId,
  });
  return authHttpClient<Document[]>(url, {
    method: "GET",
  });
}

/**
 * Deletes the given document from the database. User must have edit
 * permissions on the project.
 * @param document The document to be deleted.
 */
export async function deleteDocument(document: Document): Promise<void> {
  const url = fillEndpoint(Endpoint.deleteDocument, {
    documentId: document.documentURI,
  });
  return authHttpClient<void>(url, {
    method: "DELETE",
  });
}

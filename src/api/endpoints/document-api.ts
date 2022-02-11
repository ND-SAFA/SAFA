import { Artifact, Project, ProjectDocument } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Creates given document under project specified.
 * @param projectId - The project to create the document under.
 * @param document The document to be created.
 */
export async function createOrUpdateDocument(
  projectId: string,
  document: ProjectDocument
): Promise<ProjectDocument> {
  const url = fillEndpoint(Endpoint.createOrUpdateDocument, {
    projectId,
  });
  return authHttpClient<ProjectDocument>(url, {
    method: "POST",
    body: JSON.stringify(document),
  });
}

/**
 * Returns list of documents associated with given project.
 * @param projectId The UUID of the project whose documents are retrieved.
 */
export async function getProjectDocuments(
  projectId: string
): Promise<ProjectDocument[]> {
  const url = fillEndpoint(Endpoint.getProjectDocuments, {
    projectId,
  });
  return authHttpClient<ProjectDocument[]>(url, {
    method: "GET",
  });
}

/**
 * Deletes the given document from the database. User must have edit
 * permissions on the project.
 * @param document The document to be deleted.
 */
export async function deleteDocument(
  document: ProjectDocument
): Promise<ProjectDocument> {
  const url = fillEndpoint(Endpoint.deleteDocument, {
    documentId: document.documentId,
  });

  await authHttpClient<void>(url, {
    method: "DELETE",
  });

  return document;
}

/**
 * Attaches the given artifact to specified document marked at the
 * given version.
 * @param versionId The id of the version to mark the addition to.
 * @param documentId The id of the document to which the artifacts are added to.
 * @param artifacts The artifacts being added to the document.
 */
export async function addArtifactToDocument(
  versionId: string,
  documentId: string,
  artifacts: Artifact[]
): Promise<Artifact[]> {
  const url = fillEndpoint(Endpoint.addArtifactsToDocument, {
    versionId,
    documentId,
  });
  return authHttpClient<Artifact[]>(url, {
    method: "POST",
    body: JSON.stringify(artifacts),
  });
}

/**
 * Removed specified artifact from document marked at given
 * version.
 * @param versionId The version to mark the removal at.
 * @param documentId The document to remove the artifacts to.
 * @param artifactId The artifact to remove from the document.
 */
export async function removeArtifactFromDocument(
  versionId: string,
  documentId: string,
  artifactId: string
): Promise<void> {
  const url = fillEndpoint(Endpoint.removeArtifactFromDocument, {
    versionId,
    documentId,
    artifactId,
  });
  return authHttpClient<void>(url, {
    method: "DELETE",
  });
}

import { TraceLink } from "@/types";
import httpClient from "@/api/http-client";
import { Artifact } from "@/types/domain/artifact";
import { Endpoint, fillEndpoint } from "@/api/endpoints";

/**
 * Returns all generated links for this project.
 *
 * @param projectId - The project ID to return links for.
 *
 * @return The generated links.
 */
export async function getGeneratedLinks(
  projectId: string
): Promise<TraceLink[]> {
  return httpClient<TraceLink[]>(
    fillEndpoint(Endpoint.getGeneratedLinks, { projectId }),
    { method: "GET" }
  );
}

/**
 * Generates links from the source to target artifacts.
 *
 * @param sourceArtifacts - The artifacts to generate links from.
 * @param targetArtifacts - The artifacts to generate links to.
 *
 * @return All generated links.
 */
export async function generateLinks(
  sourceArtifacts: Artifact[],
  targetArtifacts: Artifact[]
): Promise<TraceLink[]> {
  const payload = { sourceArtifacts, targetArtifacts };

  return httpClient<TraceLink[]>(fillEndpoint(Endpoint.generateLinks), {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

/**
 * Approves the given trace link ID.
 *
 * @param traceLinkId - The trace link ID to approve.
 */
export async function approveLink(traceLinkId: string): Promise<void> {
  return httpClient<void>(fillEndpoint(Endpoint.approveLink, { traceLinkId }), {
    method: "PUT",
  });
}

/**
 * Declines the given trace link ID.
 *
 * @param traceLinkId - The trace link ID to decline.
 */
export async function declineLink(traceLinkId: string): Promise<void> {
  return httpClient<void>(fillEndpoint(Endpoint.declineLink, { traceLinkId }), {
    method: "PUT",
  });
}

/**
 * Creates a trace link from the source to the target ID for the given version ID.
 *
 * @param versionId - The version ID for this trace.
 * @param sourceId - The source ID to link from.
 * @param targetId - The target ID to link to.
 *
 * @return The created trace link.
 */
export async function createLink(
  versionId: string,
  sourceId: string,
  targetId: string
): Promise<TraceLink> {
  return httpClient<TraceLink>(
    fillEndpoint(Endpoint.createLink, { versionId, sourceId, targetId }),
    { method: "POST" }
  );
}

import { TraceApproval, TraceLink } from "@/types";
import authHttpClient from "@/api/endpoints/auth-http-client";
import { Artifact } from "@/types/domain/artifact";
import { Endpoint, fillEndpoint } from "@/api/endpoints/endpoints";
import { CommitBuilder } from "@/util/commit-builder";

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
  return authHttpClient<TraceLink[]>(
    fillEndpoint(Endpoint.getGeneratedLinks, { projectId }),
    { method: "GET" }
  );
}

/**
 * Generates links between source and target artifacts.
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

  return authHttpClient<TraceLink[]>(fillEndpoint(Endpoint.generateLinks), {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

/**
 * Approves the given trace link ID.
 *
 * @param traceLink - The trace link to approve.
 */
export async function approveLink(traceLink: TraceLink): Promise<void> {
  traceLink.approvalStatus = TraceApproval.APPROVED;
  return CommitBuilder.withCurrentVersion()
    .withModifiedTraceLink(traceLink)
    .save();
}

/**
 * Declines the given trace link ID.
 *
 * @param traceLink - The trace link to decline.
 */
export async function declineLink(traceLink: TraceLink): Promise<void> {
  traceLink.approvalStatus = TraceApproval.DECLINED;
  return CommitBuilder.withCurrentVersion()
    .withModifiedTraceLink(traceLink)
    .save();
}

/**
 * Creates a trace link from the source to the target ID for the given version ID.
 *
 * @param traceLink - The trace link to persist.
 *
 * @return The created trace link.
 */
export async function createLink(traceLink: TraceLink): Promise<void> {
  traceLink.approvalStatus = TraceApproval.DECLINED;
  return CommitBuilder.withCurrentVersion().withNewTraceLink(traceLink).save();
}

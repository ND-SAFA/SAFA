import { ApprovalType, TraceLinkModel, ArtifactModel } from "@/types";
import { Endpoint, fillEndpoint, authHttpClient } from "@/api/util";
import { CommitBuilder } from "@/api";

/**
 * Returns all generated links for this project.
 *
 * @param versionId - The project version id whose related links are retrieved.
 * @return The generated links.
 */
export async function getGeneratedLinks(
  versionId: string
): Promise<TraceLinkModel[]> {
  return authHttpClient<TraceLinkModel[]>(
    fillEndpoint(Endpoint.getGeneratedLinks, { versionId }),
    { method: "GET" }
  );
}

/**
 * Generates links between source and target artifacts.
 *
 * @param sourceArtifacts - The artifacts to generate links from.
 * @param targetArtifacts - The artifacts to generate links to.
 * @return All generated links.
 */
export async function createGeneratedLinks(
  sourceArtifacts: ArtifactModel[],
  targetArtifacts: ArtifactModel[]
): Promise<TraceLinkModel[]> {
  const payload = { sourceArtifacts, targetArtifacts };

  return authHttpClient<TraceLinkModel[]>(
    fillEndpoint(Endpoint.generateLinks),
    {
      method: "POST",
      body: JSON.stringify(payload),
    }
  );
}

/**
 * Approves the given trace link ID.
 *
 * @param traceLink - The trace link to approve.
 * @return The modified trace links.
 */
export async function updateApprovedLink(
  traceLink: TraceLinkModel
): Promise<TraceLinkModel[]> {
  traceLink.approvalStatus = ApprovalType.APPROVED;
  return CommitBuilder.withCurrentVersion()
    .withModifiedTraceLink(traceLink)
    .save()
    .then(async ({ traces }) => traces.modified);
}

/**
 * Declines the given trace link ID.
 *
 * @param traceLink - The trace link to decline.
 * @return The removed trace links.
 */
export async function updateDeclinedLink(
  traceLink: TraceLinkModel
): Promise<TraceLinkModel[]> {
  traceLink.approvalStatus = ApprovalType.DECLINED;
  return CommitBuilder.withCurrentVersion()
    .withModifiedTraceLink(traceLink)
    .save()
    .then(async ({ traces }) => traces.removed);
}

/**
 * Creates a trace link from the source to the target ID for the given version ID.
 *
 * @param traceLink - The trace link to persist.
 * @return The created trace links.
 */
export async function createLink(
  traceLink: TraceLinkModel
): Promise<TraceLinkModel[]> {
  traceLink.approvalStatus = ApprovalType.APPROVED;
  return CommitBuilder.withCurrentVersion()
    .withNewTraceLink(traceLink)
    .save()
    .then(async ({ traces }) => traces.added);
}

import {
  ApprovalType,
  JobModel,
  TraceLinkModel,
  TrainOrGenerateLinksModel,
} from "@/types";
import { CommitBuilder } from "@/api";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api/util";

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
 * @param config - Generated link configuration.
 * @return The created job.
 */
export async function createGeneratedLinks(
  config: TrainOrGenerateLinksModel
): Promise<JobModel> {
  return authHttpClient<JobModel>(fillEndpoint(Endpoint.generateLinksJob), {
    method: "POST",
    body: JSON.stringify(config),
  });
}

/**
 * Trains a model between source and target artifacts.
 *
 * @param projectId - The project to train for.
 * @param config - Model training configuration.
 * @return The created job.
 */
export async function createModelTraining(
  projectId: string,
  config: TrainOrGenerateLinksModel
): Promise<JobModel> {
  return authHttpClient<JobModel>(
    fillEndpoint(Endpoint.trainModelJob, { projectId }),
    {
      method: "POST",
      body: JSON.stringify(config),
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
  traceLink = {
    ...traceLink,
    approvalStatus: ApprovalType.APPROVED,
  };

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
  traceLink = {
    ...traceLink,
    approvalStatus: ApprovalType.DECLINED,
  };

  return CommitBuilder.withCurrentVersion()
    .withModifiedTraceLink(traceLink)
    .save()
    .then(async ({ traces }) => traces.modified);
}

/**
 * Declines all given links.
 *
 * @param traceLinks - The trace links to decline.
 * @return The removed trace links.
 */
export async function updateDeclinedLinks(
  traceLinks: TraceLinkModel[]
): Promise<TraceLinkModel[]> {
  traceLinks = traceLinks.map((link) => ({
    ...link,
    approvalStatus: ApprovalType.DECLINED,
  }));

  return CommitBuilder.withCurrentVersion()
    .withModifiedTraceLinks(traceLinks)
    .save()
    .then(async ({ traces }) => traces.modified);
}

/**
 * Declines the given trace link ID.
 *
 * @param traceLink - The trace link to decline.
 * @return The removed trace links.
 */
export async function updateUnreviewedLink(
  traceLink: TraceLinkModel
): Promise<TraceLinkModel[]> {
  traceLink = {
    ...traceLink,
    approvalStatus: ApprovalType.UNREVIEWED,
  };

  return CommitBuilder.withCurrentVersion()
    .withModifiedTraceLink(traceLink)
    .save()
    .then(async ({ traces }) => traces.modified);
}

/**
 * Creates new trace links.
 *
 * @param traceLink - The trace link to persist.
 * @return The created trace links.
 */
export async function createLink(
  traceLink: TraceLinkModel
): Promise<TraceLinkModel[]> {
  traceLink = {
    ...traceLink,
    approvalStatus: ApprovalType.APPROVED,
  };

  return CommitBuilder.withCurrentVersion()
    .withNewTraceLink(traceLink)
    .save()
    .then(async ({ traces }) => traces.added);
}

/**
 * Saves new generated trace links.
 *
 * @param traceLinks - The trace links to persist.
 * @return The created trace links.
 */
export async function saveGeneratedLinks(
  traceLinks: TraceLinkModel[]
): Promise<TraceLinkModel[]> {
  return CommitBuilder.withCurrentVersion()
    .hideErrors()
    .withNewTraceLinks(traceLinks)
    .save()
    .then(async ({ traces }) => traces.added);
}

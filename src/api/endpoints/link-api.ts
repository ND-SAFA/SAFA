import {
  JobSchema,
  TraceLinkSchema,
  TrainOrGenerateLinksSchema,
} from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api/util";

/**
 * Returns all generated links for this project.
 *
 * @param versionId - The project version id whose related links are retrieved.
 * @return The generated links.
 */
export async function getGeneratedLinks(
  versionId: string
): Promise<TraceLinkSchema[]> {
  return authHttpClient<TraceLinkSchema[]>(
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
  config: TrainOrGenerateLinksSchema
): Promise<JobSchema> {
  return authHttpClient<JobSchema>(fillEndpoint(Endpoint.generateLinksJob), {
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
  config: TrainOrGenerateLinksSchema
): Promise<JobSchema> {
  return authHttpClient<JobSchema>(
    fillEndpoint(Endpoint.trainModelJob, { projectId }),
    {
      method: "POST",
      body: JSON.stringify(config),
    }
  );
}

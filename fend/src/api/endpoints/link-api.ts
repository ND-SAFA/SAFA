import { JobSchema, TraceLinkSchema, GenerateLinksSchema } from "@/types";
import { buildRequest } from "@/api/util";

/**
 * Returns all generated links for this project.
 *
 * @param versionId - The project version id whose related links are retrieved.
 * @return The generated links.
 */
export async function getGeneratedLinks(
  versionId: string
): Promise<TraceLinkSchema[]> {
  return buildRequest<TraceLinkSchema[], "versionId">("linksGenerated", {
    versionId,
  }).get();
}

/**
 * Generates links between source and target artifacts.
 *
 * @param config - Generated link configuration.
 * @return The created job.
 */
export async function createGeneratedLinks(
  config: GenerateLinksSchema
): Promise<JobSchema> {
  return buildRequest<JobSchema, string, GenerateLinksSchema>(
    "jobLinksGenerate"
  ).post(config);
}

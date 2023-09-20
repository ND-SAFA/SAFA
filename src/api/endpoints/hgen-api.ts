import { GenerateArtifactSchema, JobSchema } from "@/types";
import { buildRequest } from "@/api";

/**
 * Generates parent artifacts from child artifacts.
 *
 * @param config - The configuration for generating the artifacts.
 * @param versionId - The version to generate the artifacts for.
 * @returns The created commit with artifacts and traces.
 */
export function createGeneratedArtifacts(
  config: GenerateArtifactSchema,
  versionId: string
): Promise<JobSchema> {
  return buildRequest<JobSchema, "versionId", GenerateArtifactSchema>(
    "generateArtifacts",
    { versionId }
  ).post(config);
}

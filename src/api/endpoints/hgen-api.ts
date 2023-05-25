import { CommitSchema, GenerateArtifactSchema } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

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
): Promise<CommitSchema> {
  return authHttpClient<CommitSchema>(
    fillEndpoint(Endpoint.generateArtifacts, { versionId }),
    {
      method: "POST",
      body: JSON.stringify(config),
    }
  );
}

import { ArtifactSchema } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Generates a summary for an artifact.
 *
 * @param artifact - The artifact to summarize.
 * @return The artifact summary.
 */
export async function createSummary(artifact: ArtifactSchema): Promise<string> {
  const summaries = await authHttpClient<string[]>(
    fillEndpoint(Endpoint.summarize),
    {
      method: "POST",
      body: JSON.stringify({
        artifacts: [
          {
            name: artifact.name,
            content: artifact.body,
          },
        ],
      }),
    }
  );

  return summaries[0] || "";
}

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
      body: JSON.stringify([
        {
          content: artifact.body,
          type: "NL",
        },
      ]),
    }
  );

  return summaries[0] || "";
}

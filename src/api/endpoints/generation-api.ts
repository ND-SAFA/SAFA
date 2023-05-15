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

/**
 * Generates a response based on a prompt.
 *
 * @param prompt - The prompt to generate with.
 * @return The response based on the prompt.
 */
export async function createPrompt(prompt: string): Promise<string> {
  const { completion } = await authHttpClient<{ completion: string }>(
    fillEndpoint(Endpoint.prompt),
    {
      method: "POST",
      body: JSON.stringify({ prompt }),
    }
  );

  return completion;
}

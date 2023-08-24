import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Generates a summary for an artifact.
 *
 * @param artifact - The artifact to summarize.
 * @return The artifact summary.
 */
export async function createSummary(
  versionId: string,
  artifactId: string
): Promise<string> {
  const summaries = await authHttpClient<string[]>(
    fillEndpoint(Endpoint.summarize, { versionId }),
    {
      method: "POST",
      body: JSON.stringify({
        artifacts: [artifactId],
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

import { buildRequest } from "@/api";

/**
 * Generates a summary for an artifact.
 *
 * @param versionId - The project version to update.
 * @param artifactId - The artifact to summarize.
 * @return The artifact summary.
 */
export async function createSummary(
  versionId: string,
  artifactId: string
): Promise<string> {
  const summaries = await buildRequest<
    string[],
    "versionId",
    { artifacts: string[] }
  >("summarize", { versionId }).post({
    artifacts: [artifactId],
  });

  return summaries[0] || "";
}

/**
 * Generates a response based on a prompt.
 *
 * @param prompt - The prompt to generate with.
 * @return The response based on the prompt.
 */
export async function createPrompt(prompt: string): Promise<string> {
  const { completion } = await buildRequest<
    { completion: string },
    string,
    { prompt: string }
  >("prompt").post({ prompt });

  return completion;
}

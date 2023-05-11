import { ArtifactSchema, IOHandlerCallback } from "@/types";
import { createSummary } from "@/api";

/**
 * Generates a summary for an artifact, and updates the app state.
 *
 * @param artifact - The artifact to summarize.
 * @param onSuccess - Called if the summary is generated successfully.
 * @param onError - Called if the summary generation fails.
 * @param onComplete - Called after the action completes.
 */
export async function handleGenerateArtifactSummary(
  artifact: ArtifactSchema,
  { onSuccess, onError, onComplete }: IOHandlerCallback<string>
): Promise<void> {
  // TODO:
  //  1. Generate a summary for the artifact.
  //  2. Save changes to the artifact.
  //  3. Update the artifact in the app state.
  try {
    const summary = await createSummary(artifact);

    onSuccess?.(summary);
  } catch (e) {
    onError?.(e as Error);
  } finally {
    onComplete?.();
  }
}

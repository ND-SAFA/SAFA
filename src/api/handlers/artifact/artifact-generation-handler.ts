import { ArtifactSchema, IOHandlerCallback } from "@/types";

/**
 * Generates a summary for an artifact, and updates the app state.
 *
 * @param artifact - The artifact to summarize.
 * @param onSuccess - Called if the summary is generated successfully.
 * @param onError - Called if the summary generation fails.
 * @param onComplete - Called after the action completes.
 */
export function handleGenerateArtifactSummary(
  artifact: ArtifactSchema,
  { onSuccess, onError, onComplete }: IOHandlerCallback
): void {
  // TODO:
  //  1. Generate a summary for the artifact.
  //  2. Save changes to thee artifact.
  //  3. Update the artifact in the app state.
  setTimeout(() => {
    artifact.summary = "Some generated summary.";
    onSuccess?.();
    onComplete?.();
  }, 1000);
}

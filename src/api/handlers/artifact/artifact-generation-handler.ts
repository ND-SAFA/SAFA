import {
  ArtifactSchema,
  ArtifactSummaryConfirmation,
  IOHandlerCallback,
} from "@/types";
import { logStore } from "@/hooks";
import { createSummary, handleSaveArtifact } from "@/api";

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
  {
    onSuccess,
    onError,
    onComplete,
  }: IOHandlerCallback<ArtifactSummaryConfirmation>
): Promise<void> {
  try {
    const summary = await createSummary(artifact);

    const confirm = () =>
      handleSaveArtifact(
        {
          ...artifact,
          summary,
        },
        true,
        undefined,
        {}
      );

    onSuccess?.({ summary, confirm });
  } catch (e) {
    onError?.(e as Error);
    logStore.onError(`Failed to generate summary: ${artifact.name}`);
  } finally {
    onComplete?.();
  }
}

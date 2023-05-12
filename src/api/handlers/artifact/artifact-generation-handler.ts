import {
  ArtifactSchema,
  ArtifactSummaryConfirmation,
  IOHandlerCallback,
} from "@/types";
import { artifactSaveStore, logStore } from "@/hooks";
import { createPrompt, createSummary, handleSaveArtifact } from "@/api";

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
          summary: generateConfirmation.summary,
        },
        true,
        undefined,
        {}
      );
    const generateConfirmation = { summary, confirm };

    onSuccess?.(generateConfirmation);
  } catch (e) {
    onError?.(e as Error);
    logStore.onError(`Failed to generate summary: ${artifact.name}`);
  } finally {
    onComplete?.();
  }
}

/**
 * Generates the body of an artifact based on an artifact prompt.
 * Uses the artifact currently being edited, and updates the edited artifact body to the response.
 *
 * @param onSuccess - Called if the body is generated successfully.
 * @param onError - Called if the body generation fails.
 * @param onComplete - Called after the action completes.
 */
export async function handleGenerateArtifactBody({
  onSuccess,
  onError,
  onComplete,
}: IOHandlerCallback): Promise<void> {
  const artifact = artifactSaveStore.editedArtifact;

  try {
    artifact.body = await createPrompt(artifact.body);

    onSuccess?.();
  } catch (e) {
    onError?.(e as Error);
    logStore.onError(
      `Failed to generate body based on prompt: ${artifact.name}`
    );
  } finally {
    onComplete?.();
  }
}

import { GenerateArtifactSchema, IOHandlerCallback } from "@/types";
import { artifactStore, logStore, projectStore, traceStore } from "@/hooks";
import { createGeneratedArtifacts } from "@/api";

/**
 * Generates parent artifacts based on child artifacts, and stores the generated artifacts.
 *
 * @param configuration - The configuration for generating the artifacts.
 * @param onSuccess - Called if the artifacts are generated successfully.
 * @param onError - Called if the artifact generation fails.
 * @param onComplete - Called after the action completes.
 */
export async function handleGenerateArtifacts(
  configuration: GenerateArtifactSchema,
  { onSuccess, onError, onComplete }: IOHandlerCallback
): Promise<void> {
  try {
    const commit = await createGeneratedArtifacts(
      configuration,
      projectStore.versionId
    );

    artifactStore.addOrUpdateArtifacts(commit.artifacts.added);
    traceStore.addOrUpdateTraceLinks(commit.traces.added);

    logStore.onSuccess("Successfully generated artifacts.");
    onSuccess?.();
  } catch (e) {
    logStore.onError("Unable to generate artifacts.");
    onError?.(e as Error);
  } finally {
    onComplete?.();
  }
}

import { ComputedRef, Ref } from "vue";
import {
  ArtifactSchema,
  ArtifactSummaryConfirmation,
  GenerateArtifactSchema,
  IOHandlerCallback,
} from "@/types";

/**
 * A hook for calling artifact generation API endpoints.
 */
export interface ArtifactGenerationApiHook {
  /**
   * If a summary has been generated, represents the summary and a callback to save it.
   */
  summaryGenConfirm: Ref<ArtifactSummaryConfirmation | undefined>;
  /**
   * Whether the name generation request is loading.
   */
  nameGenLoading: ComputedRef<boolean>;
  /**
   * Whether the body generation request is loading.
   */
  bodyGenLoading: ComputedRef<boolean>;
  /**
   * Whether the summary generation request is loading.
   */
  summaryGenLoading: ComputedRef<boolean>;
  /**
   * Whether the artifact generation request is loading.
   */
  artifactGenLoading: ComputedRef<boolean>;
  /**
   * Generates a summary for an artifact, and updates the app state.
   *
   * @param artifact - The artifact to summarize.
   * @param callbacks - The callbacks to use for the action.
   */
  handleGenerateSummary(
    artifact: ArtifactSchema,
    callbacks?: IOHandlerCallback
  ): Promise<void>;
  /**
   * Generates all summaries for an artifact type.
   *
   * @param artifactIds - The artifacts to summarize.
   * @param callbacks - The callbacks to use for the action.
   */
  handleGenerateAllSummaries(
    artifactIds: string[],
    callbacks?: IOHandlerCallback
  ): Promise<void>;
  /**
   * Generates the name of an artifact based on the body.
   * Uses the artifact currently being edited, and updates the edited artifact name to the response.
   *
   * @param callbacks - The callbacks to use for the action.
   */
  handleGenerateName(callbacks?: IOHandlerCallback): Promise<void>;
  /**
   * Generates the body of an artifact based on an artifact prompt.
   * Uses the artifact currently being edited, and updates the edited artifact body to the response.
   *
   * @param callbacks - The callbacks to use for the action.
   */
  handleGenerateBody(callbacks?: IOHandlerCallback): Promise<void>;
  /**
   * Generates parent artifacts based on child artifacts, and stores the generated artifacts.
   *
   * @param configuration - The configuration for generating the artifacts.
   * @param callbacks - The callbacks for the action.
   */
  handleGenerateArtifacts(
    configuration: GenerateArtifactSchema,
    callbacks: IOHandlerCallback
  ): Promise<void>;
}

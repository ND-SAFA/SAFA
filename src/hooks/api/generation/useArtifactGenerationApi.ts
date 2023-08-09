import { defineStore } from "pinia";

import { computed, ref } from "vue";
import {
  GenerateArtifactSchema,
  IOHandlerCallback,
  ArtifactSchema,
  ArtifactSummaryConfirmation,
} from "@/types";
import {
  useApi,
  projectStore,
  artifactSaveStore,
  artifactApiStore,
  jobStore,
} from "@/hooks";
import { createGeneratedArtifacts, createPrompt, createSummary } from "@/api";
import { pinia } from "@/plugins";

export const useArtifactGenerationApi = defineStore(
  "artifactGenerationApi",
  () => {
    const nameGenerationApi = useApi("nameGenerationApi");
    const bodyGenerationApi = useApi("bodyGenerationApi");
    const summaryGenerationApi = useApi("summaryGenerationApi");
    const artifactGenerationApi = useApi("artifactGenerationApi");

    const summaryGenConfirm = ref<ArtifactSummaryConfirmation | undefined>(
      undefined
    );

    const nameGenLoading = computed(() => nameGenerationApi.loading);
    const bodyGenLoading = computed(() => bodyGenerationApi.loading);
    const summaryGenLoading = computed(() => summaryGenerationApi.loading);
    const artifactGenLoading = computed(() => artifactGenerationApi.loading);

    /**
     * Generates a summary for an artifact, and updates the app state.
     *
     * @param artifact - The artifact to summarize.
     * @param callbacks - The callbacks to use for the action.
     */
    async function handleGenerateSummary(
      artifact: ArtifactSchema,
      callbacks: IOHandlerCallback = {}
    ): Promise<void> {
      await summaryGenerationApi.handleRequest(
        async () => {
          const summary = await createSummary(artifact);

          const clear = () => (summaryGenConfirm.value = undefined);
          const confirm = () =>
            artifactApiStore.handleSave(
              {
                ...artifact,
                summary: summaryGenConfirm.value?.summary || "",
              },
              true,
              undefined,
              { onComplete: clear }
            );

          summaryGenConfirm.value = { summary, confirm, clear };
        },
        callbacks,
        {
          error: `Failed to generate summary: ${artifact.name}`,
        }
      );
    }

    /**
     * Generates the name of an artifact based on the body.
     * Uses the artifact currently being edited, and updates the edited artifact name to the response.
     *
     * @param callbacks - The callbacks to use for the action.
     */
    async function handleGenerateName(
      callbacks: IOHandlerCallback = {}
    ): Promise<void> {
      const artifact = artifactSaveStore.editedArtifact;

      await nameGenerationApi.handleRequest(
        async () => {
          artifact.name = await createPrompt(
            `Generate a 3 word name for:\n\`\`\`\n${artifact.body}\n\`\`\``
          );
        },
        callbacks,
        {
          error: `Failed to generate name based on the body: ${artifact.name}`,
        }
      );
    }

    /**
     * Generates the body of an artifact based on an artifact prompt.
     * Uses the artifact currently being edited, and updates the edited artifact body to the response.
     *
     * @param callbacks - The callbacks to use for the action.
     */
    async function handleGenerateBody(
      callbacks: IOHandlerCallback = {}
    ): Promise<void> {
      const artifact = artifactSaveStore.editedArtifact;

      await bodyGenerationApi.handleRequest(
        async () => {
          artifact.body = await createPrompt(artifact.body);
        },
        callbacks,
        {
          error: `Failed to generate body based on prompt: ${artifact.name}`,
        }
      );
    }

    /**
     * Generates parent artifacts based on child artifacts, and stores the generated artifacts.
     *
     * @param configuration - The configuration for generating the artifacts.
     * @param callbacks - The callbacks for the action.
     */
    async function handleGenerateArtifacts(
      configuration: GenerateArtifactSchema,
      callbacks: IOHandlerCallback
    ): Promise<void> {
      await artifactGenerationApi.handleRequest(
        async () => {
          const job = await createGeneratedArtifacts(
            configuration,
            projectStore.versionId
          );

          jobStore.updateJob(job);
        },
        callbacks,
        {
          success:
            "Artifacts are being generated. You'll receive an update when they have been created.",
          error: "Unable to generate artifacts.",
        }
      );
    }

    return {
      summaryGenConfirm,
      nameGenLoading,
      bodyGenLoading,
      summaryGenLoading,
      artifactGenLoading,
      handleGenerateSummary,
      handleGenerateName,
      handleGenerateBody,
      handleGenerateArtifacts,
    };
  }
);

export default useArtifactGenerationApi(pinia);

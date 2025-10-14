import { defineStore } from "pinia";

import { computed, ref } from "vue";
import {
  ArtifactGenerationApiHook,
  ArtifactSchema,
  ArtifactSummaryConfirmation,
  GenerateArtifactSchema,
  IOHandlerCallback,
} from "@/types";
import {
  artifactApiStore,
  artifactCommitApiStore,
  artifactSaveStore,
  artifactStore,
  jobApiStore,
  projectStore,
  useApi,
} from "@/hooks";
import { createGeneratedArtifacts, createPrompt, createSummary } from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing artifact generation API requests.
 */
export const useArtifactGenerationApi = defineStore(
  "artifactGenerationApi",
  (): ArtifactGenerationApiHook => {
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

    async function handleGenerateSummary(
      artifact: ArtifactSchema,
      callbacks: IOHandlerCallback = {}
    ): Promise<void> {
      await summaryGenerationApi.handleRequest(
        async () => {
          const summaries = await createSummary(
            projectStore.versionId,
            artifact.id
          );

          const clear = () => (summaryGenConfirm.value = undefined);
          const confirm = () =>
            artifactApiStore.handleSave(
              {
                ...artifact,
                summary: summaryGenConfirm.value?.summary || "",
              },
              true,
              [],
              [],
              { onComplete: clear }
            );

          summaryGenConfirm.value = {
            summary: summaries[0] || "",
            confirm,
            clear,
          };
        },
        {
          ...callbacks,
          error: `Failed to generate summary: ${artifact.name}`,
        }
      );
    }

    async function handleGenerateAllSummaries(
      artifactIds: string[],
      callbacks: IOHandlerCallback = {}
    ): Promise<void> {
      await summaryGenerationApi.handleRequest(
        async () => {
          const artifacts = artifactStore.allArtifacts.filter(({ id }) =>
            artifactIds.includes(id)
          );

          const summaries = await createSummary(
            projectStore.versionId,
            ...artifacts.map(({ id }) => id)
          );

          const updatedArtifacts = await artifactCommitApiStore.handleUpdate(
            ...artifacts.map((artifact, index) => ({
              ...artifact,
              summary: summaries[index] || "",
            }))
          );

          artifactStore.addOrUpdateArtifacts(updatedArtifacts);
        },
        {
          ...callbacks,
          success: "Successfully generated summaries.",
          error: "Failed to generate summaries",
        }
      );
    }

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
        {
          ...callbacks,
          error: `Failed to generate name based on the body: ${artifact.name}`,
        }
      );
    }

    async function handleGenerateBody(
      callbacks: IOHandlerCallback = {}
    ): Promise<void> {
      const artifact = artifactSaveStore.editedArtifact;

      await bodyGenerationApi.handleRequest(
        async () => {
          artifact.body = await createPrompt(artifact.body);
        },
        {
          ...callbacks,
          error: `Failed to generate body based on prompt: ${artifact.name}`,
        }
      );
    }

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

          await jobApiStore.handleCreate(job);
        },
        {
          ...callbacks,
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
      handleGenerateAllSummaries,
      handleGenerateName,
      handleGenerateBody,
      handleGenerateArtifacts,
    };
  }
);

export default useArtifactGenerationApi(pinia);

import { defineStore } from "pinia";

import {
  ApprovalType,
  ArtifactLevelSchema,
  FlatTraceLink,
  IOHandlerCallback,
  ModelType,
  GenerationModelSchema,
} from "@/types";
import { createGeneratedMatrix } from "@/util";
import {
  useApi,
  approvalStore,
  artifactStore,
  jobApiStore,
  projectStore,
} from "@/hooks";
import {
  createGeneratedLinks,
  createModelTraining,
  getGeneratedLinks,
} from "@/api";
import { pinia } from "@/plugins";

export const useTraceGenerationApi = defineStore("traceGenerationApi", () => {
  const traceGenerationApi = useApi("traceGenerationApi");

  /**
   * Updates the storage of generated links.
   *
   * @param callbacks - The callbacks to use for the action.
   */
  async function handleReload(
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    if (!projectStore.isProjectDefined) return;

    await traceGenerationApi.handleRequest(
      async () => {
        const traceLinks: FlatTraceLink[] = [];
        const approvedIds: string[] = [];
        const declinedIds: string[] = [];
        const generatedLinks = await getGeneratedLinks(projectStore.versionId);

        generatedLinks.forEach((link) => {
          const source = artifactStore.getArtifactById(link.sourceId);
          const target = artifactStore.getArtifactById(link.targetId);

          if (link.approvalStatus === ApprovalType.APPROVED) {
            approvedIds.push(link.traceLinkId);
          } else if (link.approvalStatus === ApprovalType.DECLINED) {
            declinedIds.push(link.traceLinkId);
          }

          traceLinks.push({
            ...link,
            sourceType: source?.type || "",
            sourceBody: source?.body || "",
            targetType: target?.type || "",
            targetBody: target?.body || "",
          });
        });

        approvalStore.initializeTraces({
          traceLinks,
          approvedIds,
          declinedIds,
        });
      },
      callbacks,
      { useAppLoad: true }
    );
  }

  /**
   * Generates links between sets of artifact types and adds them to the project.
   *
   * @param method - The base model to generate with.
   * @param artifactLevels - An array of source and target artifact types to generate traces between.
   * @param callbacks - The callbacks to use for the action.
   */
  async function handleGenerate(
    method: ModelType | undefined,
    artifactLevels: ArtifactLevelSchema[],
    callbacks: IOHandlerCallback
  ): Promise<void> {
    const matricesName = artifactLevels
      .map(({ source, target }) => `${source} -> ${target}`)
      .join(", ");

    await traceGenerationApi.handleRequest(
      async () => {
        const job = await createGeneratedLinks({
          requests: [createGeneratedMatrix(artifactLevels, method)],
          projectVersion: projectStore.version,
        });

        await jobApiStore.handleCreate(job);
      },
      callbacks,
      {
        success: `Started generating new trace links: ${matricesName}. You'll receive a notification once they are added.`,
        error: `Unable to generate new trace links: ${matricesName}`,
      }
    );
  }

  /**
   * Trains models on created trace links.
   *
   * @param model - The model to train.
   * @param artifactLevels - An array of source and target artifact types to train on traces between.
   * @param callbacks - The callbacks to use for the action.
   */
  async function handleTrain(
    model: GenerationModelSchema,
    artifactLevels: ArtifactLevelSchema[],
    callbacks: IOHandlerCallback
  ): Promise<void> {
    const matricesName = artifactLevels
      .map(({ source, target }) => `${source} -> ${target}`)
      .join(", ");

    await traceGenerationApi.handleRequest(
      async () => {
        const job = await createModelTraining(projectStore.projectId, {
          requests: [
            createGeneratedMatrix(artifactLevels, model.baseModel, model),
          ],
        });

        await jobApiStore.handleCreate(job);
      },
      callbacks,
      {
        success: `Started training model on: ${matricesName}. You'll receive a notification once complete.`,
        error: `Unable to train model on: ${matricesName}`,
      }
    );
  }

  return { handleReload, handleGenerate, handleTrain };
});

export default useTraceGenerationApi(pinia);

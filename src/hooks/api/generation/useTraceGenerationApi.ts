import { defineStore } from "pinia";

import { computed } from "vue";
import {
  MatrixSchema,
  FlatTraceLink,
  IOHandlerCallback,
  ModelType,
  GenerationModelSchema,
  TraceGenerationApiHook,
} from "@/types";
import { buildGeneratedMatrix } from "@/util";
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

/**
 * A hook for managing trace generation API requests.
 */
export const useTraceGenerationApi = defineStore(
  "traceGenerationApi",
  (): TraceGenerationApiHook => {
    const traceGenerationApi = useApi("traceGenerationApi");

    const loading = computed(() => traceGenerationApi.loading);

    async function handleReload(
      callbacks: IOHandlerCallback = {}
    ): Promise<void> {
      if (!projectStore.isProjectDefined) return;

      await traceGenerationApi.handleRequest(
        async () => {
          const traceLinks: FlatTraceLink[] = [];
          const approvedIds: string[] = [];
          const declinedIds: string[] = [];
          const generatedLinks = await getGeneratedLinks(
            projectStore.versionId
          );

          generatedLinks.forEach((link) => {
            const source = artifactStore.getArtifactById(link.sourceId);
            const target = artifactStore.getArtifactById(link.targetId);

            if (link.approvalStatus === "APPROVED") {
              approvedIds.push(link.traceLinkId);
            } else if (link.approvalStatus === "DECLINED") {
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
        {
          ...callbacks,
          useAppLoad: true,
        }
      );
    }

    async function handleGenerate(
      method: ModelType | undefined,
      matrices: MatrixSchema[],
      callbacks: IOHandlerCallback
    ): Promise<void> {
      const matricesName = matrices
        .map(({ source, target }) => `${source} -> ${target}`)
        .join(", ");

      await traceGenerationApi.handleRequest(
        async () => {
          const job = await createGeneratedLinks({
            requests: [buildGeneratedMatrix(matrices, method)],
            projectVersion: projectStore.version,
          });

          await jobApiStore.handleCreate(job);
        },
        {
          ...callbacks,
          success: `Started generating new trace links: ${matricesName}. You'll receive a notification once they are added.`,
          error: `Unable to generate new trace links: ${matricesName}`,
        }
      );
    }

    async function handleTrain(
      model: GenerationModelSchema,
      matrices: MatrixSchema[],
      callbacks: IOHandlerCallback
    ): Promise<void> {
      const matricesName = matrices
        .map(({ source, target }) => `${source} -> ${target}`)
        .join(", ");

      await traceGenerationApi.handleRequest(
        async () => {
          const job = await createModelTraining(projectStore.projectId, {
            requests: [buildGeneratedMatrix(matrices, model.baseModel, model)],
          });

          await jobApiStore.handleCreate(job);
        },
        {
          ...callbacks,
          success: `Started training model on: ${matricesName}. You'll receive a notification once complete.`,
          error: `Unable to train model on: ${matricesName}`,
        }
      );
    }

    return { loading, handleReload, handleGenerate, handleTrain };
  }
);

export default useTraceGenerationApi(pinia);

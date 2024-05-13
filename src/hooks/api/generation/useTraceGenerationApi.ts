import { defineStore } from "pinia";

import { computed } from "vue";
import {
  MatrixSchema,
  FlatTraceLink,
  IOHandlerCallback,
  TraceGenerationApiHook,
} from "@/types";
import { buildGeneratedMatrix } from "@/util";
import {
  useApi,
  approvalStore,
  artifactStore,
  jobApiStore,
  projectStore,
  traceStore,
} from "@/hooks";
import { createGeneratedLinks } from "@/api";
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
          const generatedLinks = traceStore.allTraces;

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
      matrices: MatrixSchema[],
      callbacks: IOHandlerCallback
    ): Promise<void> {
      const matricesName = matrices
        .map(({ source, target }) => `${source} -> ${target}`)
        .join(", ");

      await traceGenerationApi.handleRequest(
        async () => {
          const job = await createGeneratedLinks({
            requests: [buildGeneratedMatrix(matrices)],
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

    return { loading, handleReload, handleGenerate };
  }
);

export default useTraceGenerationApi(pinia);

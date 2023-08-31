import { defineStore } from "pinia";

import { ApprovalType, ArtifactSchema, TraceLinkSchema } from "@/types";
import { commitApiStore } from "@/hooks";
import { pinia } from "@/plugins";
import { ArtifactCommitApiHook } from "@/types/hooks/api/commit";

export const useArtifactCommitApi = defineStore(
  "artifactCommitApi",
  (): ArtifactCommitApiHook => {
    async function handleCreate(
      versionId: string,
      artifact: ArtifactSchema
    ): Promise<ArtifactSchema[]> {
      return commitApiStore
        .handleSave((builder) => builder.withNewArtifact(artifact))
        .then((commit) => commit?.artifacts.added || []);
    }

    async function handleUpdate(
      versionId: string,
      artifact: ArtifactSchema
    ): Promise<ArtifactSchema[]> {
      return commitApiStore
        .handleSave((builder) => builder.withModifiedArtifact(artifact))
        .then((commit) => commit?.artifacts.modified || []);
    }

    async function handleDelete(
      artifact: ArtifactSchema,
      traceLinks: TraceLinkSchema[]
    ): Promise<ArtifactSchema> {
      traceLinks = traceLinks.map((link) => ({
        ...link,
        approvalStatus: ApprovalType.DECLINED,
      }));

      return commitApiStore
        .handleSave((builder) =>
          builder
            .withRemovedArtifact(artifact)
            .withModifiedTraceLink(...traceLinks)
        )
        .then(() => artifact);
    }

    return { handleCreate, handleUpdate, handleDelete };
  }
);

export default useArtifactCommitApi(pinia);

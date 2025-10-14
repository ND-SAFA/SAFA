import { defineStore } from "pinia";

import {
  ArtifactSchema,
  TraceLinkSchema,
  ArtifactCommitApiHook,
} from "@/types";
import { commitApiStore } from "@/hooks";
import { pinia } from "@/plugins";

/**
 * A hook for managing artifact commit API requests.
 */
export const useArtifactCommitApi = defineStore(
  "artifactCommitApi",
  (): ArtifactCommitApiHook => {
    async function handleCreate(
      ...artifacts: ArtifactSchema[]
    ): Promise<ArtifactSchema[]> {
      return commitApiStore
        .handleSave((builder) => builder.withNewArtifact(...artifacts))
        .then((commit) => commit?.artifacts.added || []);
    }

    async function handleUpdate(
      ...artifacts: ArtifactSchema[]
    ): Promise<ArtifactSchema[]> {
      return commitApiStore
        .handleSave((builder) => builder.withModifiedArtifact(...artifacts))
        .then((commit) => commit?.artifacts.modified || []);
    }

    async function handleDelete(
      artifact: ArtifactSchema,
      traceLinks: TraceLinkSchema[]
    ): Promise<ArtifactSchema> {
      traceLinks = traceLinks.map((link) => ({
        ...link,
        approvalStatus: "DECLINED",
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

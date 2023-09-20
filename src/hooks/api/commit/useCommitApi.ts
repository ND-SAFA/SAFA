import { defineStore } from "pinia";

import { CommitSchema, CommitApiHook } from "@/types";
import { CommitBuilder } from "@/util";
import {
  appStore,
  commitStore,
  traceStore,
  artifactStore,
  traceGenerationApiStore,
  projectStore,
  useApi,
} from "@/hooks";
import { persistCommit } from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing commit API requests.
 */
export const useCommitApi = defineStore("commitApi", (): CommitApiHook => {
  const commitApi = useApi("commitApi");

  /**
   * Creates a new commit based on the current project version.
   */
  function buildCommit(): CommitBuilder {
    const version = projectStore.version;

    if (version === undefined) {
      throw Error("No project version is selected.");
    }

    return new CommitBuilder(version);
  }

  /**
   * Applies all artifact changes from a commit.
   *
   * @param commit - The commit to apply.
   */
  async function applyArtifactChanges(commit: CommitSchema): Promise<void> {
    artifactStore.addOrUpdateArtifacts([
      ...commit.artifacts.added,
      ...commit.artifacts.modified,
    ]);
    artifactStore.deleteArtifacts(commit.artifacts.removed);
    traceStore.addOrUpdateTraceLinks([
      ...commit.traces.added,
      ...commit.traces.modified,
    ]);
    traceStore.deleteTraceLinks(commit.traces.removed);

    if (commit.traces.modified.length === 0) return;

    // Reload generated links if any are modified.
    await traceGenerationApiStore.handleReload();
  }

  async function handleSave(
    commitOrCb: CommitSchema | ((builder: CommitBuilder) => CommitBuilder)
  ): Promise<CommitSchema | undefined> {
    return commitApi.handleRequest(
      async () => {
        appStore.isSaving = true;

        const commit =
          typeof commitOrCb === "function"
            ? commitOrCb(buildCommit()).commit
            : commitOrCb;

        const commitResponse = await persistCommit(commit);

        const fullCommit = {
          ...commitResponse,
          artifacts: {
            added: commitResponse.artifacts.added,
            modified: commitResponse.artifacts.modified,
            removed: commit.artifacts.removed,
          },
          traces: {
            added: commitResponse.traces.added,
            modified: commitResponse.traces.modified,
            removed: commit.traces.removed,
          },
        };

        commitStore.saveCommit(fullCommit);

        return fullCommit;
      },
      {
        onComplete: () => (appStore.isSaving = false),
      }
    );
  }

  async function handleUndo(): Promise<void> {
    await commitApi.handleRequest(
      async () => {
        appStore.isSaving = true;

        const commit = await commitStore.undoLastCommit();

        if (!commit) return;

        const commitResponse = await persistCommit(commit);

        await applyArtifactChanges(commitResponse);
      },
      {
        onComplete: () => (appStore.isSaving = false),
      }
    );
  }

  async function handleRedo(): Promise<void> {
    await commitApi.handleRequest(
      async () => {
        appStore.isSaving = true;

        const commit = await commitStore.redoLastUndoneCommit();

        if (!commit) return;

        const commitResponse = await persistCommit(commit);

        await applyArtifactChanges(commitResponse);
      },
      {
        onComplete: () => (appStore.isSaving = false),
      }
    );
  }

  return {
    handleSave,
    handleUndo,
    handleRedo,
  };
});

export default useCommitApi(pinia);

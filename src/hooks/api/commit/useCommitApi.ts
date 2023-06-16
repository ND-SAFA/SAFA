import { defineStore } from "pinia";

import { CommitSchema } from "@/types";
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

export const useCommitApi = defineStore("commitApi", () => {
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
   * Saves commit to the application store, and persist the commit.
   *
   * @param commitOrCb - The commit to save, or a callback to create it.
   * @return The saved commit.
   */
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

  /**
   * Undoes the last commit.
   */
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

  /**
   * Reattempts the last undone commit.
   */
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

  return {
    handleSave,
    handleUndo,
    handleRedo,
  };
});

export default useCommitApi(pinia);

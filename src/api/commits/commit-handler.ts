import { Commit } from "@/types";
import { appStore, commitStore, traceStore, artifactStore } from "@/hooks";
import { handleGetGeneratedLinks, persistCommit } from "@/api";

/**
 * Saves commit to the application store, and persist the commit.
 *
 * @param commit - The commit to save.
 * @return The saved commit.
 */
export async function saveCommit(commit: Commit): Promise<Commit> {
  try {
    appStore.isSaving = true;

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
  } finally {
    appStore.isSaving = false;
  }
}

/**
 * Undoes the last commit.
 */
export async function undoCommit(): Promise<void> {
  try {
    appStore.isSaving = true;

    const commit = await commitStore.undoLastCommit();

    if (!commit) return;

    const commitResponse = await persistCommit(commit);

    await applyArtifactChanges(commitResponse);
  } finally {
    appStore.isSaving = false;
  }
}

/**
 * Reattempts the last undone commit.
 */
export async function redoCommit(): Promise<void> {
  try {
    appStore.isSaving = true;

    const commit = await commitStore.redoLastUndoneCommit();

    if (!commit) return;

    const commitResponse = await persistCommit(commit);

    await applyArtifactChanges(commitResponse);
  } finally {
    appStore.isSaving = false;
  }
}

/**
 * Applies all artifact changes from a commit.
 *
 * @param commit - The commit to apply.
 */
async function applyArtifactChanges(commit: Commit): Promise<void> {
  await artifactStore.addOrUpdateArtifacts([
    ...commit.artifacts.added,
    ...commit.artifacts.modified,
  ]);
  await artifactStore.deleteArtifacts(commit.artifacts.removed);
  await traceStore.addOrUpdateTraceLinks([
    ...commit.traces.added,
    ...commit.traces.modified,
  ]);
  await traceStore.deleteTraceLinks(commit.traces.removed);
  await handleGetGeneratedLinks({});
}

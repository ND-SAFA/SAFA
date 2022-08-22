import { Commit } from "@/types";
import { projectModule, commitModule } from "@/store";
import { appStore } from "@/hooks";
import { persistCommit } from "@/api";

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
    await commitModule.saveCommit(commitResponse);

    return commitResponse;
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

    const commit = await commitModule.undoLastCommit();
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

    const commit = await commitModule.redoLastUndoneCommit();
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
  await projectModule.addOrUpdateArtifacts([
    ...commit.artifacts.added,
    ...commit.artifacts.modified,
  ]);
  await projectModule.deleteArtifacts(commit.artifacts.removed);
  await projectModule.addOrUpdateTraceLinks([
    ...commit.traces.added,
    ...commit.traces.modified,
  ]);
  await projectModule.deleteTraceLinks(commit.traces.removed);
}

import { Commit } from "@/types";
import { projectModule, commitModule, appModule } from "@/store";
import { persistCommit } from "@/api";

/**
 * Saves commit to the application store, and persist the commit.
 *
 * @param commit - The commit to save.
 * @return The saved commit.
 */
export async function saveCommit(commit: Commit): Promise<Commit> {
  appModule.SET_IS_SAVING(true);

  const commitResponse = await persistCommit(commit);
  await commitModule.saveCommit(commitResponse);

  appModule.SET_IS_SAVING(false);

  return commitResponse;
}

/**
 * Undoes the last commit.
 */
export async function undoCommit(): Promise<void> {
  appModule.SET_IS_SAVING(true);

  const commit = await commitModule.undoLastCommit();
  const commitResponse = await persistCommit(commit);

  await applyArtifactChanges(commitResponse);

  appModule.SET_IS_SAVING(false);
}

/**
 * Reattempts the last undone commit.
 */
export async function redoCommit(): Promise<void> {
  appModule.SET_IS_SAVING(true);

  const commit = await commitModule.redoLastUndoneCommit();
  const commitResponse = await persistCommit(commit);

  await applyArtifactChanges(commitResponse);

  appModule.SET_IS_SAVING(false);
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

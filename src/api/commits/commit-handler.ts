import { Commit } from "@/types";
import { projectModule, commitModule } from "@/store";
import { persistCommit } from "@/api";

/**
 * Saves commit to the application store, and persist the commit.
 *
 * @param commit - The commit to save.
 * @return The saved commit.
 */
export async function saveCommit(commit: Commit): Promise<Commit> {
  const commitResponse = await persistCommit(commit);

  await commitModule.saveCommit(commitResponse);

  return commitResponse;
}

/**
 * Undoes the last commit.
 */
export async function undoCommit(): Promise<void> {
  const commit = await commitModule.undoLastCommit();
  const commitResponse = await persistCommit(commit);

  await applyArtifactChanges(commitResponse);
}

/**
 * Reattempts the last undone commit.
 */
export async function redoCommit(): Promise<void> {
  const commit = await commitModule.redoLastUndoneCommit();
  const commitResponse = await persistCommit(commit);

  await applyArtifactChanges(commitResponse);
}

/**
 * Applies all artifact changes from a commit.
 *
 * @param commit - The commit to apply.
 */
async function applyArtifactChanges(commit: Commit): Promise<void> {
  const artifactsAddedOrModified = commit.artifacts.added.concat(
    commit.artifacts.modified
  );

  await projectModule.addOrUpdateArtifacts(artifactsAddedOrModified);
  await projectModule.deleteArtifacts(commit.artifacts.removed);
}

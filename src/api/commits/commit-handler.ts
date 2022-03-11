import { Commit } from "@/types";
import { artifactModule, commitModule } from "@/store";
import { persistCommit } from "./commit-api";

/**
 * Saves commit to the application store, and persist the commit.
 *
 * @param commit - The commit to save.
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

async function applyArtifactChanges(commit: Commit): Promise<void> {
  const artifactsAddedOrModified = commit.artifacts.added.concat(
    commit.artifacts.modified
  );
  await artifactModule.addOrUpdateArtifacts(artifactsAddedOrModified);
  await artifactModule.deleteArtifacts(commit.artifacts.removed);
}

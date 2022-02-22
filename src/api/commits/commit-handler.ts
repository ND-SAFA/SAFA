import { Commit } from "@/types";
import { commitModule } from "@/store";
import { persistCommit } from "./commit-api";

/**
 * Saves commit to the application store, and persist the commit.
 *
 * @param commit - The commit to save.
 */
export async function saveCommit(commit: Commit): Promise<Commit> {
  await commitModule.saveCommit(commit);
  return await persistCommit(commit);
}

/**
 * Undoes the last commit.
 */
export async function undoCommit(): Promise<Commit> {
  const commit = await commitModule.undoCommit();
  return await persistCommit(commit);
}

/**
 * Reattempts the last undone commit.
 */
export async function redoCommit(): Promise<Commit> {
  const commit = await commitModule.redoCommit();
  return await saveCommit(commit);
}

import { Commit } from "@/types";
import { commitModule } from "@/store";
import { persistCommit } from "@/api/commits";

/**
 * Saves commit to the application store, and persist the commit.
 *
 * @param commit - The commit to save.
 */
export async function saveCommit(commit: Commit): Promise<void> {
  await commitModule.saveCommit(commit);
  await persistCommit(commit);
}

/**
 * Undoes the last commit.
 */
export async function undoCommit(): Promise<void> {
  const commit = await commitModule.undoCommit();

  if (commit) {
    await persistCommit(commit);
  }
}

/**
 * Reattempts the last undone commit.
 */
export async function redoCommit(): Promise<void> {
  const commit = await commitModule.redoCommit();

  if (commit) {
    await saveCommit(commit);
  }
}

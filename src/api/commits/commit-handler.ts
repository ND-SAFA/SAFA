import { Commit } from "@/types";
import { projectStore, appStore, commitStore } from "@/hooks";
import { persistCommit } from "@/api";

/**
 * Saves commit to the application store, and persist the commit.
 *
 * @param commit - The commit to save.
 * @return The saved commit.
 */
export async function saveCommit(commit: Commit): Promise<Commit> {
  try {
    appStore.$patch({ isSaving: true });

    const commitResponse = await persistCommit(commit);
    commitStore.saveCommit(commitResponse);

    return commitResponse;
  } finally {
    appStore.$patch({ isSaving: false });
  }
}

/**
 * Undoes the last commit.
 */
export async function undoCommit(): Promise<void> {
  try {
    appStore.$patch({ isSaving: true });

    const commit = await commitStore.undoLastCommit();

    if (!commit) return;

    const commitResponse = await persistCommit(commit);

    await applyArtifactChanges(commitResponse);
  } finally {
    appStore.$patch({ isSaving: false });
  }
}

/**
 * Reattempts the last undone commit.
 */
export async function redoCommit(): Promise<void> {
  try {
    appStore.$patch({ isSaving: true });

    const commit = await commitStore.redoLastUndoneCommit();

    if (!commit) return;

    const commitResponse = await persistCommit(commit);

    await applyArtifactChanges(commitResponse);
  } finally {
    appStore.$patch({ isSaving: false });
  }
}

/**
 * Applies all artifact changes from a commit.
 *
 * @param commit - The commit to apply.
 */
async function applyArtifactChanges(commit: Commit): Promise<void> {
  await projectStore.addOrUpdateArtifacts([
    ...commit.artifacts.added,
    ...commit.artifacts.modified,
  ]);
  await projectStore.deleteArtifacts(commit.artifacts.removed);
  await projectStore.addOrUpdateTraceLinks([
    ...commit.traces.added,
    ...commit.traces.modified,
  ]);
  await projectStore.deleteTraceLinks(commit.traces.removed);
}

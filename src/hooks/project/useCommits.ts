import { defineStore } from "pinia";

import { ArtifactModel, Commit, CommitHistory, TraceLinkModel } from "@/types";
import { createCommit } from "@/util";
import { pinia } from "@/plugins";
import traceStore from "./useTraces";
import artifactStore from "./useArtifacts";

/**
 * This module tracks commits and allows for undoing them.
 */
export const useCommits = defineStore("commits", {
  state: () => ({
    /**
     * The ordered tuples of commits that have occurred
     * during the current session.
     */
    commits: [] as CommitHistory[],
    /**
     * The list of recently reverted commits.
     */
    revertedCommits: [] as CommitHistory[],
  }),
  getters: {
    /**
     * @return True if at least one commit exists.
     */
    canUndo(): boolean {
      return this.commits.length > 0;
    },
    /**
     * @return True if at least one commit has been reverted.
     */
    canRedo(): boolean {
      return this.revertedCommits.length > 0;
    },
  },
  actions: {
    /**
     * Given a commit, all added entities are deleted, all deleted entities are
     * re-added, and modified entities are reverted to their state before the last
     * client change.
     *
     * @param commit - The commit to create a reversion for.
     * @return The reversion commit.
     */
    getRevert(commit: Commit): Commit {
      return {
        ...createCommit(commit.commitVersion),
        artifacts: {
          added: commit.artifacts.removed,
          removed: commit.artifacts.added,
          modified: commit.artifacts.modified
            .map(({ id }) => artifactStore.getArtifactById(id))
            .filter((artifact) => !!artifact) as ArtifactModel[],
        },
        traces: {
          added: commit.traces.removed,
          removed: commit.traces.added,
          modified: commit.traces.modified
            .map((link) =>
              traceStore.getTraceLinkByArtifacts(link.sourceId, link.targetId)
            )
            .filter((link) => !!link) as TraceLinkModel[],
        },
      };
    },
    /**
     * Saves commit to the application store.
     *
     * @param commit - The commit to save.
     */
    saveCommit(commit: Commit): void {
      this.commits = [
        ...this.commits,
        { commit, revert: this.getRevert(commit) },
      ];
    },
    /**
     * Removes the last commit from the store and attempts to revert the changes.
     * If successful, the commit is stored in previously reverted commits.
     *
     * @return The undone commit.
     */
    undoLastCommit(): Commit | undefined {
      if (!this.canUndo) return;

      const lastCommitIndex = this.commits.length - 1;
      const lastCommitHistory = this.commits[lastCommitIndex];

      this.$patch({
        commits: this.commits.filter((c, idx) => idx !== lastCommitIndex),
        revertedCommits: [...this.revertedCommits, lastCommitHistory],
      });

      return lastCommitHistory.revert;
    },
    /**
     * Removes and returns the last reverted commit.
     *
     * @return The redone commit.
     */
    redoLastUndoneCommit(): Commit | undefined {
      if (!this.canRedo) return;

      const lastCommitIndex = this.revertedCommits.length - 1;
      const lastCommitHistory = this.revertedCommits[lastCommitIndex];

      this.revertedCommits = this.revertedCommits.filter(
        (c, idx) => idx !== lastCommitIndex
      );

      return lastCommitHistory.commit;
    },
  },
});

export default useCommits(pinia);

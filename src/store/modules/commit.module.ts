import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";
import type { Artifact, Commit } from "@/types";
import { logModule, projectModule } from "@/store";
import type { CommitHistory } from "@/types";
import { persistCommit } from "@/api";
import { createCommit } from "@/util";

@Module({ namespaced: true, name: "commit" })
/**
 * Keep track of the commits occurring in this session. Provides api for:
 * 1. Committing an action.
 * 2. Undoing an action.
 */
export default class CommitModule extends VuexModule {
  /**
   * The ordered tuples of commits (and its revert) that have occurred
   * during the current session.
   */
  private commits: CommitHistory[] = [];
  private revertedCommits: CommitHistory[] = [];

  @Action({ rawError: true })
  /**
   * Saves commit to the application store.
   *
   * @param commit - The commit to save.
   */
  async saveCommit(commit: Commit): Promise<void> {
    const revert = this.createRevert(commit);

    await persistCommit(commit);
    this.ADD_COMMIT({ commit, revert });
  }

  @Action
  /**
   * Removes the last commit from the store and attempts to revert the changes.
   * If successful, the commit is stored in previously reverted commits.
   */
  async undoCommit(): Promise<void> {
    if (!this.canUndo) {
      return logModule.onWarning("There are no commits to undo.");
    }

    const lastCommitIndex = this.commits.length - 1;
    const lastCommitHistory = this.commits[lastCommitIndex];

    await persistCommit(lastCommitHistory.revert);
    this.SET_COMMITS(this.commits.filter((c, i) => i !== lastCommitIndex));
    this.ADD_REVERTED_COMMIT(lastCommitHistory);
  }

  @Action
  /**
   * Reattempts the last undone commit.
   */
  async redoCommit(): Promise<void> {
    if (!this.canRedo) {
      return logModule.onWarning(
        "Cannot redo because no commits have been reverted."
      );
    }

    const lastCommitIndex = this.revertedCommits.length - 1;
    const lastCommitHistory = this.revertedCommits[lastCommitIndex];

    await this.saveCommit(lastCommitHistory.commit);
    this.SET_REVERTED_COMMITS(
      this.revertedCommits.filter((c, i) => i !== lastCommitIndex)
    );
  }

  @Mutation
  /**
   * Sets given list as commits.
   * @param commits
   */
  SET_COMMITS(commits: CommitHistory[]): void {
    this.commits = commits;
  }

  @Mutation
  /**
   * Sets given list as reverted commits
   */
  SET_REVERTED_COMMITS(revertedCommits: CommitHistory[]): void {
    this.revertedCommits = revertedCommits;
  }

  @Mutation
  /**
   * Adds a commit to the commit history
   */
  ADD_COMMIT(commitHistory: CommitHistory): void {
    this.commits = [...this.commits, commitHistory];
  }

  @Mutation
  /**
   * Adds a commit to the commit history
   */
  ADD_REVERTED_COMMIT(commitHistory: CommitHistory): void {
    this.revertedCommits = [...this.revertedCommits, commitHistory];
  }

  /**
   * Given a commit, all added entities are deleted, all deleted entities are
   * re-added, and modified entities are reverted to their state before the last
   * client change.
   */
  get createRevert(): (c: Commit) => Commit {
    return (commit: Commit) => {
      const originalArtifacts: Artifact[] = commit.artifacts.modified.map(
        (a: Artifact) => projectModule.getArtifactById(a.id)
      );
      const originalTraces = commit.traces.modified.map((t) =>
        projectModule.getTraceLinkByArtifacts(t.sourceId, t.targetId)
      );

      return {
        ...createCommit(commit.commitVersion),
        artifacts: {
          added: commit.artifacts.removed,
          removed: commit.artifacts.added,
          modified: originalArtifacts,
        },
        traces: {
          added: commit.traces.removed,
          removed: commit.traces.added,
          modified: originalTraces,
        },
      };
    };
  }

  /**
   * @return True if at least one commit exists.
   */
  get canUndo(): boolean {
    return this.commits.length > 0;
  }

  /**
   * @return True if at least one commit has been reverted.
   */
  get canRedo(): boolean {
    return this.revertedCommits.length > 0;
  }

  /**
   * @return The current commits.
   */
  get getCommits(): CommitHistory[] {
    return this.commits;
  }
}

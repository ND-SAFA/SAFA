import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";
import type { Artifact, Commit, CommitHistory } from "@/types";
import { createCommit } from "@/util";
import { artifactModule, logModule, traceModule } from "@/store";

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

    this.ADD_COMMIT({ commit, revert });
  }

  @Action
  /**
   * Removes the last commit from the store and attempts to revert the changes.
   * If successful, the commit is stored in previously reverted commits.
   *
   * @return The undone commit.
   */
  async undoCommit(): Promise<Commit | undefined> {
    if (!this.canUndo) {
      logModule.onWarning("There are no commits to undo.");
      return;
    }

    const lastCommitIndex = this.commits.length - 1;
    const lastCommitHistory = this.commits[lastCommitIndex];

    this.SET_COMMITS(this.commits.filter((c, i) => i !== lastCommitIndex));
    this.ADD_REVERTED_COMMIT(lastCommitHistory);

    return lastCommitHistory.revert;
  }

  @Action
  /**
   * Reattempts the last undone commit.
   *
   * @return The redone commit.
   */
  async redoCommit(): Promise<Commit | undefined> {
    if (!this.canRedo) {
      logModule.onWarning("Cannot redo because no commits have been reverted.");
      return;
    }

    const lastCommitIndex = this.revertedCommits.length - 1;
    const lastCommitHistory = this.revertedCommits[lastCommitIndex];

    this.SET_REVERTED_COMMITS(
      this.revertedCommits.filter((c, i) => i !== lastCommitIndex)
    );

    return lastCommitHistory.commit;
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
        (a: Artifact) => artifactModule.getArtifactById(a.id)
      );
      const originalTraces = commit.traces.modified.map((t) =>
        traceModule.getTraceLinkByArtifacts(t.sourceId, t.targetId)
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

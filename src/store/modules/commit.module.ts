import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";
import type { Artifact, Commit, ProjectVersion } from "@/types";
import authHttpClient from "@/api/endpoints/auth-http-client";
import { Endpoint, fillEndpoint } from "@/api/endpoints/endpoints";
import { appModule, projectModule } from "@/store";
import { CommitHistory } from "@/types";

type CommitFromVersionBuilder = (v: ProjectVersion) => Commit;

@Module({ namespaced: true, name: "commit" })
/**
 * Keep track of the commits occurring in this sessions. Provides api for:
 * 1. Committing an action
 * 2. Undoing an action
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
   * @param commit
   */
  async saveCommit(commit: Commit): Promise<void> {
    const revert = this.createRevert(commit);
    await this.persistCommit(commit);
    this.addCommit({ commit, revert });
  }

  @Action
  /**
   * Removes the last commit from the store and attempts to revert the commit's
   * changes. If successful, commit is stored in previously reverted commits.
   * 1. Added artifacts
   */
  async undoCommit(): Promise<void> {
    if (!this.canUndo) {
      return appModule.onWarning("Cannot undo because no commits are written");
    }
    const lastCommitIndex = this.commits.length - 1;
    if (lastCommitIndex < 0) {
      throw Error("Could not undo commit because there are no commits.");
    }
    const lastCommitHistory = this.commits[lastCommitIndex];
    await this.persistCommit(lastCommitHistory.revert);
    this.setCommits(this.commits.filter((c, i) => i !== lastCommitIndex));
    this.addRevertedCommit(lastCommitHistory);
  }

  @Action
  /**
   * Removes the last commit from the store and attempts to revert the commit's
   * changes. Reverting changes follows the following rules:
   * 1. Added artifacts
   */
  async redoCommit(): Promise<void> {
    if (!this.canRedo) {
      return appModule.onWarning(
        "Cannot redo because no commits have been reverted."
      );
    }
    const lastCommitIndex = this.revertedCommits.length - 1;
    if (lastCommitIndex < 0) {
      throw Error("Could not revert commit because no commits reverted.");
    }
    const lastCommitHistory = this.revertedCommits[lastCommitIndex];
    await this.saveCommit(lastCommitHistory.commit);
    this.setRevertedCommits(
      this.revertedCommits.filter((_, i) => i !== lastCommitIndex)
    );
  }

  @Action
  /**
   * Sends commit to backend to be saved to the database.
   * @param commit The commit to be persisted to the database.
   */
  persistCommit(commit: Commit): Promise<void> {
    const versionId = commit.commitVersion.versionId;
    return authHttpClient<void>(fillEndpoint(Endpoint.commit, { versionId }), {
      method: "POST",
      body: JSON.stringify(commit),
    });
  }

  @Mutation
  /**
   * Sets given list as commits.
   * @param commits
   */
  setCommits(commits: CommitHistory[]): void {
    this.commits = commits;
  }

  @Mutation
  /**
   * Sets given list as reverted commits
   */
  setRevertedCommits(revertedCommits: CommitHistory[]): void {
    this.revertedCommits = revertedCommits;
  }

  @Mutation
  /**
   * Adds a commit to the commit history
   */
  addCommit(commitHistory: CommitHistory): void {
    this.commits = this.commits.concat([commitHistory]);
  }

  @Mutation
  /**
   * Adds a commit to the commit history
   */
  addRevertedCommit(commitHistory: CommitHistory): void {
    this.revertedCommits = this.revertedCommits.concat([commitHistory]);
  }

  /**
   * @return a commit object initialed with given version and empty everywhere
   * else.
   */
  get emptyCommit(): CommitFromVersionBuilder {
    return (version: ProjectVersion) => {
      return {
        commitVersion: version,
        artifacts: {
          added: [],
          removed: [],
          modified: [],
        },
        traces: {
          added: [],
          removed: [],
          modified: [],
        },
      };
    };
  }

  /**
   * Given a commit all added entities are deleted, all deleted entities are
   * re-added, and modified entities are reverted to their state before the last
   * client change.
   */
  get createRevert(): (c: Commit) => Commit {
    return (commit: Commit) => {
      const originalArtifacts: Artifact[] = commit.artifacts.modified.map(
        (a: Artifact) => projectModule.getArtifactByName(a.name)
      );
      const originalTraces = commit.traces.modified.map((t) =>
        projectModule.getTraceLinkByArtifacts(t.source, t.target)
      );

      return {
        ...this.emptyCommit(commit.commitVersion),
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
   * @return true if at least one commit exists and false otherwise.
   */
  get canUndo(): boolean {
    return this.commits.length > 0;
  }

  /**
   * @return true if at least one commit has been reverted and false otherwise.
   */
  get canRedo(): boolean {
    return this.revertedCommits.length > 0;
  }

  get getCommits(): CommitHistory[] {
    return this.commits;
  }
}
